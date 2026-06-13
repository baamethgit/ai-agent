"""GroqCloud LLM via OpenAI-compatible endpoint.

Groq exposes an OpenAI-compatible API, so we use langchain-openai's
ChatOpenAI and simply override base_url + api_key.

Docs: https://console.groq.com/docs/openai

Usage:
    from src.model.groqcloud import build_llm

    llm = build_llm()
    response = llm.invoke("Dis-moi bonjour en wolof.")
"""

from langchain_openai import ChatOpenAI

from src.utils.config import settings
from src.utils.logger import logger


def build_llm(
    model: str | None = None,
    temperature: float | None = None,
    **kwargs,
) -> ChatOpenAI:
    """Instantiate a ChatOpenAI client pointed at GroqCloud.

    Args:
        model: Override the model name from settings.
        temperature: Override the temperature from settings.
        **kwargs: Extra arguments forwarded to ChatOpenAI.

    Returns:
        A ready-to-use ChatOpenAI instance.
    """
    resolved_model = model or settings.groq_model
    resolved_temp = temperature if temperature is not None else settings.groq_temperature

    logger.info("Building GroqCloud LLM | model={} | temperature={}", resolved_model, resolved_temp)

    return ChatOpenAI(
        model=resolved_model,
        temperature=resolved_temp,
        api_key=settings.groq_api_key,
        base_url=settings.groq_base_url,
        **kwargs,
    )


__all__ = ["build_llm"]
