"""Text-to-Speech endpoints."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()


class TTSRequest(BaseModel):
    """TTS request model."""

    text: str
    voice: str | None = None
    speed: float = 1.0


@router.post("/synthesize")
async def synthesize_speech(request: TTSRequest):
    """Synthesize speech from text."""
    # TODO: Implement actual TTS integration
    # For now, return a placeholder response
    return {
        "message": "TTS integration pending",
        "text": request.text,
    }
