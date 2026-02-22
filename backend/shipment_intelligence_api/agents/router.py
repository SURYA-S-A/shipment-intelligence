from fastapi import APIRouter, BackgroundTasks, Depends
from shipment_intelligence_api.agents.constants import CommunicationChannel
from shipment_intelligence_api.agents.schema import (
    IncomingCommunicationRequest,
)
from shipment_intelligence_api.agents.service import ShipmentIntelligenceAgentService
from shipment_intelligence_api.rag.service import ShipmentRAGService
from shipment_intelligence_api.core.dependencies import (
    get_agent_service,
    get_rag_service,
)

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post(
    "/incoming-communication",
    summary="Incoming Communication",
    description="Receives TMS webhooks, email, SMS, or call transcript then store in RAG and triggers agent pipeline for the associated shipment.",
)
def handle_incoming_communication(
    request: IncomingCommunicationRequest,
    background_tasks: BackgroundTasks,
    agent_service: ShipmentIntelligenceAgentService = Depends(get_agent_service),
    rag_service: ShipmentRAGService = Depends(get_rag_service),
):
    if request.channel != CommunicationChannel.TMS_EVENT:
        rag_service.ingest_event(request)
    background_tasks.add_task(agent_service.process_query, request.shipment_id)
    return {"message": "Communication received", "shipment_id": request.shipment_id}
