from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    UnitOfPressure,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    UnitOfSpeed,
)
from homeassistant.helpers.entity import EntityCategory
from .const import DOMAIN

SENSORS = [
    ("tempC", "Temperature", UnitOfTemperature.CELSIUS),
    ("feelslikeC", "Feels Like", UnitOfTemperature.CELSIUS),
    ("dewpointC", "Dewpoint", UnitOfTemperature.CELSIUS),
    ("humidity", "Humidity", PERCENTAGE),
    ("pressureMB", "Pressure", UnitOfPressure.HPA),
    ("windSpeedMPS", "Wind Speed", UnitOfSpeed.METERS_PER_SECOND),
    ("windGustMPS", "Wind Gust Speed", UnitOfSpeed.METERS_PER_SECOND),
    ("windDirDEG", "Wind Direction", "°"),
    ("uvi", "UV Index", None),
    ("visibilityKM", "Visibility", "km"),
    ("precipMM", "Precipitation", "mm"),
    ("solradWM2", "Solar Radiation", "W/m²"),
]

POLLUTANTS = {
    "o3": "O3",
    "pm2.5": "PM2.5",
    "pm10": "PM10",
    "co": "CO",
    "no2": "NO2",
    "so2": "SO2",
}

def _alt_unit(unit):
    return (
        UnitOfTemperature.FAHRENHEIT if unit == UnitOfTemperature.CELSIUS else
        UnitOfPressure.INHG if unit == UnitOfPressure.HPA else
        UnitOfSpeed.MILES_PER_HOUR if unit == UnitOfSpeed.METERS_PER_SECOND else
        "in" if unit == "mm" else
        "mi" if unit == "km" else
        unit
    )

