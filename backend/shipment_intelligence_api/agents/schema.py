from typing import Literal

from pydantic import BaseModel, Field, model_validator
from datetime import datetime

from shipment_intelligence_api.shared.utils import extract_shipment_id


class IncomingCommunicationRequest(BaseModel):
    shipment_id: str | None = None  # auto-populated if not provided
    channel: Literal["email", "sms", "call", "tms_event"] = Field(
        ..., description="Type of incoming communication."
    )
    source: str = Field(description="Sender email or phone number.")
    content: str = Field(description="Email body, SMS text, or call transcript.")
    timestamp: datetime = Field(description="Event timestamp in ISO format.")

    @model_validator(mode="after")
    def extract_shipment_id_if_missing(self):
        if not self.shipment_id and self.content:
            self.shipment_id = extract_shipment_id(self.content)
        return self
