from typing import List
from qdrant_client import QdrantClient, models
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import VectorParams, Distance, PayloadSchemaType
from langchain_core.embeddings import Embeddings
from shipment_intelligence_api.core.settings import settings
from shipment_intelligence_api.core.logging import get_logger

logger = get_logger(__name__)


class QdrantVectorStoreManager:
    """Qdrant vector store manager."""

    def __init__(self, client: QdrantClient, embeddings: Embeddings) -> None:
        """Initialize qdrant vector store manager.

        Args:
            client: Qdrant client instance
            embeddings: Embedding model instance
        """
        self.client: QdrantClient = client
        self.embeddings: Embeddings = embeddings
        self.collection_name: str = settings.QDRANT_COLLECTION

    def init_collection(self) -> None:
        """Create collection with payload index if it doesn't exist."""

        if not self.client.collection_exists(collection_name=self.collection_name):

            vector_size = len(self.embeddings.embed_query("dimension check"))

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

            # Create index for shipment_id filtering
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="metadata.shipment_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            logger.info(
                f"Created collection '{self.collection_name}' with shipment_id index"
            )

        else:
            logger.info(f"Collection '{self.collection_name}' already exists")

    def _get_vector_store(self) -> QdrantVectorStore:
        """Get LangChain QdrantVectorStore wrapper.

        Returns:
            QdrantVectorStore: Configured vector store instance.
        """
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )

    def add_documents(self, docs: List[Document]) -> None:
        """Add documents to the vector store.

        Args:
            docs: List of documents to add.

        Returns:
            List of document IDs that were added.
        """
        vs = self._get_vector_store()
        vs.add_documents(docs)

    def query(
        self,
        shipment_id: str,
        query: str,
        k: int = 5,
    ) -> List[Document]:
        """Query documents for a specific shipment.

        Args:
            shipment_id: Shipment ID to filter by.
            query: Search query text.
            k: Number of results to return (default: 5).

        Returns:
            List of matching documents sorted by relevance.
        """
        vs = self._get_vector_store()

        # Create filter for shipment_id
        qdrant_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.shipment_id",
                    match=models.MatchValue(value=shipment_id),
                )
            ]
        )

        return vs.similarity_search(query, k=k, filter=qdrant_filter)
