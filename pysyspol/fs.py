import sys
import os
import logging
import re
from itertools import chain
from subprocess import Popen

def rsync_multiple(src, dst, opts, *paths, rsync_path='rsync'):
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
                        'rsync proccess `{0}` returned code {1}'.format(
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
        pattern = r'{}.*{}' if device and mountdir else r'{}'
        reobj = re.compile(pattern.format(device, mountdir))
    with open('/proc/mounts') as mounts:
        return any(reobj.match(mount.strip()) for mount in mounts)
