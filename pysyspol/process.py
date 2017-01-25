import re
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
