from pydantic import BaseModel, Field
from typing import Literal, Optional


class DetectionRequest(BaseModel):
    # Accepts "audio_base64_format" from GUVI form
    audio_base64: str = Field(
        ...,
        alias="audio_base64_format",
        description="Base64-encoded MP3 audio"
    )

    language: Literal["ta", "en", "hi", "ml", "te"] = Field(
        ...,
        description="Language code: ta/en/hi/ml/te"
    )

    class Config:
        populate_by_name = True


class DetectionResponse(BaseModel):
    result: Literal["AI_GENERATED", "HUMAN"]
    confidence: float = Field(ge=0.0, le=1.0)
    language: str
    detail: Optional[str] = None
