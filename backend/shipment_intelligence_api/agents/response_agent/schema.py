from typing import List, Literal
from pydantic import BaseModel, Field


class ShipmentResponseOutput(BaseModel):
    """Structured summary with confidence and escalation decision."""

    confidence: float = Field(
        description="Confidence score between 0 and 1", ge=0, le=1
    )
    sources_used: List[str] = Field(description="List of sources or documents used")
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(
        description="Risk level of the shipment issue: LOW for minor delays, MEDIUM for moderate impact, HIGH for significant disruption, CRITICAL for severe business impact"
    )
    should_escalate: bool = Field(
        description="Whether to escalate and send notifications (typically true for MEDIUM and above)"
    )
    summary: str = Field(description="Brief summary of the response")
