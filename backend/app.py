from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from config import API_KEY, ALLOWED_LANGUAGES
from schemas import DetectionResponse
from model import classifier
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI-Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or spoken by a human.",
    version="1.0.0",
)

# CORS (open for hackathon)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- UPDATED REQUEST SCHEMA ----------
class DetectionRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: Optional[str] = None
    audio_base64_format: Optional[str] = None  # GUVI field

# ---------- API KEY CHECK ----------
def verify_api_key(x_api_key: Optional[str]) -> None:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

# ---------- HEALTH CHECK ----------
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------- DETECTION ENDPOINT ----------
@app.post("/api/detect", response_model=DetectionResponse)
def detect_voice(
    payload: DetectionRequest,
    x_api_key: Optional[str] = Header(default=None, alias="x-api-key"),
):
    verify_api_key(x_api_key)

    if payload.language not in ALLOWED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # Accept BOTH field names safely
    audio_b64 = payload.audio_base64 or payload.audio_base64_format
    if not audio_b64:
        raise HTTPException(status_code=422, detail="audio_base64 missing")

    label, confidence, detail = classifier.predict(
        audio_base64=audio_b64,
        language_code=payload.language,
    )

    return DetectionResponse(
        result=label,
        confidence=confidence,
        language=ALLOWED_LANGUAGES[payload.language],
        detail=detail,
    )
