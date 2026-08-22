import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from backend.validator import validate_filesystem as vf


def fake_run_cmd(cmd):
    # Return outputs based on simple command matching used in validator
    if 'test -f /opt/rlp-labs/filesystem/README.txt' in cmd:
        return ('OK\n', '')
    if "stat -c '%U %a' /opt/rlp-labs/filesystem/README.txt" in cmd:
        return ('learner 644\n', '')
    if "stat -c '%a' /opt/rlp-labs/filesystem/README.txt" in cmd:
        return ('644\n', '')
    if "grep -q 'UUID=0000-0000' /etc/fstab" in cmd:
        return ('FOUND\n', '')
    if "grep -q '/mnt/broken' /etc/fstab" in cmd:
        return ('FOUND\n', '')
    if "mountpoint -q /mnt/broken" in cmd:
        return ('UNMOUNTED\n', '')
    if "getenforce" in cmd:
        return ('Enforcing\n', '')
    if "ls -Z /opt/rlp-labs/filesystem/README.txt" in cmd:
        return ('unconfined_u:object_r:default_t:s0 /opt/rlp-labs/filesystem/README.txt\n', '')
    if "find /opt/rlp-labs/filesystem ! -user learner -print -quit || true" in cmd:
        return ('\n', '')
    return ('', '')


def test_run_all_checks_with_mock(monkeypatch):
    monkeypatch.setattr(vf, 'run_cmd', fake_run_cmd)
    res = vf.run_all_checks()
    assert isinstance(res, dict)
    assert res['readme_present'] is True
    assert res['readme_owner_ok'] is True
    assert res['readme_perms_ok'] is True
    assert res['broken_fstab_present'] is True
    assert res['all_pass'] is True
    # hints dict should exist and be empty when all checks pass
    assert 'hints' in res
    assert isinstance(res['hints'], dict)
    assert res['hints'] == {}


def test_hints_present_on_failure(monkeypatch):
    # simulate missing README so hint should appear
    def fake_missing(cmd):
        if 'test -f /opt/rlp-labs/filesystem/README.txt' in cmd:
            return ('MISSING\n','')
        # other checks assume OK
        if "stat -c '%U %a' /opt/rlp-labs/filesystem/README.txt" in cmd:
            return ('learner 644\n', '')
        if "stat -c '%a' /opt/rlp-labs/filesystem/README.txt" in cmd:
            return ('644\n', '')
        if "grep -q 'UUID=0000-0000' /etc/fstab" in cmd:
            return ('FOUND\n', '')
        if "grep -q '/mnt/broken' /etc/fstab" in cmd:
            return ('FOUND\n', '')
        if "mountpoint -q /mnt/broken" in cmd:
            return ('UNMOUNTED\n', '')
        if "getenforce" in cmd:
            return ('Enforcing\n', '')
        if "ls -Z /opt/rlp-labs/filesystem/README.txt" in cmd:
            return ('unconfined_u:object_r:default_t:s0 /opt/rlp-labs/filesystem/README.txt\n', '')
        if "find /opt/rlp-labs/filesystem ! -user learner -print -quit || true" in cmd:
            return ('\n', '')
        return ('','')

    monkeypatch.setattr(vf, 'run_cmd', fake_missing)
    res = vf.run_all_checks()
    assert isinstance(res, dict)
    assert res['readme_present'] is False
    assert 'hints' in res
    assert 'readme_present' in res['hints']
    assert 'Create the README' in res['hints']['readme_present']
