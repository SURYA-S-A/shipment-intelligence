from shipment_intelligence_api.core.dependencies import get_rag_service
from shipment_intelligence_api.rag.schema import ShipmentRAGRequest
from shipment_intelligence_api.shared.utils import get_mermaid_graph
from shipment_intelligence_api.core.logging import get_logger


logger = get_logger(__name__)


if __name__ == "__main__":
    rag_service = get_rag_service()

    rag_request = ShipmentRAGRequest(
        question="What is the delay reason for shipment SHP1001?"
    )

    response = rag_service.run(rag_request)

    mermaid_graph = get_mermaid_graph(rag_service.pipeline.compiled_graph)

    logger.debug(f"Mermaid Graph:\n{mermaid_graph}")

    logger.debug(f"RAG Response: {response.answer}")
