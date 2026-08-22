import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

from backend.app import load_lab_config


def test_load_lab_config_defaults():
    cfg = load_lab_config('filesystem')
    assert isinstance(cfg, dict)
    assert 'host' in cfg and 'user' in cfg and 'password' in cfg


def test_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv('LAB_FILESYSTEM_HOST', '1.2.3.4')
    monkeypatch.setenv('LAB_FILESYSTEM_USER', 'foo')
    monkeypatch.setenv('LAB_FILESYSTEM_PASSWORD', 'bar')
    monkeypatch.setenv('LAB_FILESYSTEM_SSH_KEY_PATH', 'C:\\fake\\id_rsa')
    cfg = load_lab_config('filesystem')
    assert cfg['host'] == '1.2.3.4'
    assert cfg['user'] == 'foo'
    assert cfg['password'] == 'bar'
    assert cfg.get('ssh_key_path') == 'C:\\fake\\id_rsa'
