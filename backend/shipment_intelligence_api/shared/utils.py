import io
import re
import sys
from langgraph.graph.state import CompiledStateGraph
from pathlib import Path
from shipment_intelligence_api.shared.constants import SHIPMENT_PATTERN

PROGRESS_DIR = Path(__file__).resolve().parent.parent / "progress"


def extract_shipment_id(content: str) -> str:
    """Extract shipment ID from the given content using regex pattern."""
    match = re.search(SHIPMENT_PATTERN, content)

    if not match:
        raise ValueError("Shipment ID not found in content")

    return match.group(0)


def get_file(shipment_id: str) -> Path:
    PROGRESS_DIR.mkdir(exist_ok=True)
    return PROGRESS_DIR / f"{shipment_id}.txt"


def write_mermaid_graph(compiled_graph: CompiledStateGraph, shipment_id: str):
    mermaid_graph = compiled_graph.get_graph(xray=True).draw_mermaid()
    mermaid_graph = (
        mermaid_graph.replace("\\5b", "_").replace("\\5d", "_").replace("\\2e", "_")
    )
    with get_file(shipment_id).open("a") as f:
        f.write(f"\n{'='*80}\n")
        f.write("ORCHESTRATOR GRAPH\n")
        f.write(f"{'='*80}\n\n")
        f.write(mermaid_graph)
        f.write(f"\n{'='*80}\n\n")


def write_agent_messages(shipment_id: str, title: str, messages: list):
    with get_file(shipment_id).open("a") as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"{title}\n")
        f.write(f"{'='*80}\n\n")
        if not messages:
            f.write("No messages.\n\n")
            return
        for msg in messages:
            buffer = io.StringIO()
            sys.stdout = buffer
            msg.pretty_print()
            sys.stdout = sys.__stdout__
            f.write(buffer.getvalue())
            f.write("\n")


def write_response(shipment_id: str, response: dict):
    with get_file(shipment_id).open("a", encoding="utf-8") as f:

        # Retrieval agent messages
        f.write(f"\n{'='*80}\n")
        f.write("RETRIEVAL AGENT\n")
        f.write(f"{'='*80}\n\n")
        f.write(f"Shipment ID: {response.get('shipment_id', 'N/A')}\n")
        f.write(f"Question: {response.get('question', 'N/A')}\n")
        f.write(f"TMS Data: {response.get('tms_data', 'N/A')}\n")
        f.write(f"Customer Name: {response.get('customer_name', 'N/A')}\n")
        f.write(f"Customer Email: {response.get('customer_email', 'N/A')}\n")
        f.write(f"Customer Phone: {response.get('customer_phone_number', 'N/A')}\n")
        f.write(f"Retrieved Docs:\n{response.get('retrieved_docs', 'N/A')}\n")

    write_agent_messages(
        shipment_id,
        "RETRIEVAL AGENT MESSAGES",
        response.get("retrieval_agent_messages", []),
    )

    # Analysis agent
    with get_file(shipment_id).open("a", encoding="utf-8") as f:
        f.write(f"\n{'='*80}\n")
        f.write("ANALYSIS AGENT\n")
        f.write(f"{'='*80}\n\n")
        f.write(f"Detailed Analysis:\n{response.get('detailed_analysis', 'N/A')}\n")

    write_agent_messages(
        shipment_id,
        "ANALYSIS AGENT MESSAGES",
        response.get("analysis_agent_messages", []),
    )

    # Response agent
    with get_file(shipment_id).open("a", encoding="utf-8") as f:
        f.write(f"\n{'='*80}\n")
        f.write("RESPONSE AGENT\n")
        f.write(f"{'='*80}\n\n")
        f.write(f"Should Escalate: {response.get('should_escalate', False)}\n\n")
        response_output = response.get("response_output", {})
        for key, value in response_output.items():
            f.write(f"{key.upper()}:\n{value}\n\n")

    write_agent_messages(
        shipment_id,
        "RESPONSE AGENT MESSAGES",
        response.get("response_agent_messages", []),
    )

    # Escalation agent
    write_agent_messages(
        shipment_id,
        "ESCALATION AGENT MESSAGES",
        response.get("escalation_agent_messages", []),
    )

    with get_file(shipment_id).open("a", encoding="utf-8") as f:
        f.write(f"\n{'='*80}\n")
        f.write("WORKFLOW COMPLETE\n")
        f.write(f"{'='*80}\n")
