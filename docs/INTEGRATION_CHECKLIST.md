Integration smoke checklist
==========================

Use this checklist to validate the end-to-end MVP locally (Windows host).

Prereqs
-------

- VirtualBox
- Vagrant
- Python 3.11
- `pip install -r requirements.txt`

Steps
-----

1. Copy `.env.example` to `.env` and update `LAB_FILESYSTEM_SSH_KEY_PATH` if you want key-based auth.
2. If using key auth, generate a key pair on the host and place the public key at `labs/filesystem/learner_id_rsa.pub`.
3. Start the backend:

```powershell
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

4. From a separate shell, bring up the VM:

```powershell
cd labs\filesystem
vagrant up
```

5. Verify `vagrant ssh` can connect, or use the frontend to open the terminal at `http://127.0.0.1:8000/static/index.html`.
6. Run the validator locally to ensure it can SSH to the VM:

```powershell
python backend\validator\validate_filesystem.py
```

7. Test snapshot save/restore via API (or UI) and verify the VM state is restored.

Notes
-----
- If using password-based auth, ensure `LAB_FILESYSTEM_PASSWORD` in `.env` matches the learner password (provisioner sets it to `learner` by default unless locked by key install).
- For production or shared deployments, use vaulting/secret management instead of plaintext `.env` files.
