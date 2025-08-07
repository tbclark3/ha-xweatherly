"""Constants for the Xweather integration."""

DOMAIN = "xweather"

PLATFORMS = ["weather", "sensor", "air_quality", "button"]

CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_NAME = "Xweather"
DEFAULT_UPDATE_INTERVAL = 60

API_BASE = "https://data.api.xweather.com"

# Map XWeather coded conditions to Home Assistant weather conditions/icons
ICON_MAP = {
    # Cloud codes
    "CL": "sunny",
    "CL-N": "clear-night",
    "FW": "partlycloudy",
    "SC": "partlycloudy",
    "SC-N": "partlycloudy-night",
    "BK": "cloudy",
    "OV": "cloudy",

    # Precipitation and weather codes
    "R": "rainy",
    "RW": "rainy",
    "LD": "rainy",  # Drizzle is a form of rain
    "RS": "snowy-rainy",
    "S": "snowy",
    "SW": "snowy",
    "SS": "snowy",  # Snow/sleet mix is similar to snowy-rainy
    "SI": "snowy-rainy",
    "WM": "snowy-rainy",
    "IP": "snowy-rainy",  # Ice pellets/sleet
    "T": "lightning-rainy",  # Thunderstorms always imply rain
    "TOT": "exceptional",  # Tornado
    "FC": "exceptional",  # Funnel Cloud
    "WP": "exceptional",  # Waterspouts
    "AH": "hail",
    "ZR": "pouring",  # Freezing rain is similar to pouring rain
    "ZL": "pouring",  # Freezing drizzle
    "ZF": "fog",
    "F": "fog",
    "FR": "fog",  # Frost can be represented as fog
    "IF": "fog",  # Ice fog
    "BR": "fog",  # Mist is a form of fog
    "H": "fog",  # Haze is a form of fog
    "BS": "windy-variant",  # Blowing snow
    "BD": "windy-variant",  # Blowing dust
    "BN": "windy-variant",  # Blowing sand
    "BY": "windy-variant",  # Blowing spray
    "K": "fog",  # Smoke
    "VA": "exceptional",  # Volcanic ash
    "IC": "snowy",  # Ice crystals
    "UP": "exceptional",  # Unknown precipitation
    "ZY": "exceptional"  # Freezing spray
}
