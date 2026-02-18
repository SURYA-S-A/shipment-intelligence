from pydantic import BaseModel, Field


class ShipmentRetrievalOutput(BaseModel):
    """Shipment ID extracted from the given query."""

    shipment_id: str = Field(description="The ID of the shipment being analyzed")
