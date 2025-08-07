from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, DEFAULT_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the button platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([XWeatherRefreshButton(coordinator, entry)])


class XWeatherRefreshButton(CoordinatorEntity, ButtonEntity):
    """A button to manually refresh the XWeather data."""

    def __init__(self, coordinator, entry):
        """Initialize the button."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_name = f"{entry.data.get('name', DEFAULT_NAME)} Refresh"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_refresh"
        self._attr_icon = "mdi:refresh"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": DEFAULT_NAME,
            "manufacturer": DEFAULT_NAME,
            "model": "API",
            "entry_type": "service",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.coordinator.async_request_refresh()
