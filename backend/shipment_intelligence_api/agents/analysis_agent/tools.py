from langchain_core.tools import StructuredTool, tool


@tool
def check_weather(location: str) -> str:
    """Check the current weather for a given location.

    Args:
         location: The location to check the weather for should be one of the cities related to the shipment route (e.g., NYC, Chicago, Miami)
    """
    print(f"Invoking tool: check_weather with location={location}")
    # TODO: Replace mock data with real weather API integration
    weather_data = {
        "NYC": "Rainy, 15°C",
        "Chicago": "Cloudy, 10°C",
        "Miami": "Sunny, 25°C",
    }
    return weather_data.get(location, "Weather data not available for this location")
