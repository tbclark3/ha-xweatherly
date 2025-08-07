from __future__ import annotations

from homeassistant.components.air_quality import AirQualityEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, DEFAULT_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the XWeather Air Quality entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            XWeatherAirQuality(coordinator, entry),
            XWeatherDominantPollutantSensor(coordinator, entry),
        ],
        True,
    )


class XWeatherAirQuality(CoordinatorEntity, AirQualityEntity):
    """XWeather Air Quality Entity."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, entry):
        """Initialize the XWeather Air Quality entity."""
        super().__init__(coordinator)
        self.entry = entry

        # Name the entity based on the user-provided name
        self._attr_name = f"{entry.data.get('name', DEFAULT_NAME)} Air Quality"
        # Ensure a unique ID for this specific entity
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_airquality"

    @property
    def device_info(self):
        """Return the device info, using the user-provided name."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self.entry.data.get('name', DEFAULT_NAME),
            "manufacturer": DEFAULT_NAME,
            "model": "API",
            "entry_type": "service",
        }

    @property
    def available(self):
        """Return if the entity is available."""
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [])
        if not periods:
            return False
        return periods[0].get("aqi") is not None

    @property
    def native_air_quality_index(self):
        """Return the native air quality index."""
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [])
        if not periods:
            return None
        return periods[0].get("aqi")

    @property
    def attribution(self):
        """Return the attribution."""
        return "Data provided by XWeather"

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [{}])
        if not periods:
            return {}
        period = periods[0]
        return {
            "aqi_category": period.get("category"),
            "health_index": period.get("health", {}).get("index"),
            "health_category": period.get("health", {}).get("category"),
        }

    @property
    def co(self):
        """Return the CO concentration."""
        return self._get_pollutant("co")

    @property
    def no2(self):
        """Return the NO2 concentration."""
        return self._get_pollutant("no2")

    @property
    def o3(self):
        """Return the O3 concentration."""
        return self._get_pollutant("o3")

    @property
    def so2(self):
        """Return the SO2 concentration."""
        return self._get_pollutant("so2")

    @property
    def particulate_matter_10(self):
        """Return the PM10 concentration."""
        return self._get_pollutant("pm10")

    @property
    def particulate_matter_2_5(self):
        """Return the PM2.5 concentration."""
        return self._get_pollutant("pm2.5")

    @property
    def co_unit(self):
        """Return the CO unit."""
        return CONCENTRATION_PARTS_PER_MILLION

    @property
    def no2_unit(self):
        """Return the NO2 unit."""
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def o3_unit(self):
        """Return the O3 unit."""
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def so2_unit(self):
        """Return the SO2 unit."""
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def particulate_matter_10_unit(self):
        """Return the PM10 unit."""
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def particulate_matter_2_5_unit(self):
        """Return the PM2.5 unit."""
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    def _get_pollutant(self, key: str):
        """
        Helper to get a specific pollutant's value.
        This method is refactored to be more robust and efficient.
        It first creates a dictionary of pollutants for quick lookup,
        and then returns the concentration for the requested key.
        """
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [{}])
        if not periods:
            return None

        # Build a dictionary of pollutants for O(1) lookup
        pollutants_dict = {
            (pol.get("type") or pol.get("name", "").lower()).replace(".", "").replace(" ", "").lower(): pol
            for pol in periods[0].get("pollutants", [])
        }

        # Normalize the key we are looking for
        match_key = key.replace(".", "").lower()

        pollutant_data = pollutants_dict.get(match_key)
        if not pollutant_data:
            return None

        # Return the most relevant concentration value
        return (
            pollutant_data.get("valueUGM3")
            or pollutant_data.get("concentrationUGM3")
            or pollutant_data.get("value")
        )

class XWeatherDominantPollutantSensor(CoordinatorEntity, SensorEntity):
    """XWeather Dominant Pollutant Sensor Entity."""

    _attr_device_class = None
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, entry):
        """Initialize the XWeather Dominant Pollutant sensor."""
        super().__init__(coordinator)
        self.entry = entry
        
        self._attr_name = f"{entry.data.get('name', DEFAULT_NAME)} Dominant Pollutant"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_dominant_pollutant"
        self._attr_icon = "mdi:air-filter"

    @property
    def device_info(self):
        """Return the device info, linking it to the main device."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
        }

    @property
    def available(self):
        """Return if the entity is available."""
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [])
        if not periods:
            return False
        return periods[0].get("dominant") is not None

    @property
    def native_value(self):
        """Return the dominant pollutant value."""
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [])
        if not periods:
            return None
        return periods[0].get("dominant")

