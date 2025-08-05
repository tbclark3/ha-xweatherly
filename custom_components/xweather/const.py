DOMAIN = "xweather"

PLATFORMS = ["weather", "sensor", "air_quality", "button"]

CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_NAME = "xweather"
DEFAULT_UPDATE_INTERVAL = 60

API_BASE = "https://data.api.xweather.com"

# Map XWeather coded conditions to Home Assistant weather conditions/icons
ICON_MAP = {
    # Cloud-only codes
    "CL": "sunny",
    "FW": "partlycloudy",
    "SC": "partlycloudy",
    "BK": "cloudy",
    "OV": "cloudy",
    # Precipitation and weather codes
    "R": "rainy",
    "RW": "rainy",
    "RS": "snowy-rainy",
    "S": "snowy",
    "SW": "snowy",
    "T": "lightning",
    "WM": "snowy-rainy",
    "ZR": "pouring",
    "ZL": "pouring",
    "ZF": "fog",
    "F": "fog",
    "H": "fog",
    "BR": "fog",
}
