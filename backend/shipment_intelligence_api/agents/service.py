from shipment_intelligence_api.agents.orchestrator.workflow import (
    ShipmentIntelligenceOrchestrator,
)
from shipment_intelligence_api.shared.utils import (
    get_file,
    write_response,
)


class ShipmentIntelligenceAgentService:
    def __init__(self, orchestrator: ShipmentIntelligenceOrchestrator):
        self.orchestrator = orchestrator

    def process_query(self, query: str) -> None:
        """Process a shipment intelligence query through the orchestrator workflow."""
        response = self.orchestrator.run(query)

        shipment_id = response.get("shipment_id", "UNKNOWN")

        # New file every run based on shipment_id
        get_file(shipment_id).write_text(
            f"SHIPMENT INTELLIGENCE REPORT — {shipment_id}\n"
        )

        write_response(shipment_id, response)

        print(f"Done → progress/{shipment_id}.txt")
