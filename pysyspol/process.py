import re
import select
import sys
from logging import DEBUG, ERROR
from subprocess import Popen, PIPE
from itertools import chain
from os.path import join, exists
from os import getpid, remove

ANKI_DESKTOP_RE_PATTERN = r'.*python.*bin/anki'

def is_local_unix_process_active(reobj, ps_cmd=('ps', 'aux')):
    with Popen(ps_cmd, stdout=PIPE, stderr=PIPE,
            universal_newlines=True) as proc:
        matched_processes = [l for l in proc.stdout.read().splitlines()
                if reobj.match(l)]
    return len(matched_processes) > 0

def is_remote_unix_process_active(reobj, remote_id, ps_cmd=('ps', 'aux'),
        client_cmd=('ssh',)):
    popen_args = tuple(chain(client_cmd, (remote_id,), ps_cmd))
    with Popen(popen_args, stdout=PIPE, stderr=PIPE,
            universal_newlines=True) as proc:
        matched_processes = [l for l in proc.stdout.read().splitlines()
                if reobj.match(l)]
    return len(matched_processes) > 0

def is_local_anki_desktop_active(pattern=ANKI_DESKTOP_RE_PATTERN,
        ps_cmd=('ps', 'aux')):
    reobj = re.compile(pattern, re.IGNORECASE)
    return is_local_unix_process_active(reobj, ps_cmd)

def is_remote_ankidroid_active(hostname, user=None,
        pattern=r'.*com.ichi2.anki.*', ps_cmd=('ps',)):
    reobj = re.compile(pattern, re.IGNORECASE)
    remote_id = '@'.join([user, hostname]) if user else hostname
    return is_remote_unix_process_active(reobj, remote_id, ps_cmd)
is_remote_anki_desktop_active = (
    lambda hostname, username: is_remote_ankidroid_active(hostname,
        username, pattern=ANKI_DESKTOP_RE_PATTERN, ps_cmd=('ps', 'aux')))

def is_app_locked(root, name):
    lockf = join(root, 'var', 'lock', 'LCK..' + name)
    return lockf if exists(lockf) else False

def lock_app(root, name, lock=True):
    """Returns lock filepath if something was done, False otherwise"""
    lockf = join(root, 'var', 'lock', 'LCK..' + name)
    is_locked = is_app_locked(root, name)
    if lock and not is_locked:
        with open(lockf, 'w') as f:
            print(getpid(), file=f)
        return lockf
    if not lock and is_locked:
        remove(lockf)
        return lockf
    return False

def call(popenargs, logger, stdout_log_level=DEBUG, stderr_log_level=ERROR,
        sys_stderr=True, **kwargs):
    """
    Variant of subprocess.call that accepts a logger instead of stdout/stderr,
    and logs stdout messages via logger.debug and stderr messages via
    logger.error.

    Based on https://gist.github.com/bgreenlee/1402841
    """
    child = Popen(popenargs, stdout=PIPE, stderr=PIPE, **kwargs)

    log_level = {child.stdout: stdout_log_level,
                 child.stderr: stderr_log_level}

    def check_io():
        ready_to_read = select.select([child.stdout, child.stderr],
                [], [], 1000)[0]
        for io in ready_to_read:
            line = io.readline()
            linestr = line[:-1].decode('UTF-8')
            if not linestr:
                continue
            logger.log(log_level[io], linestr)
            if io is child.stderr and sys_stderr:
                print(linestr, file=sys.stderr)

    # keep checking stdout/stderr until the child exits
    while child.poll() is None:
        check_io()

    check_io()  # check again to catch anything after the process exits

    return child.wait()
