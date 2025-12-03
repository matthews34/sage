"""Text embeddings using Sentence Transformers."""

from sage.config import get_settings

settings = get_settings()


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self):
        """Initialize embedding service."""
        self.model_name = settings.embedding_model
        self.device = settings.embedding_device

    async def embed(self, text: str) -> list[float]:
        """Generate embeddings for text."""
        # TODO: Implement actual embedding generation
        return [0.0] * 384  # Placeholder embedding
