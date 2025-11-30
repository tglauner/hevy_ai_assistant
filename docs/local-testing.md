# Local testing on macOS

## Prerequisites
- Docker Desktop for Mac (for n8n + backend via `docker-compose`).
- Python 3.11 (if you prefer running the backend without Docker).
- Node 18+ (optional, if you wire a frontend to the backend endpoints).

## Quick start (Docker Compose)
1. Copy env vars:
   ```bash
   cp backend/.env.example .env
   ```
2. Start services:
   ```bash
   docker compose up --build
   ```
3. Open n8n UI at http://localhost:5678 and import `n8n/workflows/hevy_gpt_workflow.json`.
4. Test the backend health:
   ```bash
   curl http://localhost:8000/health
   ```
5. Hit recommendation webhook (n8n will receive the payload and fan out):
   ```bash
   curl -X POST http://localhost:8000/api/recommendations \
     -H "Content-Type: application/json" \
     -d '{
       "context": {"user_id": "abc123", "equipment": ["barbell"], "goals": "hypertrophy"},
       "recent_sessions": [{"date": "2024-05-01", "movements": ["squat", "bench"]}]
     }'
   ```

## Running FastAPI locally (no Docker)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Notes for iMacs
- Apple Silicon works well with Docker Desktop; ensure you enable "Use Virtualization Framework".
- If port 5678 is occupied, override with `WEBHOOK_URL` and `N8N_PORT` in `.env` and `docker-compose.yml`.
- For HTTPS tunneling (to expose webhooks), use `cloudflared tunnel` or `ngrok` pointing to port 5678.
