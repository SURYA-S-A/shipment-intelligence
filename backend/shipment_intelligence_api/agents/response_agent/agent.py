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
from shipment_intelligence_api.infrastructure.llm.llm_provider import get_llm


class ShipmentResponseAgent:
    """Generates structured summaries with confidence scores and escalation decisions."""

    def __init__(self):
        self.llm = get_llm()
        self.llm_with_structured_output = self.llm.with_structured_output(
            ShipmentResponseOutput
        )
        self.compiled_graph: CompiledStateGraph = self._build_graph()

    def _agent(self, state: ShipmentWorkflowState):
        print("Running Shipment Response Agent...")
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

        print(f"Response Agent completed with output: {structured_response}")
        state["should_escalate"] = structured_response.should_escalate
        state["response_output"] = structured_response.model_dump()

        return state

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(ShipmentWorkflowState)
        graph.add_node("agent", self._agent)
        graph.add_edge(START, "agent")
        graph.add_edge("agent", END)
        return graph.compile()
