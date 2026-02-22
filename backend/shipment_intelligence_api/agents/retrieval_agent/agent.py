from langchain.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.messages import SystemMessage
from langgraph.graph import START, END, StateGraph
from shipment_intelligence_api.agents.orchestrator.state import ShipmentWorkflowState
from shipment_intelligence_api.agents.retrieval_agent.mock_data import (
    get_customer_data,
    get_tms_data,
)
from shipment_intelligence_api.agents.retrieval_agent.prompts import (
    SHIPMENT_RETRIEVAL_AGENT_SYSTEM_PROMPT,
)
from shipment_intelligence_api.agents.retrieval_agent.schema import (
    ShipmentRetrievalOutput,
)
from shipment_intelligence_api.infrastructure.vector_store.qdrant_store_manager import (
    QdrantVectorStoreManager,
)
from shipment_intelligence_api.core.logging import get_logger

logger = get_logger(__name__)


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
        logger.info("Running Shipment Retrieval Agent...")
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
        logger.debug(f"Extracted shipment ID: {structured_response.shipment_id}")
        return state

    def _fetch_shipment_event(self, state: ShipmentWorkflowState):
        shipment_id = state.get("shipment_id")
        logger.info(f"Fetching shipment events for {shipment_id}")

        retrieved_docs = self.qdrant_store_manager.query(
            shipment_id=shipment_id, query=state["question"]
        )

        return {"retrieved_docs": retrieved_docs}

    def _fetch_tms_data(self, state: ShipmentWorkflowState):
        shipment_id = state.get("shipment_id")
        logger.info(f"Fetching TMS data for {shipment_id}")
        data = get_tms_data(shipment_id)
        return {
            "tms_data": f"Status: {data['status']}, Origin: {data['origin']}, Destination: {data['destination']}, Carrier: {data['carrier']}, Planned Arrival: {data['planned_arrival']}, Estimated Arrival: {data['estimated_arrival']}, Delay (min): {data['delay_minutes']}, SLA Breach: {data['sla_breach']}."
        }

    def _fetch_customer_data(self, state: ShipmentWorkflowState):
        shipment_id = state.get("shipment_id")
        logger.info(f"Fetching customer data for {shipment_id}")
        data = get_customer_data(shipment_id)
        return {
            "customer_name": data["customer_name"],
            "customer_phone_number": data["customer_phone"],
            "customer_email": data["customer_email"],
        }

    def _build_graph(self) -> CompiledStateGraph:
        graph = StateGraph(ShipmentWorkflowState)
        graph.add_node("agent", self._agent)
        graph.add_node("fetch_shipment_event", self._fetch_shipment_event)
        graph.add_node("fetch_tms_data", self._fetch_tms_data)
        graph.add_node("fetch_customer_data", self._fetch_customer_data)
        graph.add_edge(START, "agent")
        graph.add_edge("agent", "fetch_shipment_event")
        graph.add_edge("agent", "fetch_tms_data")
        graph.add_edge("agent", "fetch_customer_data")
        graph.add_edge("fetch_shipment_event", END)
        graph.add_edge("fetch_tms_data", END)
        graph.add_edge("fetch_customer_data", END)
        return graph.compile()
