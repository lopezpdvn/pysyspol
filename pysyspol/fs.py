import sys
import os
import logging
from itertools import chain
from subprocess import Popen

def rsync_multiple(src, dst, opts, *paths, rsync_path='rsync'):
    report = []
    for ipaths in paths:
        cmd = [rsync_path]
        cmd.extend(opts)
        path = ipaths[0]
        if len(ipaths) > 1:
            excludes = ipaths[1:]
            excludes_args = map(lambda x: ('--exclude', os.sep + x), excludes)
            cmd.extend((chain(*excludes_args)))
        isrc = os.path.join(src, path)
        if path.endswith(os.sep):
            idst = os.path.join(dst, path).rstrip(os.sep)
        else:
            idst = os.path.join(dst, os.path.split(path)[0])
        cmd.extend((isrc, idst))

        with Popen(cmd, stdout=sys.stdout, stderr=sys.stderr) as proc:
            proc.wait()
            if proc.returncode:
                logging.error(
                        'rsync proccess `{0}` returned code {1}'.format(
                            ' '.join(cmd), proc.returncode))
            report.append((tuple(cmd), proc.returncode))

    return tuple(report)
