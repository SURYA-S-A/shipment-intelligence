from typing import Any, Dict
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from shipment_intelligence_api.infrastructure.vector_store.qdrant_store_manager import (
    QdrantVectorStoreManager,
)
from shipment_intelligence_api.rag.prompts import get_question_answering_prompt
from shipment_intelligence_api.rag.state import ShipmentRAGState
from langchain_core.language_models import BaseChatModel


class ShipmentRAGPipeline:
    """RAG pipeline for shipment intelligence queries.

    Implements a retrieval-augmented generation workflow using LangGraph
    to orchestrate document retrieval and answer generation.
    """

    def __init__(
        self, llm: BaseChatModel, qdrant_store_manager: QdrantVectorStoreManager
    ):
        """Initialize RAG pipeline.

        Args:
            llm: LLM instance for answer generation.
            qdrant_store_manager: Manager for qdrant vector store operations.
        """
        self.llm: BaseChatModel = llm
        self.qdrant_store_manager = qdrant_store_manager
        self.compiled_graph: CompiledStateGraph = self._build_graph()

    def _retrieve_documents(self, state: ShipmentRAGState) -> Dict[str, Any]:
        """Retrieve relevant documents from vector store.

        Args:
            state: Current RAG state containing shipment_id and question.

        Returns:
            Dict with 'context' key containing retrieved documents.
        """
        docs = self.qdrant_store_manager.query(
            query=state["question"],
        )
        return {"context": docs}

    def _generate_answer(self, state: ShipmentRAGState) -> Dict[str, Any]:
        """Generate answer based on retrieved context.

        Args:
            state: Current RAG state containing question and context documents.

        Returns:
            Dict with 'answer' key containing generated response.
        """
        llm = self.llm
        prompt = get_question_answering_prompt()

        context_text = "\n\n".join([doc.page_content for doc in state["context"]])

        messages = prompt.format_prompt(
            context=context_text,
            question=state["question"],
        ).to_messages()

        response = llm.invoke(messages)

        return {"answer": response.content}

    def _build_graph(self) -> CompiledStateGraph:
        """Build and compile the LangGraph workflow.

        Returns:
            Compiled state graph for execution.
        """
        graph = StateGraph(ShipmentRAGState)

        graph.add_node("retrieve_documents", self._retrieve_documents)
        graph.add_node("generate_answer", self._generate_answer)

        graph.add_edge(START, "retrieve_documents")
        graph.add_edge("retrieve_documents", "generate_answer")
        graph.add_edge("generate_answer", END)

        return graph.compile()

    def run(self, question: str) -> dict:
        """Execute the RAG pipeline for a given query.

        Args:
            question: User's question about the shipment.

        Returns:
            Dict containing 'answer' and 'context' keys.
        """
        return self.compiled_graph.invoke(
            {
                "question": question,
            }
        )
