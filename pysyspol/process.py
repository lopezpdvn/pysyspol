from subprocess import Popen, PIPE
from itertools import chain

def is_local_unix_process_active(pattern, ps_cmd=('ps', 'aux')):
    with Popen(ps_cmd, stdout=PIPE, stderr=PIPE,
            universal_newlines=True) as proc:
        matched_processes = [l for l in proc.stdout.read().splitlines()
                if pattern.match(l)]
    return len(matched_processes) > 0

def is_remote_unix_process_active(pattern, remote_id, ps_cmd=('ps', 'aux'),
        client_cmd=('ssh',)):
    popen_args = tuple(chain(client_cmd, (remote_id,), ps_cmd))
    with Popen(popen_args, stdout=PIPE, stderr=PIPE,
            universal_newlines=True) as proc:
        matched_processes = [l for l in proc.stdout.read().splitlines()
                if pattern.match(l)]
    return len(matched_processes) > 0
