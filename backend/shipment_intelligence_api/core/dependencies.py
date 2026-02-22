from functools import lru_cache
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from qdrant_client import QdrantClient

from shipment_intelligence_api.agents.analysis_agent.agent import ShipmentAnalysisAgent
from shipment_intelligence_api.agents.escalation_agent.agent import EscalationAgent
from shipment_intelligence_api.agents.orchestrator.workflow import (
    ShipmentIntelligenceOrchestrator,
)
from shipment_intelligence_api.agents.response_agent.agent import ShipmentResponseAgent
from shipment_intelligence_api.agents.retrieval_agent.agent import (
    ShipmentRetrievalAgent,
)
from shipment_intelligence_api.agents.service import ShipmentIntelligenceAgentService
from shipment_intelligence_api.infrastructure.embeddings.embedding_provider import (
    get_embeddings,
    get_sparse_embeddings,
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
from langchain_qdrant import FastEmbedSparse


@lru_cache()
def get_llm_instance() -> BaseChatModel:
    """Get cached LLM instance."""
    return get_llm()


@lru_cache()
def get_embeddings_instance() -> Embeddings:
    """Get cached embeddings instance."""
    return get_embeddings()


@lru_cache()
def get_sparse_embeddings_instance() -> FastEmbedSparse:
    """Get cached sparse embeddings instance."""
    return get_sparse_embeddings()


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
        sparse_embeddings=get_sparse_embeddings_instance(),
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


@lru_cache()
def get_retrieval_agent() -> ShipmentRetrievalAgent:
    """Get cached retrieval agent."""
    return ShipmentRetrievalAgent(
        llm=get_llm_instance(),
        qdrant_store_manager=get_qdrant_store_manager_instance(),
    )


@lru_cache()
def get_analysis_agent() -> ShipmentAnalysisAgent:
    """Get cached analysis agent."""
    return ShipmentAnalysisAgent(llm=get_llm_instance())


@lru_cache()
def get_response_agent() -> ShipmentResponseAgent:
    """Get cached response agent."""
    return ShipmentResponseAgent(llm=get_llm_instance())


@lru_cache()
def get_escalation_agent() -> EscalationAgent:
    """Get cached escalation agent."""
    return EscalationAgent(llm=get_llm_instance())


@lru_cache()
def get_orchestrator() -> ShipmentIntelligenceOrchestrator:
    """Get cached orchestrator with all agents."""
    return ShipmentIntelligenceOrchestrator(
        retrieval_agent=get_retrieval_agent(),
        analysis_agent=get_analysis_agent(),
        response_agent=get_response_agent(),
        escalation_agent=get_escalation_agent(),
    )


@lru_cache()
def get_agent_service() -> ShipmentIntelligenceAgentService:
    return ShipmentIntelligenceAgentService(orchestrator=get_orchestrator())
