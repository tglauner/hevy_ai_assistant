# Hevy AI Assistant

AI assistant that creates and assesses routines/workouts on Hevy using GPT 5.1 and n8n automation.

## What you get
- **FastAPI backend** that relays requests to n8n webhooks and returns workflow results.
- **n8n workflow export** (`n8n/workflows/hevy_gpt_workflow.json`) covering webhook trigger → GPT suggestion → Hevy routine creation → backend callback.
- **Docker Compose** for backend + n8n (+ Redis for caching/queueing if you expand).
- **Local testing guide** (`docs/local-testing.md`) tailored to macOS/iMac.

## Quick start
1. Copy env template and run compose:
   ```bash
   cp backend/.env.example .env
   docker compose up --build
   ```
2. Open n8n at http://localhost:5678 (basic auth defaults to admin/admin). Import `n8n/workflows/hevy_gpt_workflow.json`.
3. Test the backend health:
   ```bash
   curl http://localhost:8000/health
   ```
4. Send a recommendation request (flows into n8n → GPT → Hevy):
   ```bash
   curl -X POST http://localhost:8000/api/recommendations \
     -H "Content-Type: application/json" \
     -d '{
       "context": {"user_id": "abc123", "equipment": ["barbell"], "goals": "hypertrophy"},
       "recent_sessions": [{"date": "2024-05-01", "movements": ["squat", "bench"]}]
     }'
   ```

## n8n integration tips
- Create credentials:
  - **OpenAI** (GPT 5.1) for the `GPT:Suggest` node.
  - **Generic HTTP** for Hevy API calls with your Hevy token.
  - Optional **Generic HTTP** for the backend callback (or leave default).
- The exported workflow enforces a JSON shape for routines and validates presence of `exercises`.
- Add a second webhook path (e.g., `hevy/routines/new`) by duplicating the trigger node and linking to the same GPT + validation path.

## Extending
- Map exercise names to Hevy exercise IDs in the `Code:Validate` node before the POST.
- Add retries/backoff around the Hevy HTTP node and handle 429s.
- Wire Slack/Email nodes after `Callback:Backend` to notify users with summaries.

## Dev notes
- Backend entrypoint: `backend/main.py` (run with `uvicorn main:app --reload --port 8000`).
- Dependencies: `backend/requirements.txt`.
- Docker build: `backend/Dockerfile`.
- Mac/iMac specifics and curl snippets: `docs/local-testing.md`.
