from shipment_intelligence_api.core.dependencies import get_agent_service
from shipment_intelligence_api.shared.utils import (
    get_file,
    write_mermaid_graph,
    write_response,
)


if __name__ == "__main__":
    agent_service = get_agent_service()

    response = agent_service.process_query(
        query="delay reason customer complaint urgency escalation history - SHP1009"
    )

    shipment_id = response.get("shipment_id", "UNKNOWN")

    # New file every run based on shipment_id
    get_file(shipment_id).write_text(f"SHIPMENT INTELLIGENCE REPORT — {shipment_id}\n")

    write_mermaid_graph(agent_service.orchestrator.compiled_graph, shipment_id)
    write_response(shipment_id, response)

    print(f"Done → progress/{shipment_id}.txt")
