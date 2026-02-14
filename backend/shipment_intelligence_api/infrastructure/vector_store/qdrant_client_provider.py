from qdrant_client import QdrantClient
from shipment_intelligence_api.core.constants import QdrantStoreMode
from shipment_intelligence_api.core.settings import settings


def get_qdrant_client() -> QdrantClient:
    """Create and return configured Qdrant client based on environment settings.

    Supports both local (disk-based) and remote (cloud/server) modes.

    Returns:
        QdrantClient: Configured Qdrant client instance.

    Raises:
        ValueError: If QDRANT_MODE is not LOCAL or REMOTE.
    """
    if settings.QDRANT_MODE == QdrantStoreMode.LOCAL:
        return QdrantClient(path=settings.QDRANT_PATH)

    if settings.QDRANT_MODE == QdrantStoreMode.REMOTE:
        return QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

    raise ValueError(
        f"Invalid QDRANT_MODE: {settings.QDRANT_MODE}. "
        f"Must be '{QdrantStoreMode.LOCAL}' or '{QdrantStoreMode.REMOTE}'."
    )
