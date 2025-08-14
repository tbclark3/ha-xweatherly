from __future__ import annotations

from homeassistant.components.weather import (
    WeatherEntity,
    WeatherEntityFeature,
    Forecast,
)
from homeassistant.const import UnitOfTemperature, UnitOfPressure, UnitOfSpeed
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ICON_MAP, DEFAULT_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Xweatherly weather entity."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([XweatherlyWeather(coordinator, entry)], True)

class XweatherlyWeather(CoordinatorEntity,WeatherEntity):
    """Xweatherly main weather entity."""

    _attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY | WeatherEntityFeature.FORECAST_DAILY

    def __init__(self, coordinator, entry):
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entry = entry
        self._hass = coordinator.hass
        self._attr_name = entry.data.get("name", DEFAULT_NAME)
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}"

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self.entry.data.get("name", DEFAULT_NAME),
            "manufacturer": DEFAULT_NAME,
            "model": "API",
            "entry_type": "service",
        }

    @property
    def available(self):
        """Return if the entity is available."""
        return "conditions" in self.coordinator.data and bool(self.coordinator.data["conditions"])

    def _sel(self, metric, imperial):
        """Select metric or imperial value based on Hass configuration."""
        unit = self._hass.config.units.temperature_unit
        is_metric = unit == UnitOfTemperature.CELSIUS
        return metric if is_metric else imperial

    @property
    def native_temperature(self):
        """Return the temperature in native units."""
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("tempC"), p.get("tempF"))

    @property
    def native_temperature_unit(self):
        """Return the native temperature unit."""
        return self._sel(UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT)

    @property
    def native_pressure(self):
        """Return the pressure in native units."""
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("pressureMB"), p.get("pressureIN"))

    @property
    def native_pressure_unit(self):
        """Return the native pressure unit."""
        return self._sel(UnitOfPressure.HPA, UnitOfPressure.INHG)

    @property
    def native_wind_speed(self):
        """Return the wind speed in native units."""
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("windSpeedMPS"), p.get("windSpeedMPH"))

    @property
    def native_wind_speed_unit(self):
        """Return the native wind speed unit."""
        return self._sel(UnitOfSpeed.METERS_PER_SECOND, UnitOfSpeed.MILES_PER_HOUR)

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return self.coordinator.data["conditions"]["periods"][0].get("windDirDEG")

    @property
    def native_wind_gust_speed(self):
        """Return the wind gust speed in native units."""
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("windGustMPS"), p.get("windGustMPH"))

    @property
    def native_wind_gust_speed_unit(self):
        """Return the native wind gust speed unit."""
        return self._sel(UnitOfSpeed.METERS_PER_SECOND, UnitOfSpeed.MILES_PER_HOUR)

    @property
    def humidity(self):
        """Return the humidity."""
        return self.coordinator.data["conditions"]["periods"][0].get("humidity")

    @property
    def native_dew_point(self):
        """Return the dew point in native units."""
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("dewpointC"), p.get("dewpointF"))

    @property
    def native_dew_point_unit(self):
        """Return the native dew point unit."""
        return self._sel(UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT)

    @property
    def native_visibility(self):
        """Return the visibility in native units."""
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("visibilityKM"), p.get("visibilityMI"))

    @property
    def native_visibility_unit(self):
        """Return the native visibility unit."""
        return self._sel("km", "mi")

    @property
    def condition(self):
        """Return the current weather condition."""
        p = self.coordinator.data["conditions"]["periods"][0]
        code = p.get("weatherPrimaryCoded", "::CL").split(":")[-1]
        is_day = p.get("isDay", True)
    
        if code == "SC" and not is_day:
            return ICON_MAP.get("SC-N", "cloudy")
        
        if code == "CL" and not is_day:
            return ICON_MAP.get("CL-N", "cloudy")
    
        return ICON_MAP.get(code, "cloudy")

    def _get_forecast_value(self, p, key_c, key_f):
        """Get the correct forecast value based on user's units."""
        unit = self._hass.config.units.temperature_unit
        is_metric = unit == UnitOfTemperature.CELSIUS
        return p.get(key_c) if is_metric else p.get(key_f)

    async def async_forecast_hourly(self) -> list[Forecast]:
        """Return the hourly forecast."""
        fc = []
        for p in self.coordinator.data["forecast_hourly"]["periods"]:
            code = p.get("weatherPrimaryCoded", "::CL").split(":")[-1]
            is_day = p.get("isDay", True)
            
            if code == "SC" and not is_day:
                condition_key = "SC-N"
            elif code == "CL" and not is_day:
                condition_key = "CL-N"
            else:
                condition_key = code
            
            fc.append(
                Forecast(
                    datetime=p["dateTimeISO"],
                    temperature=self._get_forecast_value(p, "tempC", "tempF"),
                    precipitation=self._get_forecast_value(p, "precipMM", "precipIN"),
                    condition=ICON_MAP.get(condition_key, "cloudy"),
                    humidity=p.get("humidity"),
                    pressure=self._get_forecast_value(p, "pressureMB", "pressureIN"),
                    wind_speed=self._get_forecast_value(p, "windSpeedMPS", "windSpeedMPH"),
                    wind_bearing=p.get("windDirDEG"),
                    wind_gust_speed=self._get_forecast_value(p, "windGustMPS", "windGustMPH"),
                    dew_point=self._get_forecast_value(p, "dewpointC", "dewpointF"),
                    precipitation_probability=p.get("pop"),
                )
            )
        return fc

    async def async_forecast_daily(self) -> list[Forecast]:
        """Return the daily forecast."""
        fc = []
        for p in self.coordinator.data["forecast_daily"]["periods"]:
            code = p.get("weatherPrimaryCoded", "::CL").split(":")[-1]
            is_day = p.get("isDay", True)
            
            if code == "SC" and not is_day:
                condition_key = "SC-N"
            elif code == "CL" and not is_day:
                condition_key = "CL-N"
            else:
                condition_key = code

            fc.append(
                Forecast(
                    datetime=p["dateTimeISO"],
                    temperature=self._get_forecast_value(p, "maxTempC", "maxTempF") or self._get_forecast_value(p, "tempC", "tempF"),
                    templow=self._get_forecast_value(p, "minTempC", "minTempF"),
                    precipitation=self._get_forecast_value(p, "precipMM", "precipIN"),
                    condition=ICON_MAP.get(condition_key, "cloudy"),
                    precipitation_probability=p.get("pop"),
                    wind_speed=self._get_forecast_value(p, "windSpeedMPS", "windSpeedMPH"),
                    wind_bearing=p.get("windDirDEG"),
                    humidity=p.get("humidity"),
                    dew_point=self._get_forecast_value(p, "dewpointC", "dewpointF"),
                )
            )
        return fc
