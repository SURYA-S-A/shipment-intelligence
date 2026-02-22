from langchain_core.tools import tool
from shipment_intelligence_api.agents.analysis_agent.mock_data import WEATHER_DATA


@tool
def check_weather(location: str) -> str:
    """Check the current weather for a given location.

    Args:
        location: City name only, without state or country suffix.
    """
    # Normalize — strip state suffix like ", PA" or ", NY"
    normalized = location.split(",")[0].strip()

    data = WEATHER_DATA.get(normalized)
    if not data:
        return f"Weather data not available for {normalized}"
    return f"{normalized}: {data['condition']}, {data['temp']}, Wind: {data['wind']}"
