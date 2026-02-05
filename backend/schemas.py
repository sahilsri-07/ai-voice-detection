from pydantic import BaseModel, Field
from typing import Literal


class DetectionRequest(BaseModel):
    language: Literal["ta", "en", "hi", "ml", "te"]

    audio_format: Literal["mp3"] = Field(
        ...,
        alias="audioFormat",
        description="Audio format (mp3)"
    )

    audio_base64: str = Field(
        ...,
        alias="audioBase64",
        description="Base64-encoded MP3 audio"
    )

    class Config:
        populate_by_name = True


class DetectionResponse(BaseModel):
    result: Literal["AI_GENERATED", "HUMAN"]
    confidence: float
    language: str
    detail: str | None = None
