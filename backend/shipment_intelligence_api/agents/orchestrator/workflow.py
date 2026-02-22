from langgraph.graph.message import StateGraph
from langchain_core.messages import HumanMessage
from langgraph.graph import START, END
from typing import Literal
from langgraph.graph.state import CompiledStateGraph
from shipment_intelligence_api.agents.analysis_agent.agent import ShipmentAnalysisAgent
from shipment_intelligence_api.agents.escalation_agent.agent import EscalationAgent
from shipment_intelligence_api.agents.orchestrator.state import ShipmentWorkflowState
from shipment_intelligence_api.agents.response_agent.agent import ShipmentResponseAgent
from shipment_intelligence_api.agents.retrieval_agent.agent import (
    ShipmentRetrievalAgent,
)
from shipment_intelligence_api.core.logging import get_logger

logger = get_logger(__name__)


class ShipmentIntelligenceOrchestrator:
    """Orchestrates the multi-agent workflow for shipment intelligence queries."""

    def __init__(
        self,
        retrieval_agent: ShipmentRetrievalAgent,
        analysis_agent: ShipmentAnalysisAgent,
        response_agent: ShipmentResponseAgent,
        escalation_agent: EscalationAgent,
    ):
        """Initializes orchestrator with agent instances.

        Args:
            retrieval_agent: Agent for document retrieval.
            analysis_agent: Agent for insight analysis.
            response_agent: Agent for summary generation.
            escalation_agent: Agent for escalation actions.
        """
        self.retrieval_agent = retrieval_agent
        self.analysis_agent = analysis_agent
        self.response_agent = response_agent
        self.escalation_agent = escalation_agent
        self.compiled_graph: CompiledStateGraph = self._build_graph()

    def _should_escalate(
        self, state: ShipmentWorkflowState
    ) -> Literal["escalation", "__end__"]:
        should_escalate = state.get("should_escalate", False)
        logger.info(f"Escalation decision: {should_escalate}")
        return "escalation" if should_escalate else "__end__"

    def _build_graph(self):
        graph = StateGraph(ShipmentWorkflowState)
        graph.add_node("retrieval", self.retrieval_agent.compiled_graph)
        graph.add_node("analysis", self.analysis_agent.compiled_graph)
        graph.add_node("response", self.response_agent.compiled_graph)
        graph.add_node("escalation", self.escalation_agent.compiled_graph)

        graph.add_edge(START, "retrieval")
        graph.add_edge("retrieval", "analysis")
        graph.add_edge("analysis", "response")
        graph.add_conditional_edges(
            "response",
            self._should_escalate,
            {"escalation": "escalation", "__end__": END},
        )
        graph.add_edge("escalation", END)

        return graph.compile()

    def run(self, query: str):
        """Executes the multi-agent workflow for a given query.

        Args:
            query: Shipment-related query or event trigger containing shipment ID.
                Can be user-initiated, system-generated, or event-driven.

        Returns:
            Final state containing all agent outputs and messages.
        """
        response = self.compiled_graph.invoke(
            {
                "question": query,
                "retrieval_agent_messages": [
                    HumanMessage(content=f"Extract shipment information from: {query}")
                ],
                "analysis_agent_messages": [
                    HumanMessage(
                        content="Analyze the retrieved documents and find insights"
                    )
                ],
                "response_agent_messages": [
                    HumanMessage(
                        content="Generate a structured response based on the analysis with confidence score, sources used, and whether to escalate"
                    )
                ],
                "escalation_agent_messages": [
                    HumanMessage(
                        content="Execute appropriate escalation actions (email, SMS, ticket creation) based on the response"
                    )
                ],
            }
        )

        return response
