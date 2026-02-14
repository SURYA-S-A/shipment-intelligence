from datetime import datetime
from typing import List
from langchain_core.documents import Document
from pydantic import BaseModel, Field


class ShipmentEventRequest(BaseModel):
    """Request model for ingesting a shipment event into the vector store."""

    shipment_id: str = Field(
        ...,
        description="Unique identifier for the shipment.",
        example="SH12345",
    )

    event_type: str = Field(
        ...,
        description="Type of shipment event (e.g., EMAIL, STATUS_UPDATE, ALERT).",
        example="EMAIL",
    )

    source: str = Field(
        ...,
        description="Source system or sender of the event.",
        example="ops@carrier.com",
    )

    description: str = Field(
        ...,
        description="Detailed description of the shipment event.",
        example="Shipment delayed due to customs inspection.",
    )

    timestamp: datetime = Field(
        ...,
        description="Timestamp when the event occurred (ISO format).",
        example="2026-02-14T10:30:00",
    )


class ShipmentRAGRequest(BaseModel):
    """Request model for shipment investigation query."""

    shipment_id: str = Field(
        ...,
        description="Unique shipment identifier to investigate.",
        example="SH12345",
    )

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
