import httpx
from rich import print as rprint

from . import config, schema
from .agents import (
    CoordinatesGetterDeps,
    WeatherForecastDeps,
    alert_agent,
    coordinates_getter_agent,
    location_gen_agent,
    suggest_agent,
    weather_forecast_agent,
)


class App:
    def __init__(self):
        self.args = config.CliArgs.from_cli()
        self.client = httpx.AsyncClient()

    async def run(self):
        print("Getting location...", end="\r")
        location = await self._get_user_location()
        print("Getting coordinates...", end="\r")
        coordinates = await self._get_coordinates(location)
        print("Getting weather forecast...", end="\r")
        weather_forecast = await self._get_weather_forecast(
            location.city_name, coordinates
        )
        print(weather_forecast)
        print()
        print("Getting suggests...", end="\r")
        suggests = await self._get_suggests(weather_forecast)
        rprint(f"[green]{suggests}[/green]")
        print()
        print("Getting alerts...", end="\r")
        alerts = await self._get_alerts(weather_forecast)
        rprint(f"[dark_orange]{alerts}[/dark_orange]")
        print()
        await self.client.aclose()

    async def _get_weather_forecast(
        self,
        location: str,
        coordinates: schema.Coordinates,
    ) -> str:
        assert config.OPEN_WEATHER_API_KEY is not None, (
            "Please provide OPEN_WEATHER_API_KEY in the environment"
        )
        deps = WeatherForecastDeps(
            api_key=config.OPEN_WEATHER_API_KEY,
            client=self.client,
        )
        lat = coordinates.latitude
        lon = coordinates.longitude
        result = await weather_forecast_agent.run(
            f"make weather forecast for {location}, lat: {lat}, lon: {lon}", deps=deps
        )
        return result.data

    async def _get_user_location(self) -> schema.WeatherLocationFormatResult:
        location = await location_gen_agent.run(self.args.location)
        return location.data

    async def _get_coordinates(
        self, location: schema.WeatherLocationFormatResult
    ) -> schema.Coordinates:
        assert config.OPEN_WEATHER_API_KEY is not None, (
            "Please provide OPEN_WEATHER_API_KEY in the environment"
        )
        deps = CoordinatesGetterDeps(
            client=self.client,
            api_key=config.OPEN_WEATHER_API_KEY,
            json_path=config.CACHE_JSON_PATH,
        )
        coordinates = await coordinates_getter_agent.run(str(location), deps=deps)
        return coordinates.data

    async def _get_suggests(self, weather_forecast: str) -> str:
        suggests = await suggest_agent.run(weather_forecast)
        return suggests.data

    async def _get_alerts(self, weather_forecast: str) -> str:
        alerts = await alert_agent.run(weather_forecast)
        return alerts.data
