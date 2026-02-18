from functools import partial
from langgraph.graph.state import CompiledStateGraph
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from shipment_intelligence_api.agents.escalation_agent.prompts import (
    ESCALATION_AGENT_SYSTEM_PROMPT,
)
from shipment_intelligence_api.agents.escalation_agent.tool import (
    create_support_ticket,
    send_email,
    send_sms,
)
from shipment_intelligence_api.agents.orchestrator.state import ShipmentWorkflowState
from shipment_intelligence_api.infrastructure.llm.llm_provider import get_llm


class EscalationAgent:
    """Executes notifications, creates tickets, and logs communications."""

    def __init__(self):
        self.tools = [send_email, send_sms, create_support_ticket]
        self.llm = get_llm()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.compiled_graph: CompiledStateGraph = self._build_graph()

    def _agent(self, state: ShipmentWorkflowState):
        print(
            f"Escalation Agent processing escalation with response output: {state.get('response_output', {})}"
        )

        agent_prompt = ChatPromptTemplate(
            [
                SystemMessagePromptTemplate.from_template(
                    ESCALATION_AGENT_SYSTEM_PROMPT
                ),
                MessagesPlaceholder(variable_name="escalation_agent_messages"),
            ]
        )
        agent_runnable = agent_prompt | self.llm_with_tools

        response = agent_runnable.invoke(
            {
                "response_agent_output": state.get("response_output", {}),
                "customer_name": state.get("customer_name", ""),
                "customer_email": state.get("customer_email", ""),
                "customer_phone": state.get("customer_phone_number", ""),
                "escalation_agent_messages": state.get("escalation_agent_messages", []),
            }
        )

        state["escalation_agent_messages"] = add_messages(
            state["escalation_agent_messages"], [response]
        )

        return state

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(ShipmentWorkflowState)
        graph.add_node("agent", self._agent)
        graph.add_node(
            "tools",
            ToolNode(self.tools, messages_key="escalation_agent_messages"),
        )
        graph.add_edge(START, "agent")
        graph.add_conditional_edges(
            "agent",
            partial(tools_condition, messages_key="escalation_agent_messages"),
            {"tools": "tools", "__end__": END},
        )
        graph.add_edge("tools", "agent")
        return graph.compile()
