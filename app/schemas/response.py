from pydantic import BaseModel
from typing import List


class Segment(BaseModel):
    text: str


class TranslationResponse(BaseModel):
    detected_language: str
    transcription: List[Segment]
    translation: str
