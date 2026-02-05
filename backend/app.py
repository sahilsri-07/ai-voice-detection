from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import Header, HTTPException

from config import API_KEY, ALLOWED_LANGUAGES
from schemas import DetectionRequest, DetectionResponse
from model import classifier

app = FastAPI(
    title="AI-Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or spoken by a human.",
    version="1.0.0",
)

# Allow local frontend / others
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon/testing; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(x_api_key: Optional[str]) -> None:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/detect", response_model=DetectionResponse)
def detect_voice(
    payload: DetectionRequest,
    x_api_key: Optional[str] = Header(default=None, alias="x-api-key"),
):
    verify_api_key(x_api_key)

    if payload.language not in ALLOWED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language code")

    label, confidence, detail = classifier.predict(
        audio_base64=payload.audio_base64,
        language_code=payload.language,
    )

    return DetectionResponse(
        result=label,
        confidence=confidence,
        language=ALLOWED_LANGUAGES[payload.language],
        detail=detail,
    )