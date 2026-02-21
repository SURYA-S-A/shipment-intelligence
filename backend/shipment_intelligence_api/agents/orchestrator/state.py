from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage


class ShipmentWorkflowState(TypedDict):
    """Shared state across all agents in the shipment intelligence workflow."""

    # State for Shipment Retriever Agent
    question: str
    retrieval_agent_messages: Annotated[list[AnyMessage], add_messages]
    shipment_id: str
    retrieved_docs: str
    customer_name: str
    customer_phone_number: str
    customer_email: str

    # State for Shipment Analyzer Agent
    analysis_agent_messages: Annotated[list[AnyMessage], add_messages]
    detailed_analysis: str

    # State for Shipment Response Agent
    response_agent_messages: Annotated[list[AnyMessage], add_messages]
    should_escalate: bool
    response_output: dict

    # State for Escalation Agent
    escalation_agent_messages: Annotated[list[AnyMessage], add_messages]
