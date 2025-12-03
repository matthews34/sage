"""LLM integration using Ollama."""

from sage.config import get_settings

settings = get_settings()


class LLMService:
    """Service for interacting with Ollama LLM."""

    def __init__(self):
        """Initialize LLM service."""
        self.host = settings.ollama_host
        self.default_model = settings.ollama_model

    async def generate(self, prompt: str, model: str | None = None) -> str:
        """Generate text completion using LLM."""
        # TODO: Implement actual Ollama integration
        return f"LLM response placeholder for prompt: {prompt}"
