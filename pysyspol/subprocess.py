from subprocess import Popen, PIPE

def is_local_unix_process_active(pattern, psCommand=('ps', 'aux')):
    with Popen(psCommand, stdout=PIPE, stderr=PIPE,
            universal_newlines=True) as proc:
        matched_processes = [l for l in proc.stdout.read().splitlines()
                if pattern.match(l)]
    return len(matched_processes) > 0
