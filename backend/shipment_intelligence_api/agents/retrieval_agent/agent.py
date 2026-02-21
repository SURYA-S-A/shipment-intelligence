from langchain.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.messages import SystemMessage
from langgraph.graph import START, END, StateGraph
from shipment_intelligence_api.agents.orchestrator.state import ShipmentWorkflowState
from shipment_intelligence_api.agents.retrieval_agent.prompts import (
    SHIPMENT_RETRIEVAL_AGENT_SYSTEM_PROMPT,
)
from shipment_intelligence_api.agents.retrieval_agent.schema import (
    ShipmentRetrievalOutput,
)
from shipment_intelligence_api.infrastructure.vector_store.qdrant_store_manager import (
    QdrantVectorStoreManager,
)


class ShipmentRetrievalAgent:
    """Extracts shipment ID and fetches related documents and customer data."""

    def __init__(
        self, llm: BaseChatModel, qdrant_store_manager: QdrantVectorStoreManager
    ):
        self.llm: BaseChatModel = llm
        self.qdrant_store_manager: QdrantVectorStoreManager = qdrant_store_manager
        self.llm_with_structured_output = self.llm.with_structured_output(
            ShipmentRetrievalOutput
        )
        self.compiled_graph: CompiledStateGraph = self._build_graph()

    def _agent(self, state: ShipmentWorkflowState):
        print("Running Shipment Retrieval Agent...")
        agent_prompt = ChatPromptTemplate(
            [
                SystemMessage(content=SHIPMENT_RETRIEVAL_AGENT_SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="retrieval_agent_messages"),
            ]
        )
        agent_runnable = agent_prompt | self.llm_with_structured_output

        structured_response: ShipmentRetrievalOutput = agent_runnable.invoke(
            input=state["retrieval_agent_messages"]
        )

        state["shipment_id"] = structured_response.shipment_id
        return state

    def _fetch_shipment_data(self, state: ShipmentWorkflowState):
        shipment_id = state.get("shipment_id")
        print(f" [Node] Fetching shipment data for shipment ID: {shipment_id}")

        retrieved_docs = self.qdrant_store_manager.query(
            shipment_id=shipment_id, query=state["question"]
        )

        return {"retrieved_docs": retrieved_docs}

    def _fetch_customer_data(self, state: ShipmentWorkflowState):
        shipment_id = state.get("shipment_id")
        print(f" [Node] Fetching customer data for shipment ID: {shipment_id}")

        # TODO: Replace with actual customer data retrieval based on shipment ID
        return {
            "customer_name": "John Doe",
            "customer_phone_number": "+1234567890",
            "customer_email": "john.doe@example.com",
        }

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(ShipmentWorkflowState)
        graph.add_node("agent", self._agent)
        graph.add_node("fetch_shipment_data", self._fetch_shipment_data)
        graph.add_node("fetch_customer_data", self._fetch_customer_data)
        graph.add_edge(START, "agent")
        graph.add_edge("agent", "fetch_shipment_data")
        graph.add_edge("agent", "fetch_customer_data")
        graph.add_edge("fetch_shipment_data", END)
        graph.add_edge("fetch_customer_data", END)
        return graph.compile()
