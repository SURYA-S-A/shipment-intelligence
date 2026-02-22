from langchain.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langgraph.graph import START, END, StateGraph
from shipment_intelligence_api.agents.orchestrator.state import ShipmentWorkflowState
from shipment_intelligence_api.agents.response_agent.prompts import (
    SHIPMENT_RESPONSE_AGENT_SYSTEM_PROMPT,
)
from shipment_intelligence_api.agents.response_agent.schema import (
    ShipmentResponseOutput,
)
from shipment_intelligence_api.core.logging import get_logger

logger = get_logger(__name__)


class ShipmentResponseAgent:
    """Generates structured summaries with confidence scores and escalation decisions."""

    def __init__(self, llm: BaseChatModel):
        self.llm: BaseChatModel = llm
        self.llm_with_structured_output = self.llm.with_structured_output(
            ShipmentResponseOutput
        )
        self.compiled_graph: CompiledStateGraph = self._build_graph()

    def _agent(self, state: ShipmentWorkflowState):
        logger.info("Running Shipment Response Agent...")
        agent_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    SHIPMENT_RESPONSE_AGENT_SYSTEM_PROMPT
                ),
                MessagesPlaceholder(variable_name="response_agent_messages"),
            ]
        )

        agent_runnable = agent_prompt | self.llm_with_structured_output

        structured_response: ShipmentResponseOutput = agent_runnable.invoke(
            {
                "detailed_analysis": state.get("detailed_analysis", ""),
                "response_agent_messages": state.get("response_agent_messages", []),
            }
        )

        logger.debug(f"Response Agent output: {structured_response}")
        state["should_escalate"] = structured_response.should_escalate
        state["response_output"] = structured_response.model_dump()

        return state

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(ShipmentWorkflowState)
        graph.add_node("agent", self._agent)
        graph.add_edge(START, "agent")
        graph.add_edge("agent", END)
        return graph.compile()
