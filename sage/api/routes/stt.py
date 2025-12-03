"""Speech-to-Text endpoints."""

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

router = APIRouter()


class TranscriptionResponse(BaseModel):
    """Transcription response model."""

    text: str
    language: str | None = None
    duration: float | None = None


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe audio file to text."""
    # TODO: Implement actual STT integration
    return TranscriptionResponse(
        text="This is a placeholder transcription. STT integration pending.",
        language="en",
    )
