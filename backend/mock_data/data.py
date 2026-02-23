TMS_DATA = {
    "SHP1001": {
        "shipment_id": "SHP1001",
        "status": "delayed",
        "origin": "New York, NY",
        "destination": "Miami, FL",
        "carrier": "FastTrack Logistics",
        "planned_arrival": "2026-02-20T16:00:00Z",
        "estimated_arrival": "2026-02-20T22:00:00Z",
        "delay_minutes": 180,
        "sla_breach": True,
    },
    "SHP1002": {
        "shipment_id": "SHP1002",
        "status": "delayed",
        "origin": "Chicago, IL",
        "destination": "Dallas, TX",
        "carrier": "SwiftShip Co",
        "planned_arrival": "2026-02-21T10:00:00Z",
        "estimated_arrival": "2026-02-21T14:00:00Z",
        "delay_minutes": 240,
        "sla_breach": True,
    },
    "SHP1003": {
        "shipment_id": "SHP1003",
        "status": "delayed",
        "origin": "Seattle, WA",
        "destination": "Denver, CO",
        "carrier": "PacificRoute Freight",
        "planned_arrival": "2026-02-18T09:00:00Z",
        "estimated_arrival": "2026-02-18T15:00:00Z",
        "delay_minutes": 360,
        "sla_breach": True,
    },
    "SHP1004": {
        "shipment_id": "SHP1004",
        "status": "delayed",
        "origin": "Atlanta, GA",
        "destination": "Boston, MA",
        "carrier": "EastCoast Logistics",
        "planned_arrival": "2026-02-22T12:00:00Z",
        "estimated_arrival": "2026-02-22T18:00:00Z",
        "delay_minutes": 120,
        "sla_breach": False,
    },
    "SHP1005": {
        "shipment_id": "SHP1005",
        "status": "delayed",
        "origin": "Houston, TX",
        "destination": "Phoenix, AZ",
        "carrier": "SunBelt Carriers",
        "planned_arrival": "2026-02-21T08:00:00Z",
        "estimated_arrival": "2026-02-21T16:00:00Z",
        "delay_minutes": 480,
        "sla_breach": True,
    },
    "SHP1006": {
        "shipment_id": "SHP1006",
        "status": "delayed",
        "origin": "Minneapolis, MN",
        "destination": "Kansas City, MO",
        "carrier": "MidWest Express",
        "planned_arrival": "2026-02-20T14:00:00Z",
        "estimated_arrival": "2026-02-20T20:00:00Z",
        "delay_minutes": 300,
        "sla_breach": True,
    },
    "SHP1009": {
        "shipment_id": "SHP1009",
        "status": "delayed",
        "origin": "New York, NY",
        "destination": "Miami, FL",
        "carrier": "FastTrack Logistics",
        "planned_arrival": "2026-02-19T16:00:00Z",
        "estimated_arrival": "2026-02-19T22:00:00Z",
        "delay_minutes": 360,
        "sla_breach": True,
    },
}

CUSTOMER_DATA = {
    "SHP1001": {
        "customer_name": "Acme Corp",
        "customer_email": "ops@acmecorp.com",
        "customer_phone": "+15551234567",
    },
    "SHP1002": {
        "customer_name": "Global Traders Inc",
        "customer_email": "logistics@globaltraders.com",
        "customer_phone": "+15559876543",
    },
    "SHP1003": {
        "customer_name": "PacificTech Supplies",
        "customer_email": "warehouse@pacifictech.com",
        "customer_phone": "+15553456789",
    },
    "SHP1004": {
        "customer_name": "NorthEast Manufacturing",
        "customer_email": "supply@nemfg.com",
        "customer_phone": "+15556543210",
    },
    "SHP1005": {
        "customer_name": "SunState Industries",
        "customer_email": "ops@sunstate.com",
        "customer_phone": "+15557891234",
    },
    "SHP1006": {
        "customer_name": "MidWest Distributors",
        "customer_email": "dispatch@mwdist.com",
        "customer_phone": "+15552345678",
    },
    "SHP1009": {
        "customer_name": "Acme Corp",
        "customer_email": "john.doe@acmecorp.com",
        "customer_phone": "+15551234567",
    },
}


def get_tms_data(shipment_id: str) -> dict:
    return TMS_DATA.get(
        shipment_id,
        {
            "shipment_id": shipment_id,
            "status": "unknown",
            "origin": "N/A",
            "destination": "N/A",
            "carrier": "N/A",
            "planned_arrival": "N/A",
            "estimated_arrival": "N/A",
            "delay_minutes": 0,
            "sla_breach": False,
        },
    )


def get_customer_data(shipment_id: str) -> dict:
    return CUSTOMER_DATA.get(
        shipment_id,
        {
            "customer_name": "Unknown",
            "customer_email": "unknown@example.com",
            "customer_phone": "N/A",
        },
    )


WEATHER_DATA = {
    # SHP1001 — NYC → Miami (delay near Philadelphia)
    "New York": {"condition": "Rainy", "temp": "13°C", "wind": "25km/h"},
    "Philadelphia": {"condition": "Heavy Rain", "temp": "11°C", "wind": "40km/h"},
    "Miami": {"condition": "Sunny", "temp": "28°C", "wind": "15km/h"},
    # SHP1002 — Chicago → Dallas (delay near Oklahoma City)
    "Chicago": {"condition": "Cloudy", "temp": "10°C", "wind": "30km/h"},
    "Oklahoma City": {"condition": "High Winds", "temp": "18°C", "wind": "65km/h"},
    "Dallas": {"condition": "Windy", "temp": "18°C", "wind": "50km/h"},
    # SHP1003 — Seattle → Denver (delay near Salt Lake City)
    "Seattle": {"condition": "Drizzle", "temp": "11°C", "wind": "22km/h"},
    "Salt Lake City": {"condition": "Blizzard", "temp": "-5°C", "wind": "70km/h"},
    "Denver": {"condition": "Snowy", "temp": "-3°C", "wind": "35km/h"},
    # SHP1004 — Atlanta → Boston (delay near Richmond)
    "Atlanta": {"condition": "Thunderstorm", "temp": "23°C", "wind": "40km/h"},
    "Richmond": {"condition": "Thunderstorm", "temp": "14°C", "wind": "45km/h"},
    "Boston": {"condition": "Overcast", "temp": "5°C", "wind": "20km/h"},
    # SHP1005 — Houston → Phoenix (delay in Houston)
    "Houston": {"condition": "Thunderstorm", "temp": "25°C", "wind": "55km/h"},
    "Phoenix": {"condition": "Sunny", "temp": "32°C", "wind": "10km/h"},
    # SHP1006 — Minneapolis → Kansas City (delay near Minneapolis)
    "Minneapolis": {"condition": "Blizzard", "temp": "-8°C", "wind": "60km/h"},
    "Kansas City": {"condition": "Cloudy", "temp": "12°C", "wind": "22km/h"},
}
