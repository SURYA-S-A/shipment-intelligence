from enum import Enum


class LLMProvider(str, Enum):
    """Enum for supported LLM providers."""

    OPENAI = "openai"
    GOOGLE_GENAI = "google_genai"


class EmbeddingProvider(str, Enum):
    """Enum for supported embedding providers."""

    OPENAI = "openai"
    GOOGLE_GENAI = "google_genai"


class SparseEmbeddingProvider(str, Enum):
    FASTEMBED = "fastembed"


class QdrantStoreMode(str, Enum):
    """Enum for Qdrant vector store operation modes."""

    LOCAL = "local"
    REMOTE = "remote"


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
