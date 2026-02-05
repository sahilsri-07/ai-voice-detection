from fastapi import FastAPI, Request, HTTPException
from typing import Optional

from model import classifier
from config import ALLOWED_LANGUAGES

app = FastAPI()

# 🔐 Hardcoded key for hackathon
VALID_API_KEY = "hackathon-secret-key"


def extract_api_key(request: Request) -> Optional[str]:
    headers = request.headers

    return (
        headers.get("x-api-key")
        or headers.get("X-API-KEY")
        or headers.get("authorization")
        or headers.get("Authorization")
    )


@app.post("/api/detect")
async def detect_voice(request: Request):
    api_key = extract_api_key(request)

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    # If Authorization: Bearer xxx
    if api_key.startswith("Bearer "):
        api_key = api_key.replace("Bearer ", "").strip()

    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    body = await request.json()

    language = body.get("language")
    audio_base64 = body.get("audioBase64") or body.get("audio_base64")
    audio_format = body.get("audioFormat") or body.get("audio_format")

    if not language or not audio_base64 or not audio_format:
        raise HTTPException(
            status_code=422,
            detail="Missing fields: language, audioFormat, audioBase64",
        )

    if language not in ALLOWED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

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
