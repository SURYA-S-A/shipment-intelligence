from shipment_intelligence_api.infrastructure.vector_store.qdrant_store_manager import (
    QdrantVectorStoreManager,
)
from shipment_intelligence_api.rag.pipeline import ShipmentRAGPipeline
from shipment_intelligence_api.rag.schema import (
    IncomingCommunicationRequest,
    ShipmentRAGRequest,
    ShipmentRAGResponse,
)
from langchain_core.documents import Document


class ShipmentRAGService:
    """Service for shipment event ingestion and RAG queries."""

    def __init__(
        self,
        pipeline: ShipmentRAGPipeline,
        qdrant_store_manager: QdrantVectorStoreManager,
    ) -> None:
        """Initialize shipment RAG service.

        Args:
            pipeline: RAG pipeline for query processing.
            qdrant_store_manager: Manager for qdrant vector store operations.
        """
        self.pipeline = pipeline
        self.qdrant_store_manager = qdrant_store_manager

    def ingest_event(self, request: IncomingCommunicationRequest) -> dict:
        """Ingest a shipment event into the vector store.
        This can be an email, SMS, or call transcript related to a shipment.
        The service extracts the shipment ID from the content and stores the event as a document in the qdrant vector store for later retrieval during RAG queries.

        Args:
            request: Shipment event data to ingest.

        Returns:
            Dict with status message.
        """
        doc = Document(
            page_content=request.content,
            metadata={
                "shipment_id": request.shipment_id,
                # "event_type": request.event_type,
                "channel": request.channel,
                "source": request.source,
                "timestamp": request.timestamp,
            },
        )

        self.qdrant_store_manager.add_documents(docs=[doc])

        return {
            "status": "event ingested successfully",
            "shipment_id": request.shipment_id,
        }

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
