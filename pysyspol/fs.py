#!/usr/bin/env python
# coding=utf-8
# Author: Pedro Ivan Lopez
# Contact: http://pedroivanlopez.com

'''File system utilities
'''

# Standard library imports.
import sys
import os
import logging
import re
import shutil
from itertools import chain
from subprocess import Popen

from pysyspol.util import random_alphanumeric_str

__version__ = '0.01'

def rsync_multiple(src, dst, opts, *paths, rsync_path='rsync'):
    '''Runs *rsync* process multiple times

    Parameters
    ----------

    src: str
        Source filepath
    dst: str
        Destination filepath
    opts: sequence
        Extra options to *rsync* process
    *paths: finite iterable of finite iterables of str
        Inner iterables of strings have the following structure:

        - The first path is the path to sync, and is relative to ``src`` and
          ``dst``.
        - The rest of the paths, if any, are paths to be excluded from the
          *rsync* invocation. They are relative to the first path of the inner
          iterable

        If any path is a directory it must end with character ``/``.

        The length of this argument is the number of times the *rsync* process
        will be executed.
    rsync_path: str
        *Optional*, path to *rsync* executable

    Returns
    -------
    reports: tuple of tuples of length 2
        Inner tuples have the following structure:

        1. Tuple of strings with the command line of the *rsync* invocation
        2. ``int``, return code of the *rsync* invocation

    Notes
    -----

    See `this technical note
    <http://pedroivanlopez.com/rsync/#selective-mirror-with-excluded-directories>`
    '''
    report = []
    for ipaths in paths:
        cmd = [rsync_path, '--relative']
        cmd.extend(opts)
        path = ipaths[0]
        if len(ipaths) > 1:
            excludes = ipaths[1:]
            excludes_args = map(lambda x: ('--exclude', os.path.join(path, x)),
                    excludes)
            cmd.extend((chain(*excludes_args)))
        isrc = os.path.join(src, '.', path)
        idst = dst.rstrip(os.sep)
        cmd.extend((isrc, idst))
        with Popen(cmd, stdout=sys.stdout, stderr=sys.stderr) as proc:
            proc.wait()
            if proc.returncode:
                logging.error(
                        'rsync process `{0}` returned code {1}'.format(
                            ' '.join(cmd), proc.returncode))
            report.append((tuple(cmd), proc.returncode))

    return tuple(report)

def unison(profile, *paths, interface='text', opts=(), unison_path='unison'):
    cmd = [unison_path, profile, '-ui', interface]
    cmd.extend(opts)
    cmd.extend(chain(*map(lambda x: ('-path', x), paths)))
    logging.info(' '.join(cmd))
    with Popen(cmd, stdout=sys.stdout, stderr=sys.stderr) as proc:
        proc.wait()
        return proc.returncode

def is_filesystem_mounted(*, reobj=None, device='', mountdir=''):
    if reobj is None:
        if not (device or mountdir):
            raise ValueError('No pattern was provided')
        elif device and not mountdir:
            reobj = re.compile(r'.*{}.*'.format(device))
        elif mountdir and not device:
            reobj = re.compile(r'.*{}.*'.format(mountdir))
        else:
            reobj = re.compile(r'.*{}.*{}.*'.format(device, mountdir))
    with open('/proc/mounts') as mounts:
        return any(reobj.match(mount.strip()) for mount in mounts)

def randomize_basename(fname, ntries=16, basename_len=40, verbosity=0,
        fverbose=sys.stderr, preserve_ext=True):
    assert ntries > 0
    assert basename_len > 0

    itry = ntries
    dirname, basename_src = os.path.split(fname)
    fname_dst = fname

    while os.path.exists(fname_dst):
        if itry <= 0:
            msg = "Failed {} times to find an available basename".format(ntries)
            raise OSError(msg)

        basename_dst_woext = random_alphanumeric_str(basename_len)
        if preserve_ext:
            basename_src_woext, basename_src_ext = os.path.splitext(
                                                                   basename_src)
            basename_dst = basename_dst_woext + basename_src_ext
        else:
            basename_dst = basename_dst_woext

        fname_dst = os.path.join(dirname, basename_dst)
        itry -= 1

    shutil.move(fname, fname_dst)
    if verbosity:
        print('`{}` -> `{}`'.format(fname, fname_dst), file=fverbose)
