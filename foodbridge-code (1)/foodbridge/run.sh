#!/usr/bin/env bash
# Local run: ./run.sh   ->  http://127.0.0.1:8000  (member app)   http://127.0.0.1:8000/staff/  (admin)
set -e
cd "$(dirname "$0")/backend"
[ -f .env ] || cp ../.env.example .env
python3 -m venv .venv 2>/dev/null || true
. .venv/bin/activate
pip install -q -r requirements.txt
set -a; . ./.env; set +a
exec uvicorn app.main:app --host 127.0.0.1 --port 8000
