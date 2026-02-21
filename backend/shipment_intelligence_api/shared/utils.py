import re

from shipment_intelligence_api.shared.constants import SHIPMENT_PATTERN


def extract_shipment_id(content: str) -> str:
    match = re.search(SHIPMENT_PATTERN, content)

    if not match:
        raise ValueError("Shipment ID not found in content")

    return match.group(0)
