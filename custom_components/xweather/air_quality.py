from __future__ import annotations

from homeassistant.components.air_quality import AirQualityEntity
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, DEFAULT_NAME


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([XWeatherAirQuality(coordinator, entry)], True)


class XWeatherAirQuality(CoordinatorEntity, AirQualityEntity):
    """XWeather Air Quality Entity."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry
        # Correctly uses DEFAULT_NAME as a fallback
        self._attr_name = f"{entry.data.get('name', DEFAULT_NAME)} Air Quality"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_airquality"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            # Hardcodes the name to the default as requested
            "name": DEFAULT_NAME,
            "manufacturer": DEFAULT_NAME,
            "model": "API",
            "entry_type": "service",
        }

    @property
    def available(self):
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [])
        if not periods:
            return False
        return periods[0].get("aqi") is not None

    @property
    def native_air_quality_index(self):
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [])
        if not periods:
            return None
        return periods[0].get("aqi")

    @property
    def attribution(self):
        return "Data provided by XWeather"

    @property
    def extra_state_attributes(self):
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [{}])
        if not periods:
            return {}
        period = periods[0]
        return {
            "aqi_category": period.get("category"),
            "dominant_pollutant": period.get("dominant"),
            "health_index": period.get("health", {}).get("index"),
            "health_category": period.get("health", {}).get("category"),
        }

    @property
    def co(self):
        return self._get_pollutant("co")

    @property
    def no2(self):
        return self._get_pollutant("no2")

    @property
    def o3(self):
        return self._get_pollutant("o3")

    @property
    def so2(self):
        return self._get_pollutant("so2")

    @property
    def particulate_matter_10(self):
        return self._get_pollutant("pm10")

    @property
    def particulate_matter_2_5(self):
        return self._get_pollutant("pm2.5")

    @property
    def co_unit(self):
        return CONCENTRATION_PARTS_PER_MILLION

    @property
    def no2_unit(self):
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def o3_unit(self):
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def so2_unit(self):
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def particulate_matter_10_unit(self):
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    @property
    def particulate_matter_2_5_unit(self):
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER

    def _get_pollutant(self, key: str):
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [{}])
        if not periods:
            return None
        for pol in periods[0].get("pollutants", []):
            pol_key = pol.get("type") or pol.get("name", "").lower()
            if not pol_key:
                continue
            norm = pol_key.replace(".", "").replace(" ", "").lower()
            match = key.replace(".", "").lower()
            if norm == match:
                return (
                    pol.get("valueUGM3")
                    or pol.get("concentrationUGM3")
                    or pol.get("value")
                )
        return None
