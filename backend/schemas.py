from pydantic import BaseModel
from typing import Literal, Optional


class DetectionResponse(BaseModel):
    result: Literal["AI_GENERATED", "HUMAN"]
    confidence: float
    language: str
    detail: Optional[str] = None
