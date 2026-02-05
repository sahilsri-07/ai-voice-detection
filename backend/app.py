from fastapi import FastAPI, HTTPException, Header
from typing import Optional
import requests
import base64

from model import classifier
from config import API_KEY, ALLOWED_LANGUAGES

app = FastAPI()


def verify_api_key(x_api_key: Optional[str]):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.post("/api/detect")
def detect_voice(
    payload: dict,
    x_api_key: Optional[str] = Header(default=None, alias="x-api-key"),
):
    verify_api_key(x_api_key)

    # GUVI sends audio file URL
    audio_url = payload.get("audio_url") or payload.get("audioUrl")
    language = payload.get("language", "en")

    if not audio_url:
        raise HTTPException(status_code=400, detail="audio_url is required")

    if language not in ALLOWED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # Download audio file
    response = requests.get(audio_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Unable to fetch audio file")

    # Convert MP3 → Base64
    audio_base64 = base64.b64encode(response.content).decode("utf-8")

    # Run prediction
    label, confidence, detail = classifier.predict(
        audio_base64=audio_base64,
        language_code=language,
    )

    return {
        "result": label,
        "confidence": confidence,
        "language": ALLOWED_LANGUAGES[language],
        "detail": detail,
    }
