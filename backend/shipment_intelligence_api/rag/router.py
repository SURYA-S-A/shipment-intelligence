from fastapi import APIRouter, Depends
from shipment_intelligence_api.rag.schema import (
    ShipmentRAGRequest,
    ShipmentRAGResponse,
)
from shipment_intelligence_api.rag.service import ShipmentRAGService
from shipment_intelligence_api.core.dependencies import get_rag_service

router = APIRouter(prefix="/rag", tags=["RAG"])


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
