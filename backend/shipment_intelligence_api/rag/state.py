from typing import TypedDict, List
from langchain_core.documents import Document


class ShipmentRAGState(TypedDict):
    shipment_id: str
    question: str
    context: List[Document]
    answer: str
