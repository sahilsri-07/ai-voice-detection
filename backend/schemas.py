from pydantic import BaseModel, Field
from typing import Literal


class DetectionRequest(BaseModel):
    language: Literal["ta", "en", "hi", "ml", "te"] = Field(
        ..., description="Language code: ta/en/hi/ml/te"
    )

    audio_format: Literal["mp3"] = Field(
        ..., description="Audio format (mp3)"
    )

    audio_base64: str = Field(
        ..., description="Base64-encoded MP3 audio"
    )


class DetectionResponse(BaseModel):
    result: Literal["AI_GENERATED", "HUMAN"]
    confidence: float = Field(ge=0.0, le=1.0)
    language: str
    detail: str | None = None
