Write-Host "Starting backend (FastAPI) on localhost:8000"
$env:PYTHONUNBUFFERED = 1
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
