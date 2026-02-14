from functools import lru_cache
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from qdrant_client import QdrantClient

from shipment_intelligence_api.infrastructure.embeddings.embedding_provider import (
    get_embeddings,
)
from shipment_intelligence_api.infrastructure.llm.llm_provider import get_llm
from shipment_intelligence_api.infrastructure.vector_store.qdrant_client_provider import (
    get_qdrant_client,
)
from shipment_intelligence_api.infrastructure.vector_store.qdrant_store_manager import (
    QdrantVectorStoreManager,
)
from shipment_intelligence_api.rag.pipeline import ShipmentRAGPipeline
from shipment_intelligence_api.rag.service import ShipmentRAGService


@lru_cache()
def get_llm_instance() -> BaseChatModel:
    """Get cached LLM instance."""
    return get_llm()


@lru_cache()
def get_embeddings_instance() -> Embeddings:
    """Get cached embeddings instance."""
    return get_embeddings()


@lru_cache()
def get_qdrant_client_instance() -> QdrantClient:
    """Get cached Qdrant client."""
    return get_qdrant_client()


@lru_cache()
def get_qdrant_store_manager_instance() -> QdrantVectorStoreManager:
    """Get cached vector store manager."""
    manager = QdrantVectorStoreManager(
        client=get_qdrant_client_instance(),
        embeddings=get_embeddings_instance(),
    )
    manager.init_collection()
    return manager


@lru_cache()
def get_rag_pipeline() -> ShipmentRAGPipeline:
    """Get cached RAG pipeline."""
    return ShipmentRAGPipeline(
        llm=get_llm_instance(),
        qdrant_store_manager=get_qdrant_store_manager_instance(),
    )


@lru_cache()
def get_rag_service() -> ShipmentRAGService:
    """Get cached RAG service."""
    return ShipmentRAGService(
        pipeline=get_rag_pipeline(),
        qdrant_store_manager=get_qdrant_store_manager_instance(),
    )
