from typing import List, Optional
from qdrant_client import QdrantClient, models
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from qdrant_client.models import (
    VectorParams,
    SparseVectorParams,
    Distance,
    PayloadSchemaType,
)
from langchain_core.embeddings import Embeddings
from shipment_intelligence_api.core.settings import settings
from shipment_intelligence_api.core.logging import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = get_logger(__name__)


class QdrantVectorStoreManager:
    """Qdrant vector store manager with hybrid dense + sparse search."""

    def __init__(
        self,
        client: QdrantClient,
        embeddings: Embeddings,
        sparse_embeddings: FastEmbedSparse,
    ) -> None:
        """Initialize qdrant vector store manager.

        Args:
            client: Qdrant client instance
            embeddings: Embedding model instance
            sparse_embeddings: Sparse embedding model instance
        """
        self.client: QdrantClient = client
        self.embeddings: Embeddings = embeddings
        self.sparse_embeddings: FastEmbedSparse = sparse_embeddings
        self.collection_name: str = settings.QDRANT_COLLECTION

    def init_collection(self) -> None:
        """Create collection with dense + sparse vectors and payload index."""
        if not self.client.collection_exists(collection_name=self.collection_name):

            vector_size = len(self.embeddings.embed_query("dimension check"))

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "fast-dense": VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE,
                    )
                },
                sparse_vectors_config={"fast-sparse": SparseVectorParams()},
            )

            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="metadata.shipment_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            logger.info(
                f"Created hybrid collection '{self.collection_name}' with shipment_id index"
            )
        else:
            logger.info(f"Collection '{self.collection_name}' already exists")

    def _get_vector_store(self) -> QdrantVectorStore:
        """Get hybrid LangChain QdrantVectorStore.
        Returns:
            QdrantVectorStore: Configured vector store instance.
        """
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
            sparse_embedding=self.sparse_embeddings,
            retrieval_mode=RetrievalMode.HYBRID,
            vector_name="fast-dense",
            sparse_vector_name="fast-sparse",
        )

    def add_documents(self, docs: List[Document]) -> None:
        """Add documents to the hybrid vector store.
        Automatically splits large documents before storing.

        Args:
            docs: List of documents to add.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        final_docs = []
        for doc in docs:
            if len(doc.page_content) > 1000:
                chunks = splitter.create_documents(
                    texts=[doc.page_content], metadatas=[doc.metadata]
                )
                final_docs.extend(chunks)
                logger.debug(f"Split large document into {len(chunks)} chunks")
            else:
                final_docs.append(doc)

        vs = self._get_vector_store()
        vs.add_documents(final_docs)
        logger.info(
            f"Added {len(final_docs)} documents to collection '{self.collection_name}'"
        )

    def query(
        self,
        query: str,
        shipment_id: Optional[str] = None,
        k: int = 5,
    ) -> List[Document]:
        """Hybrid query with optional shipment_id filter."""

        vs = self._get_vector_store()

        qdrant_filter = None

        # Apply filter only if shipment_id is provided
        if shipment_id:
            qdrant_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.shipment_id",
                        match=models.MatchValue(value=shipment_id),
                    )
                ]
            )

        results = vs.similarity_search(
            query,
            k=k,
            filter=qdrant_filter,
        )

        logger.debug(
            f"Retrieved {len(results)} documents"
            + (
                f" for shipment {shipment_id}"
                if shipment_id
                else " (no shipment filter)"
            )
        )

        return results
