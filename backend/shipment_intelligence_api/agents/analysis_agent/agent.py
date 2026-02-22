from langchain_core.language_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langgraph.graph import START, END, StateGraph
from shipment_intelligence_api.agents.analysis_agent.prompts import (
    SHIPMENT_ANALYSIS_AGENT_SYSTEM_PROMPT,
)
from shipment_intelligence_api.agents.analysis_agent.tools import check_weather
from shipment_intelligence_api.agents.orchestrator.state import ShipmentWorkflowState
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from functools import partial


class ShipmentAnalysisAgent:
    """Analyzes retrieved documents and generates insights using available tools."""

    def __init__(self, llm: BaseChatModel):
        self.tools = [check_weather]
        self.llm: BaseChatModel = llm
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.compiled_graph: CompiledStateGraph = self._build_graph()

    def _agent(self, state: ShipmentWorkflowState):
        print("Running Shipment Analysis Agent...")
        agent_prompt = ChatPromptTemplate(
            [
                SystemMessagePromptTemplate.from_template(
                    SHIPMENT_ANALYSIS_AGENT_SYSTEM_PROMPT
                ),
                MessagesPlaceholder(variable_name="analysis_agent_messages"),
            ]
        )

        agent_runnable = agent_prompt | self.llm_with_tools

        response = agent_runnable.invoke(
            {
                "retrieved_docs": state.get("retrieved_docs", ""),
                "tms_data": state.get("tms_data", ""),
                "analysis_agent_messages": state.get("analysis_agent_messages", []),
            }
        )

        state["analysis_agent_messages"] = add_messages(
            state["analysis_agent_messages"], [response]
        )
        state["detailed_analysis"] = (
            state.get("detailed_analysis", "") + "\n" + str(response)
        )
        return state

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(ShipmentWorkflowState)
        graph.add_node("agent", self._agent)
        graph.add_node(
            "tools", ToolNode(self.tools, messages_key="analysis_agent_messages")
        )
        graph.add_edge(START, "agent")
        graph.add_conditional_edges(
            "agent",
            partial(tools_condition, messages_key="analysis_agent_messages"),
            {"tools": "tools", "__end__": END},
        )
        graph.add_edge("tools", "agent")
        return graph.compile()
