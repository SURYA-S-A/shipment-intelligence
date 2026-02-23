from typing import List
from langchain_core.documents import Document
from pydantic import BaseModel, Field


class ShipmentRAGRequest(BaseModel):
    """Request model for shipment investigation query."""

    question: str = Field(
        ...,
        description="User question related to the shipment.",
        example="Why is this shipment delayed?",
    )


class ShipmentRAGResponse(BaseModel):
    """Response model containing shipment investigation results."""

    answer: str = Field(
        ...,
        description="Generated analysis including delay status, root cause, and recommended action.",
    )

    context: List[Document] = Field(
        default_factory=list,
        description="List of retrieved shipment event documents used for analysis.",
    )
