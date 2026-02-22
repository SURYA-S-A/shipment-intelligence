from typing import Optional
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from shipment_intelligence_api.core.constants import (
    EmbeddingProvider,
    Environment,
    LLMProvider,
    QdrantStoreMode,
    SparseEmbeddingProvider,
)


class Settings(BaseSettings):
    # Environment config
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # LLM config
    LLM_PROVIDER: LLMProvider
    LLM_MODEL: str
    LLM_API_KEY: Optional[str] = None

    # Embedding config
    EMBEDDING_PROVIDER: EmbeddingProvider
    EMBEDDING_MODEL: str
    EMBEDDING_API_KEY: Optional[str] = None

    # Sparse embedding config
    SPARSE_EMBEDDING_PROVIDER: SparseEmbeddingProvider
    SPARSE_EMBEDDING_MODEL: str

    # Qdrant store config
    QDRANT_MODE: QdrantStoreMode
    QDRANT_PATH: Optional[str] = None
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION: str

    model_config = SettingsConfigDict(
        env_file="../../.env", env_prefix="SHIPMENT_INTELLIGENCE_"
    )

    @model_validator(mode="after")
    def validate_vector_config(self):

        if self.QDRANT_MODE == QdrantStoreMode.LOCAL:
            if not self.QDRANT_PATH:
                raise ValueError(
                    f"QDRANT_PATH is required when QDRANT_MODE={QdrantStoreMode.LOCAL}"
                )

        if self.QDRANT_MODE == QdrantStoreMode.REMOTE:
            if not self.QDRANT_URL:
                raise ValueError(
                    f"QDRANT_URL is required when QDRANT_MODE={QdrantStoreMode.REMOTE}"
                )

            if not self.QDRANT_API_KEY:
                raise ValueError(
                    f"QDRANT_API_KEY is required when QDRANT_MODE={QdrantStoreMode.REMOTE}"
                )

        return self


settings = Settings()
