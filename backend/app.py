from fastapi import FastAPI, Request, HTTPException

from model import classifier
from config import ALLOWED_LANGUAGES

app = FastAPI()


@app.post("/api/detect")
async def detect_voice(request: Request):
    body = await request.json()

    # Accept ALL possible key styles
    language = body.get("language")
    audio_base64 = (
        body.get("audioBase64")
        or body.get("audio_base64")
    )
    audio_format = (
        body.get("audioFormat")
        or body.get("audio_format")
    )

    if not language or not audio_base64 or not audio_format:
        raise HTTPException(
            status_code=400,
            detail="Required fields: language, audioFormat, audioBase64",
        )

    if language not in ALLOWED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

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
