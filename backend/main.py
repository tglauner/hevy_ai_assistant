import hmac
import hashlib
import json
import os
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


class UserContext(BaseModel):
    user_id: str = Field(..., description="Hevy user id")
    equipment: Optional[list[str]] = Field(default=None, description="Available equipment")
    goals: Optional[str] = Field(default=None, description="User goal description")
    constraints: Optional[str] = Field(default=None, description="Injuries, time limits, etc")


class RecommendationRequest(BaseModel):
    context: UserContext
    recent_sessions: Optional[list[dict]] = Field(default=None, description="Lightweight workout history")


class Routine(BaseModel):
    day: str
    exercises: list[dict]
    notes: Optional[str] = None


class RoutineRequest(BaseModel):
    context: UserContext
    routine: Routine


class RoutineUpdateRequest(BaseModel):
    context: UserContext
    routine_id: str
    routine: Routine


class WebhookResponse(BaseModel):
    workflow_run_id: str
    status: str
    summary: Optional[str] = None
    routine_preview: Optional[dict] = None


def get_env(key: str, default: Optional[str] = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(f"Environment variable {key} is required")
    return value


def sign_payload(secret: str, payload: bytes) -> str:
    signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return signature


app = FastAPI(title="Hevy AI Assistant", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


async def post_to_n8n(path: str, payload: dict) -> WebhookResponse:
    n8n_url = get_env("N8N_WEBHOOK_URL")
    secret = get_env("N8N_WEBHOOK_SECRET", "")

    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    headers = {}
    if secret:
        headers["X-Signature"] = sign_payload(secret, body)

    url = f"{n8n_url.rstrip('/')}/{path.lstrip('/')}"
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(url, content=body, headers=headers)
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail=response.text)
        try:
            data = response.json()
        except Exception:
            raise HTTPException(status_code=502, detail="Invalid response from workflow")
    return WebhookResponse(**data)


@app.post("/api/recommendations", response_model=WebhookResponse)
async def recommend(req: RecommendationRequest):
    payload = req.model_dump()
    return await post_to_n8n("webhook/hevy/recommendations", payload)


@app.post("/api/routines/new", response_model=WebhookResponse)
async def create_routine(req: RoutineRequest):
    payload = req.model_dump()
    return await post_to_n8n("webhook/hevy/routines/new", payload)


@app.post("/api/routines/update", response_model=WebhookResponse)
async def update_routine(req: RoutineUpdateRequest):
    payload = req.model_dump()
    return await post_to_n8n("webhook/hevy/routines/update", payload)


@app.post("/webhooks/n8n", response_model=WebhookResponse)
async def n8n_callback(
    payload: WebhookResponse,
    x_signature: Optional[str] = Header(default=None, convert_underscores=False),
):
    secret = get_env("N8N_CALLBACK_SECRET", "")
    if secret:
        raw_body = payload.model_dump_json().encode()
        expected_sig = sign_payload(secret, raw_body)
        if not hmac.compare_digest(expected_sig, x_signature or ""):
            raise HTTPException(status_code=401, detail="Invalid signature")
    return payload


# Example local runner: `uvicorn main:app --reload --port 8000`
