from shipment_intelligence_api.infrastructure.vector_store.qdrant_store_manager import (
    QdrantVectorStoreManager,
)
from shipment_intelligence_api.rag.pipeline import ShipmentRAGPipeline
from shipment_intelligence_api.rag.schema import (
    ShipmentEventRequest,
    ShipmentRAGRequest,
    ShipmentRAGResponse,
)
from langchain_core.documents import Document


class ShipmentRAGService:
    """Service for shipment event ingestion and RAG queries."""

    def __init__(
        self, pipeline: ShipmentRAGPipeline, qdrant_store_manager: QdrantVectorStoreManager
    ) -> None:
        """Initialize shipment RAG service.

        Args:
            pipeline: RAG pipeline for query processing.
            qdrant_store_manager: Manager for qdrant vector store operations.
        """
        self.pipeline = pipeline
        self.qdrant_store_manager = qdrant_store_manager

    def ingest_event(self, request: ShipmentEventRequest) -> dict:
        """Ingest a shipment event into the vector store.

        Args:
            request: Shipment event data to ingest.

        Returns:
            Dict with status message.
        """
        doc = Document(
            page_content=request.description,
            metadata={
                "shipment_id": request.shipment_id,
                "event_type": request.event_type,
                "source": request.source,
                "timestamp": request.timestamp,
            },
        )

        self.qdrant_store_manager.add_documents(docs=[doc])

        return {"status": "event ingested successfully"}

    def run(self, request: ShipmentRAGRequest) -> ShipmentRAGResponse:
        """Execute RAG query for shipment intelligence.

        Args:
            request: RAG query request containing shipment_id and question.

        Returns:
            ShipmentRAGResponse with answer and context documents.
        """
        result = self.pipeline.run(
            shipment_id=request.shipment_id, question=request.question
        )

        return ShipmentRAGResponse(
            answer=result["answer"], context=result.get("context")
        )
