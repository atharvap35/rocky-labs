import os, sys
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)
from backend.validator import validate_filesystem as vf

# Mocked outputs for each command
responses = {
    "test -f /opt/rlp-labs/filesystem/README.txt": ('OK\n',''),
    "stat -c '%U %a' /opt/rlp-labs/filesystem/README.txt": ('learner 644\n',''),
    "stat -c '%a' /opt/rlp-labs/filesystem/README.txt": ('644\n',''),
    "grep -q 'UUID=0000-0000' /etc/fstab": ('FOUND\n',''),
    "grep -q '/mnt/broken' /etc/fstab": ('FOUND\n',''),
    "mountpoint -q /mnt/broken": ('UNMOUNTED\n',''),
    "getenforce": ('Enforcing\n',''),
    "ls -Z /opt/rlp-labs/filesystem/README.txt": ('unconfined_u:object_r:default_t:s0 /opt/rlp-labs/filesystem/README.txt\n',''),
    "find /opt/rlp-labs/filesystem ! -user learner -print -quit || true": ('\n',''),
}


def fake_run_cmd(cmd):
    for k,v in responses.items():
        if k in cmd:
            return v
    return ('','')

vf.run_cmd = fake_run_cmd
res = vf.run_all_checks()
print(res)
