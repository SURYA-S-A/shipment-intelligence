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
from shipment_intelligence_api.infrastructure.llm.llm_provider import get_llm


class ShipmentRetrievalAgent:
    """Extracts shipment ID and fetches related documents and customer data."""

    def __init__(self):
        self.llm = get_llm()
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
        sample_docs = [
            {
                "page_content": "Shipment departed late from NYC due to operational delay.",
                "metadata": {
                    "shipment_id": "SHP1003",
                    "source": "tms_system",
                    "doc_type": "status_update",
                    "timestamp": "2026-02-10T10:30:00",
                },
                "score": 0.92,
            },
            {
                "page_content": "Weather was rainy in NYC at time of departure.",
                "metadata": {
                    "shipment_id": "SHP1003",
                    "source": "tms_system",
                    "doc_type": "weather_info",
                    "timestamp": "2026-02-10T09:00:00",
                },
                "score": 0.88,
            },
            {
                "page_content": "Shipment currently in Chicago and expected to arrive in Miami next week.",
                "metadata": {
                    "shipment_id": "SHP1003",
                    "source": "tracking_service",
                    "doc_type": "location_update",
                    "timestamp": "2026-02-14T14:15:00",
                },
                "score": 0.95,
            },
            {
                "page_content": "Shipment will be delayed again due to storm in Chicago.",
                "metadata": {
                    "shipment_id": "SHP1003",
                    "source": "email",
                    "doc_type": "delay_notice",
                    "timestamp": "2026-02-15T08:00:00",
                },
                "score": 0.90,
            },
        ]

        # TODO: Replace with RAG retrieval from vector database and document store

        return {
            "retrieved_docs": "\n\n".join(
                [
                    f"{doc['page_content']} (Source: {doc['metadata']['source']}) (Score: {doc['score']} (Doc Type: {doc['metadata']['doc_type']} Timestamp: {doc['metadata']['timestamp']}))"
                    for doc in sample_docs
                ]
            )
        }

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
