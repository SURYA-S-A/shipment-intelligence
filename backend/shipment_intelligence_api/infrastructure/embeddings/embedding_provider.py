from shipment_intelligence_api.core.constants import EmbeddingProvider
from shipment_intelligence_api.core.settings import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.embeddings import Embeddings


def get_embeddings() -> Embeddings:
    """Get configured embeddings model.

    Returns:
        Embeddings: Initialized embedding model.

    Raises:
        ValueError: If unsupported embedding provider is configured.
    """
    if settings.EMBEDDING_PROVIDER == EmbeddingProvider.GOOGLE_GENAI:
        return GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.EMBEDDING_API_KEY,
        )

    raise ValueError(f"Unsupported embedding provider: {settings.EMBEDDING_PROVIDER}")
