from fastapi import APIRouter, Depends
from shipment_intelligence_api.rag.schema import (
    ShipmentEventRequest,
    ShipmentRAGRequest,
    ShipmentRAGResponse,
)
from shipment_intelligence_api.rag.service import ShipmentRAGService
from shipment_intelligence_api.core.dependencies import get_rag_service

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post(
    "/ingest-event",
    summary="Ingest Shipment Event",
    description=(
        "The event may contain structured or unstructured operational data "
        "such as emails, status updates, or delay notifications."
    ),
)
def ingest_event(
    request: ShipmentEventRequest,
    rag_service: ShipmentRAGService = Depends(get_rag_service),
):
    """Store a shipment event in the vector database.

    Args:
        request: Shipment event payload.
        rag_service: Injected RAG service.

    Returns: A confirmation response indicating successful ingestion.
    """
    return rag_service.ingest_event(request)


@router.post(
    "/query",
    summary="Investigate Shipment",
    description=(
        "Perform shipment investigation using RAG-based contextual retrieval. "
    ),
    response_model=ShipmentRAGResponse,
)
def query_shipment(
    request: ShipmentRAGRequest,
    rag_service: ShipmentRAGService = Depends(get_rag_service),
):
    """Retrieves shipment-related events from the vector store.

    Args:
        request: Query payload.
        rag_service: Injected RAG service.

    Returns: Structured response containing answers,
    """
    return rag_service.run(request)
