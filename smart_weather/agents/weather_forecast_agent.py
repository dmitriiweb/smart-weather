import datetime as dt
from dataclasses import dataclass

import httpx
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from typing_extensions import Any

from smart_weather import config


@dataclass
class Deps:
    client: httpx.AsyncClient
    api_key: str
    time_now: str = dt.datetime.now().strftime("%H:%M")


ollama_model = OpenAIModel(
    model_name=config.OLLAMA_MODEL_NAME,
    provider=OpenAIProvider(base_url=config.OLLAMA_API_URL),
)

agent = Agent(
    ollama_model,
    instrument=True,
    deps_type=Deps,
    system_prompt=(
        "Retrieve weather data from the OpenWeather API using the `get_weather` tool. "
        "Start your response with the location name. "
        "Provide a brief weather description using only the metric system. "
        "Use only the data from the OpenWeather API response. "
        "Consider time of day. "
    ),
    retries=2,
)


@agent.system_prompt
async def add_time_now(ctx: RunContext[Deps]) -> str:
    return f"Now is {ctx.deps.time_now}"


@agent.tool
async def get_weather(ctx: RunContext[Deps], lat: float, lon: float) -> dict[str, Any]:
    """Get the weather from the Open Weather API by latitude and longitude

    Args:
        ctx: The context of the run
        lat: The latitude of the location
        lon: The longitude of the location

    Returns:
        dictionary object with the weather data
    """
    client = ctx.deps.client
    api_key = ctx.deps.api_key
    url = f"https://pro.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = await client.get(url)
    data = response.json()
    data = _convert_kelvin_to_celsius(data)
    return data


def _convert_kelvin_to_celsius(data: dict[str, Any]) -> dict[str, Any]:
    target_fields = ("temp", "feels_like", "temp_min", "temp_max")
    for field in target_fields:
        data["main"][field] -= 273.15
    return data