def _imperial_key(key):
    return (
        key.replace("C", "F")
        if "C" in key else key.replace("MPS", "MPH")
        if "MPS" in key else key.replace("KM", "MI")
        if "KM" in key else key.replace("MM", "IN")
        if "MM" in key else key
    )


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for key, name, unit in SENSORS:
        entities.append(
            XWeatherSensor(
                coordinator,
                entry,
                key,
                name,
                unit,
                source="conditions",
                key_override=key,
            )
        )

    for key, display in POLLUTANTS.items():
        safe_key = key.replace(".", "").replace(" ", "_").lower()
        entities.append(
            XWeatherPollutantSensor(
                coordinator,
                entry,
                key,
                f"{display} Concentration",
                CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
                key_override=safe_key,
            )
        )

    entities.append(XWeatherAqiSensor(coordinator, entry))

    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted High Temperature Today",
            key_metric="maxTempC",
            key_imperial="maxTempF",
            unit_metric=UnitOfTemperature.CELSIUS,
            unit_imperial=UnitOfTemperature.FAHRENHEIT,
            day_offset=0,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Low Temperature Today",
            key_metric="minTempC",
            key_imperial="minTempF",
            unit_metric=UnitOfTemperature.CELSIUS,
            unit_imperial=UnitOfTemperature.FAHRENHEIT,
            day_offset=0,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Rain Amount Today",
            key_metric="precipMM",
            key_imperial="precipIN",
            unit_metric="mm",
            unit_imperial="in",
            day_offset=0,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Rain Probability Today",
            key_metric="pop",  
            key_imperial="pop",
            unit_metric=PERCENTAGE,
            unit_imperial=PERCENTAGE,
            day_offset=0,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Wind Speed Today",
            key_metric="windSpeedKPH",
            key_imperial="windSpeedMPH",
            unit_metric=UnitOfSpeed.KILOMETERS_PER_HOUR,
            unit_imperial=UnitOfSpeed.MILES_PER_HOUR,
            day_offset=0,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Humidity Today",
            key_metric="humidity", 
            key_imperial="humidity",
            unit_metric=PERCENTAGE,
            unit_imperial=PERCENTAGE,
            day_offset=0,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Average Temperature Today",
            key_metric="avgTempC",
            key_imperial="avgTempF",
            unit_metric=UnitOfTemperature.CELSIUS,
            unit_imperial=UnitOfTemperature.FAHRENHEIT,
            day_offset=0,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Snowfall Today",
            key_metric="snowCM",
            key_imperial="snowIN",
            unit_metric="cm",
            unit_imperial="in",
            day_offset=0,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Cloud Cover Today",
            key_metric="sky",
            key_imperial="sky",
            unit_metric=PERCENTAGE,
            unit_imperial=PERCENTAGE,
            day_offset=0,
        )
    )

    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted High Temperature Tomorrow",
            key_metric="maxTempC",
            key_imperial="maxTempF",
            unit_metric=UnitOfTemperature.CELSIUS,
            unit_imperial=UnitOfTemperature.FAHRENHEIT,
            day_offset=1,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Low Temperature Tomorrow",
            key_metric="minTempC",
            key_imperial="minTempF",
            unit_metric=UnitOfTemperature.CELSIUS,
            unit_imperial=UnitOfTemperature.FAHRENHEIT,
            day_offset=1,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Rain Amount Tomorrow",
            key_metric="precipMM",
            key_imperial="precipIN",
            unit_metric="mm",
            unit_imperial="in",
            day_offset=1,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Rain Probability Tomorrow",
            key_metric="pop",
            key_imperial="pop",
            unit_metric=PERCENTAGE,
            unit_imperial=PERCENTAGE,
            day_offset=1,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Wind Speed Tomorrow",
            key_metric="windSpeedKPH",
            key_imperial="windSpeedMPH",
            unit_metric=UnitOfSpeed.KILOMETERS_PER_HOUR,
            unit_imperial=UnitOfSpeed.MILES_PER_HOUR,
            day_offset=1,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Humidity Tomorrow",
            key_metric="humidity",
            key_imperial="humidity",
            unit_metric=PERCENTAGE,
            unit_imperial=PERCENTAGE,
            day_offset=1,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Average Temperature Tomorrow",
            key_metric="avgTempC",
            key_imperial="avgTempF",
            unit_metric=UnitOfTemperature.CELSIUS,
            unit_imperial=UnitOfTemperature.FAHRENHEIT,
            day_offset=1,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Snowfall Tomorrow",
            key_metric="snowCM",
            key_imperial="snowIN",
            unit_metric="cm",
            unit_imperial="in",
            day_offset=1,
        )
    )
    entities.append(
        XWeatherForecastSensor(
            coordinator,
            entry,
            name="Predicted Cloud Cover Tomorrow",
            key_metric="sky",
            key_imperial="sky",
            unit_metric=PERCENTAGE,
            unit_imperial=PERCENTAGE,
            day_offset=1,
        )
    )


    async_add_entities(entities, True)


class XWeatherBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for XWeather sensors with device info."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self.entry.data.get("name", "XWeather"),
            "manufacturer": "XWeather",
            "model": "API",
            "entry_type": "service",
        }

class XWeatherSensor(XWeatherBaseSensor):
    """Standard weather sensor with dynamic unit selection."""

    def __init__(self, coordinator, entry, key, name, unit, source, key_override=None):
        super().__init__(coordinator, entry)
        self.key = key
        self.key_override = key_override or key
        self.source = source
        self.name_field = name
        self._unit_metric = unit
        self._unit_imperial = _alt_unit(unit)
        self._attr_name = f"{entry.data.get('name','xweather')} {name}"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{self.key_override}"

    def _sel(self, metric, imperial):
        unit = self.coordinator.hass.config.units.temperature_unit
        is_metric = unit == UnitOfTemperature.CELSIUS
        return metric if is_metric else imperial

    @property
    def available(self):
        data = self.coordinator.data.get(self.source, {})
        periods = data.get("periods", [])
        if not periods:
            return False
        metric_val = periods[0].get(self.key)
        imperial_val = periods[0].get(_imperial_key(self.key))
        return (metric_val is not None or imperial_val is not None)

    @property
    def native_value(self):
        data = self.coordinator.data.get(self.source, {})
        periods = data.get("periods", [{}])
        period = periods[0] if periods else {}
        metric_val = period.get(self.key)
        imperial_val = period.get(_imperial_key(self.key))
        return self._sel(metric_val, imperial_val)

    @property
    def native_unit_of_measurement(self):
        return self._sel(self._unit_metric, self._unit_imperial)

