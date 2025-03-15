from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from smart_weather import config

ollama_model = OpenAIModel(
    model_name=config.OLLAMA_MODEL_NAME,
    provider=OpenAIProvider(base_url=config.OLLAMA_API_URL),
)

agent = Agent(
    ollama_model,
    instrument=True,
    retries=2,
    system_prompt=(
        "You are a helpful assistant responsible for alerting users about potential issues based on the given weather forecast. "
        "Warn the user about any significant weather conditions that may affect safety, travel, or daily activities. "
        "Use only the data from the provided weather forecast and avoid making assumptions."
    ),
)
