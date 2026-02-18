from shipment_intelligence_api.agents.analysis_agent.agent import ShipmentAnalysisAgent
from shipment_intelligence_api.agents.escalation_agent.agent import EscalationAgent
from shipment_intelligence_api.agents.orchestrator.workflow import (
    ShipmentIntelligenceOrchestrator,
)
from shipment_intelligence_api.agents.response_agent.agent import ShipmentResponseAgent
from shipment_intelligence_api.agents.retrieval_agent.agent import (
    ShipmentRetrievalAgent,
)


def generate_mermaid_graph(orchestrator: ShipmentIntelligenceOrchestrator):
    """Generate and save mermaid graph"""
    print(f"\n{'='*70}")
    print("Mermaid Graph for Shipment Intelligence Orchestrator")
    print(f"{'='*70}\n")

    mermaid_graph = orchestrator.compiled_graph.get_graph(xray=True).draw_mermaid()
    mermaid_graph = (
        mermaid_graph.replace("\\5b", "_").replace("\\5d", "_").replace("\\2e", "_")
    )
    print(mermaid_graph)
    print(f"\n{'='*70}\n")
    print("Graph generation complete.")


def pretty_print_messages(title: str, messages: list):
    """Prints messages in a formatted way.
    Args:
        title: Section title for the messages.
        messages: List of messages to print.
    """
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'=' * 70}")
    if not messages:
        print("No messages.\n")
        return

    if not isinstance(messages, list):
        messages = [messages]

    for message in messages:
        message.pretty_print()
        print("\n")


if __name__ == "__main__":
    print("Initializing agents...")
    retrieval_agent = ShipmentRetrievalAgent()
    analysis_agent = ShipmentAnalysisAgent()
    response_agent = ShipmentResponseAgent()
    escalation_agent = EscalationAgent()

    orchestrator = ShipmentIntelligenceOrchestrator(
        retrieval_agent, analysis_agent, response_agent, escalation_agent
    )

    # Generate mermaid graph
    generate_mermaid_graph(orchestrator)

    print("Running orchestrator with sample query...")

    response = orchestrator.run(
        query="What is the status of shipment SHP1003 and are there any issues?"
    )

    print("Orchestrator run complete. Output:\n")

    pretty_print_messages(
        "Shipment Retrieval Agent Messages",
        response.get("retrieval_agent_messages", []),
    )

    pretty_print_messages(
        "Shipment Analysis Agent Messages",
        response.get("analysis_agent_messages", []),
    )

    pretty_print_messages(
        "Shipment Response Agent Messages",
        response.get("response_agent_messages", []),
    )

    pretty_print_messages(
        "Escalation Agent Messages",
        response.get("escalation_agent_messages", []),
    )
    print(f"{'='*70}\n")
