from datetime import datetime
from typing import List, Literal
from langchain_core.documents import Document
from pydantic import BaseModel, Field, model_validator

from shipment_intelligence_api.shared.utils import extract_shipment_id


class IncomingCommunicationRequest(BaseModel):
    channel: Literal["email", "sms", "call"] = Field(
        ..., description="Type of incoming communication."
    )

    source: str = Field(..., description="Sender email or phone number.")

    content: str = Field(..., description="Email body, SMS text, or call transcript.")

    timestamp: datetime = Field(..., description="Event timestamp in ISO format.")

    shipment_id: str | None = None  # auto-populated

    @model_validator(mode="after")
    def set_shipment_id(cls, values):
        values.shipment_id = extract_shipment_id(values.content)
        return values


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
