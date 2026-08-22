# Backend — FastAPI orchestration

Endpoints:

- `GET /api/status` — returns raw `vagrant status` output for the lab
- `POST /api/start` — starts `vagrant up` in the lab directory (background thread)
- `POST /api/validate` — runs the `backend/validator/validate_filesystem.py` script and returns stdout/stderr
- WebSocket `/ws/terminal` — connects to the lab VM via SSH and proxies a shell to the browser (query params: `host`, `user`, `password`)
- Snapshot endpoints: `POST /api/snapshot/save`, `POST /api/snapshot/restore`, `GET /api/snapshot/list`, `POST /api/snapshot/delete` (all accept JSON body `{ "name": "snapshot-name" }` for POSTs)

Run locally:

```powershell
# Install deps (prefer a venv)
pip install -r requirements.txt

# Copy the example env and edit as needed
copy .env.example .env

# Start the backend (reloads on change)
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Security:

- The dev setup reads `labs/<lab>/config.json` which may contain credentials. Add those files to `.gitignore` and avoid committing secrets.
- Prefer using the `.env` file (copy from `.env.example`) or CI secrets. The backend will prefer environment variables `LAB_<LAB>_HOST`, `LAB_<LAB>_USER`, and `LAB_<LAB>_PASSWORD` before falling back to `labs/<lab>/config.json`.

- SSH key auth: you may set `LAB_FILESYSTEM_SSH_KEY_PATH` in `.env` to point to a private key on the host; the backend and validator will prefer key-based auth when configured. For local VM provisioning, place the public key at `labs/filesystem/learner_id_rsa.pub` so the provisioning script installs it into `learner`'s `authorized_keys`.

CI guidance:

- Do not commit `.env` to the repository. In CI, set `LAB_FILESYSTEM_HOST`, `LAB_FILESYSTEM_USER`, and `LAB_FILESYSTEM_PASSWORD` as repository secrets and expose them to the workflow when needed.

Example quick-check (local):

```powershell
# Start the backend as above, then in a separate shell run the validator against the host configured in .env
python "backend\validator\validate_filesystem.py"
```

Validator notes:

- The validator SSHes into the lab VM configured via `.env` or `labs/filesystem/config.json`.
- Running `pytest` will exercise config-loading tests, but the filesystem validator tests will attempt to reach the configured VM — run them locally after `vagrant up`.
 - The backend `/api/validate` endpoint now calls the validator module directly and returns structured JSON. The frontend consumes that JSON and renders pass/fail results.
