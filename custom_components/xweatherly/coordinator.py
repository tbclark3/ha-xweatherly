from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    API_BASE,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

# Pollutant key normalization for consistency
POLLUTANT_KEY_MAP = {
    "pm2.5": "pm25",
    "pm10": "pm10",
    "co": "co",
    "no2": "no2",
    "so2": "so2",
    "o3": "o3",
}


class XWeatherlyDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching and processing XWeatherly data."""

    def __init__(self, hass: HomeAssistant, entry):
        self.hass = hass
        self.entry = entry
        self.session = async_get_clientsession(hass)

        self.client_id = entry.data[CONF_CLIENT_ID]
        self.client_secret = entry.data[CONF_CLIENT_SECRET]
        self.lat = entry.data.get("latitude", hass.config.latitude)
        self.lon = entry.data.get("longitude", hass.config.longitude)
        interval = entry.data.get(CONF_UPDATE_INTERVAL, 60)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=interval),
        )

    async def _async_update_data(self):
        """Fetch and normalize XWeatherly data."""
        try:
            conditions = await self._fetch("conditions")
            airquality = await self._fetch("airquality")
            forecast_hourly = await self._fetch(
                "forecasts", {"filter": "1hr", "limit": 24}
            )
            forecast_daily = await self._fetch(
                "forecasts", {"filter": "day", "limit": 7}
            )

            # Normalize pollutants in air quality data
            if airquality and "periods" in airquality and airquality["periods"]:
                for period in airquality["periods"]:
                    pollutants = period.get("pollutants", [])
                    normalized_pollutants = []
                    for pol in pollutants:
                        original_type = pol.get("type", "").lower()
                        safe_type = POLLUTANT_KEY_MAP.get(original_type, original_type)
                        pol["safe_type"] = safe_type
                        normalized_pollutants.append(pol)
                    period["pollutants"] = normalized_pollutants

            return {
                "conditions": conditions,
                "airquality": airquality,
                "forecast_hourly": forecast_hourly,
                "forecast_daily": forecast_daily,
            }

        except Exception as err:
            raise UpdateFailed(f"Error fetching XWeatherly data: {err}") from err

    async def _fetch(self, endpoint: str, extra_params=None):
        """Fetch data from an XWeatherly API endpoint."""
        params = {
            "format": "json",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if extra_params:
            params.update(extra_params)

        url = f"{API_BASE}/{endpoint}/{self.lat},{self.lon}"
        async with self.session.get(url, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise UpdateFailed(
                    f"HTTP {resp.status} for {endpoint}: {text[:200]}"
                )
            data = await resp.json()
            return data.get("response", [{}])[0]
