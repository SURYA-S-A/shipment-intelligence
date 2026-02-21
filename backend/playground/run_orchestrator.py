from shipment_intelligence_api.core.dependencies import get_agent_service
from langgraph.graph.state import CompiledStateGraph


def generate_mermaid_graph(compiled_graph: CompiledStateGraph):
    """Generate and save mermaid graph"""
    print(f"\n{'='*70}")
    print("Mermaid Graph for Shipment Intelligence Orchestrator")
    print(f"{'='*70}\n")

    mermaid_graph = compiled_graph.get_graph(xray=True).draw_mermaid()
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
    agent_service = get_agent_service()

    # Generate mermaid graph
    generate_mermaid_graph(agent_service.orchestrator.compiled_graph)

    print("Running orchestrator with sample query...")

    response = agent_service.process_query(
        query="delay reason customer complaint urgency escalation history - SHP1009"
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
