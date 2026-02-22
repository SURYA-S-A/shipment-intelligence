from langchain_core.tools import tool
from shipment_intelligence_api.agents.analysis_agent.mock_data import WEATHER_DATA


@tool
def check_weather(location: str) -> str:
    """Check the current weather for a given location.

    Args:
        location: City name related to the shipment route.
    """
    data = WEATHER_DATA.get(location)
    if not data:
        result = f"Weather data not available for {location}"
    else:
        result = (
            f"{location}: {data['condition']}, {data['temp']}, Wind: {data['wind']}"
        )
    return result