class XWeatherPollutantSensor(XWeatherBaseSensor):
    """Pollutant sensor for XWeather."""

    def __init__(self, coordinator, entry, pollutant_key, name, unit, key_override=None):
        super().__init__(coordinator, entry)
        self.pollutant_key = pollutant_key
        self._attr_name = f"{entry.data.get('name','xweather')} {name}"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key_override or pollutant_key}"
        self._attr_native_unit_of_measurement = unit

    @property
    def available(self):
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [])
        if not periods:
            return False
        for pol in periods[0].get("pollutants", []):
            pol_key = pol.get("type") or pol.get("name", "").lower()
            if not pol_key:
                continue
            norm = pol_key.replace(".", "").replace(" ", "").lower()
            match = self.pollutant_key.replace(".", "").lower()
            if norm == match and (pol.get("valueUGM3") or pol.get("concentrationUGM3") or pol.get("value")) is not None:
                return True
        return False

    @property
    def native_value(self):
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [{}])
        if not periods:
            return None
        for pol in periods[0].get("pollutants", []):
            key = pol.get("type") or pol.get("name", "").lower()
            if not key:
                continue
            norm = key.replace(".", "").replace(" ", "").lower()
            match = self.pollutant_key.replace(".", "").lower()
            if norm == match:
                return (
                    pol.get("valueUGM3")
                    or pol.get("concentrationUGM3")
                    or pol.get("value")
                )
        return None

class XWeatherAqiSensor(XWeatherBaseSensor):
    """AQI sensor for XWeather."""

    _attr_native_unit_of_measurement = None

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_name = f"{entry.data.get('name', 'xweather')} Air Quality Index"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_aqi"
        self._attr_icon = "mdi:air-filter"

    @property
    def available(self):
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [])
        if not periods:
            return False
        return periods[0].get("aqi") is not None

    @property
    def native_value(self):
        aq = self.coordinator.data.get("airquality", {})
        periods = aq.get("periods", [{}])
        return periods[0].get("aqi") if periods else None


class XWeatherForecastSensor(XWeatherBaseSensor):
    """Forecast sensor for XWeather with dynamic unit selection."""

    def __init__(self, coordinator, entry, name, key_metric, key_imperial, unit_metric, unit_imperial, day_offset):
        super().__init__(coordinator, entry)
        self.key_metric = key_metric
        self.key_imperial = key_imperial
        self.day_offset = day_offset

        self._unit_metric = unit_metric
        self._unit_imperial = unit_imperial

        self._attr_name = f"{entry.data.get('name', 'xweather')} {name}"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{name.replace(' ', '_').lower()}"

    def _sel(self, metric, imperial):
        unit = self.coordinator.hass.config.units.temperature_unit
        is_metric = unit == UnitOfTemperature.CELSIUS
        return metric if is_metric else imperial

    @property
    def native_value(self):
        forecast_data = self.coordinator.data.get("forecast_daily", {})
        periods = forecast_data.get("periods", [])
        if len(periods) > self.day_offset:
            period = periods[self.day_offset]
            metric_val = period.get(self.key_metric)
            imperial_val = period.get(self.key_imperial)
            return self._sel(metric_val, imperial_val)
        return None

    @property
    def native_unit_of_measurement(self):
        return self._sel(self._unit_metric, self._unit_imperial)

    @property
    def available(self):
        forecast_data = self.coordinator.data.get("forecast_daily", {})
        periods = forecast_data.get("periods", [])
        if len(periods) > self.day_offset:
            period = periods[self.day_offset]
            return period.get(self.key_metric) is not None or period.get(self.key_imperial) is not None
        return False
