from typing import TypedDict, List
from langchain_core.documents import Document


class ShipmentRAGState(TypedDict):
    question: str
    context: List[Document]
    answer: str
