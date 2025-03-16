from dataclasses import dataclass
from pathlib import Path

import aiofiles
import httpx
import json
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from smart_weather import config, schema


@dataclass
class Deps:
    client: httpx.AsyncClient
    api_key: str
    json_path: Path


ollama_model = OpenAIModel(
    model_name=config.OLLAMA_MODEL_NAME,
    provider=OpenAIProvider(base_url=config.OLLAMA_API_URL),
)

agent = Agent(
    ollama_model,
    result_type=schema.Coordinates,
    instrument=True,
    deps_type=Deps,
    system_prompt=(
        "You are a helpful assistant for retrieving coordinates based on a city and country. "
        "First, check the cache for the coordinates. If they are not found, fetch them from the OpenWeather API."
    ),
    retries=2,
)


@agent.tool
async def get_coordinates_from_api(
    ctx: RunContext[Deps], user_location: str
) -> schema.Coordinates:
    """Get a latitude and longitude from the Open Weather API by city and country

    Args:
        ctx: The context of the run
        user_location: The location to get the coordinates, e.g. "London,GB"

    Returns:
        dataclass with latitude and longitude fields
    """
    # logger.debug(f"Getting coordinates from the Open Weather API for {user_location}")
    api_key = ctx.deps.api_key
    client = ctx.deps.client
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={user_location}&limit=1&appid={api_key}"
    response = await client.get(url)
    # logger.debug(f"{response.json()}")
    res = response.json()
    result = schema.Coordinates(latitude=res[0]["lat"], longitude=res[0]["lon"])
    await update_cache(user_location, result, ctx.deps.json_path)
    return result


@agent.tool
async def get_coordinates_from_cache(
    ctx: RunContext[Deps], user_location: str
) -> schema.Coordinates | None:
    """Get a latitude and longitude from the cache in json file

    Args:
        ctx: The context of the run
        user_location: The location to get the coordinates, e.g. "London,GB"

    Returns:
        dataclass with latitude and longitude fields or None if not found
    """
    # logger.debug(f"Getting coordinates from the cache for {user_location}")
    file_path = ctx.deps.json_path
    if not file_path.exists():
        return None
    async with aiofiles.open(file_path, mode="r") as f:
        content = await f.read()
        cache = json.loads(content)

    if user_location in cache:
        coordinates = cache[user_location]
        return schema.Coordinates(
            latitude=coordinates["lat"], longitude=coordinates["lon"]
        )
    return None


async def update_cache(location: str, coordinates: schema.Coordinates, file_path: Path) -> None:
    """Update the cache with the new coordinates

    Args:
        location: The location to update in the cache
        coordinates: The latitude and longitude to update in the cache
        file_path: The path to the json file
    """
    cache = {}
    if file_path.exists():
        async with aiofiles.open(file_path, mode="r") as f:
            content = await f.read()
            cache = json.loads(content)

    cache[location] = {"lat": coordinates.latitude, "lon": coordinates.longitude}

    async with aiofiles.open(file_path, mode="w") as f:
        await f.write(json.dumps(cache))
