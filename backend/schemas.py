from pydantic import BaseModel, Field
from typing import Literal


class DetectionRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64-encoded MP3 audio")
    language: Literal["ta", "en", "hi", "ml", "te"] = Field(
        ..., description="Language code: ta/en/hi/ml/te"
    )


class DetectionResponse(BaseModel):
    result: Literal["AI_GENERATED", "HUMAN"]
    confidence: float = Field(ge=0.0, le=1.0)
    language: str
    detail: str | None = None