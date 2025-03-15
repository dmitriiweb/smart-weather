from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from smart_weather import config, schema

ollama_model = OpenAIModel(
    model_name=config.OLLAMA_MODEL_NAME,
    provider=OpenAIProvider(base_url=config.OLLAMA_API_URL),
)

agent = Agent(
    ollama_model,
    result_type=schema.WeatherLocationFormatResult,
    instrument=True,
    system_prompt=(
        "You are a helpful assistant for retrieving weather information for any location. "
        "Convert the user's input into a properly formatted location: 'City Name, State Code' (for US locations) or 'City Name, Country Code' (using ISO 3166 country codes). "
        "If the location contains typos, correct them before processing."
    ),
    retries=2,
)
