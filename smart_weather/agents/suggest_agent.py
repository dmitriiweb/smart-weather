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
        "You are a helpful assistant providing clothing and activity recommendations based on the given weather forecast. "
        "Suggest appropriate attire and the best activities suited for the weather conditions. "
        "Use only the data from the provided weather forecast and avoid making assumptions."
    ),
)
