"""Speech-to-Text integration using Faster Whisper."""

from sage.config import get_settings

settings = get_settings()


class STTService:
    """Service for speech-to-text transcription."""

    def __init__(self):
        """Initialize STT service."""
        self.model_name = settings.whisper_model
        self.device = settings.whisper_device
        self.compute_type = settings.whisper_compute_type

    async def transcribe(self, audio_data: bytes) -> dict:
        """Transcribe audio to text."""
        # TODO: Implement actual Whisper integration
        return {
            "text": "Transcription placeholder",
            "language": "en",
        }
