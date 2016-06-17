import sys
import os
import logging
from itertools import chain
from subprocess import Popen, PIPE

def rsync(src, dst, opts, *dirs, rsync_path='rsync'):
    if dirs:
        report = []
        for idir in dirs:
            cmd = [rsync_path]
            cmd.extend(opts)
            idir = [f.rstrip(os.sep) for f in idir]
            if len(idir) > 1:
                exclude = idir[1:]
                exclude_args = map(lambda x: ('--exclude', os.sep + x), exclude)
                cmd.extend((chain(*exclude_args)))
            isrc = os.path.join(src, idir[0]) + os.sep
            idst = os.path.join(dst, idir[0])
            cmd.extend((isrc, idst))

            with Popen(cmd, stdout=sys.stdout, stderr=sys.stderr) as proc:
                proc.wait()
                if proc.returncode:
                    logging.warning(
                            'rsync proccess `{0}` returned code {1}'.format(
                                cmd, proc.returncode))
                report.append([cmd, proc.returncode])
        return report
