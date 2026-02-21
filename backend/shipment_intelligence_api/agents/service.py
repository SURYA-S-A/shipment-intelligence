from shipment_intelligence_api.agents.orchestrator.workflow import (
    ShipmentIntelligenceOrchestrator,
)


class ShipmentIntelligenceAgentService:
    def __init__(self, orchestrator: ShipmentIntelligenceOrchestrator):
        self.orchestrator = orchestrator

    def process_query(self, query: str) -> dict:
        """Process a shipment intelligence query through the orchestrator workflow."""
        result = self.orchestrator.run(query)
        return result
