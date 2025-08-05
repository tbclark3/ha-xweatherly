from __future__ import annotations

from homeassistant.components.weather import (
    WeatherEntity,
    WeatherEntityFeature,
    Forecast,
)
from homeassistant.const import UnitOfTemperature, UnitOfPressure, UnitOfSpeed
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ICON_MAP

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([XWeatherWeather(coordinator, entry)], True)

class XWeatherWeather(CoordinatorEntity,WeatherEntity):
    """XWeather main weather entity."""

    _attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY | WeatherEntityFeature.FORECAST_DAILY

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry
        self._hass = coordinator.hass
        self._attr_name = entry.data.get("name", "xweather")
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self.entry.data.get("name", "XWeather"),
            "manufacturer": "XWeather",
            "model": "API",
            "entry_type": "service",
        }

    @property
    def available(self):
        return "conditions" in self.coordinator.data and bool(self.coordinator.data["conditions"])

    def _sel(self, metric, imperial):
        unit = self._hass.config.units.temperature_unit
        is_metric = unit == UnitOfTemperature.CELSIUS
        return metric if is_metric else imperial

    @property
    def native_temperature(self):
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("tempC"), p.get("tempF"))

    @property
    def native_temperature_unit(self):
        return self._sel(UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT)

    @property
    def native_pressure(self):
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("pressureMB"), p.get("pressureIN"))

    @property
    def native_pressure_unit(self):
        return self._sel(UnitOfPressure.HPA, UnitOfPressure.INHG)

    @property
    def native_wind_speed(self):
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("windSpeedMPS"), p.get("windSpeedMPH"))

    @property
    def native_wind_speed_unit(self):
        return self._sel(UnitOfSpeed.METERS_PER_SECOND, UnitOfSpeed.MILES_PER_HOUR)

    @property
    def wind_bearing(self):
        return self.coordinator.data["conditions"]["periods"][0].get("windDirDEG")

    @property
    def native_wind_gust_speed(self):
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("windGustMPS"), p.get("windGustMPH"))

    @property
    def native_wind_gust_speed_unit(self):
        return self._sel(UnitOfSpeed.METERS_PER_SECOND, UnitOfSpeed.MILES_PER_HOUR)

    @property
    def humidity(self):
        return self.coordinator.data["conditions"]["periods"][0].get("humidity")

    @property
    def native_dew_point(self):
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("dewpointC"), p.get("dewpointF"))

    @property
    def native_dew_point_unit(self):
        return self._sel(UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT)

    @property
    def native_visibility(self):
        p = self.coordinator.data["conditions"]["periods"][0]
        return self._sel(p.get("visibilityKM"), p.get("visibilityMI"))

    @property
    def native_visibility_unit(self):
        return self._sel("km", "mi")

    @property
    def condition(self):
        code = self.coordinator.data["conditions"]["periods"][0].get("weatherPrimaryCoded", "::CL").split(":")[-1]
        return ICON_MAP.get(code, "cloudy")

    def _fc_sel(self, p, key_c, key_f):
        return self._sel(p.get(key_c), p.get(key_f))

    async def async_forecast_hourly(self) -> list[Forecast]:
        fc = []
        for p in self.coordinator.data["forecast_hourly"]["periods"]:
            fc.append(
                Forecast(
                    datetime=p["dateTimeISO"],
                    temperature=self._fc_sel(p, "tempC", "tempF"),
                    precipitation=self._fc_sel(p, "precipMM", "precipIN"),
                    condition=ICON_MAP.get(p.get("weatherPrimaryCoded", "::CL").split(":")[-1], "cloudy"),
                    humidity=p.get("humidity"),
                    pressure=self._fc_sel(p, "pressureMB", "pressureIN"),
                    wind_speed=self._fc_sel(p, "windSpeedMPS", "windSpeedMPH"),
                    wind_bearing=p.get("windDirDEG"),
                    wind_gust_speed=self._fc_sel(p, "windGustMPS", "windGustMPH"),
                    dew_point=self._fc_sel(p, "dewpointC", "dewpointF"),
                    precipitation_probability=p.get("pop"),
                )
            )
        return fc

    async def async_forecast_daily(self) -> list[Forecast]:
        fc = []
        for p in self.coordinator.data["forecast_daily"]["periods"]:
            fc.append(
                Forecast(
                    datetime=p["dateTimeISO"],
                    temperature=self._fc_sel(p, "maxTempC", "maxTempF") or self._fc_sel(p, "tempC", "tempF"),
                    templow=self._fc_sel(p, "minTempC", "minTempF"),
                    precipitation=self._fc_sel(p, "precipMM", "precipIN"),
                    condition=ICON_MAP.get(p.get("weatherPrimaryCoded", "::CL").split(":")[-1], "cloudy"),
                    precipitation_probability=p.get("pop"),
                    wind_speed=self._fc_sel(p, "windSpeedMPS", "windSpeedMPH"),
                    wind_bearing=p.get("windDirDEG"),
                    humidity=p.get("humidity"),
                    dew_point=self._fc_sel(p, "dewpointC", "dewpointF"),
                )
            )
        return fc
