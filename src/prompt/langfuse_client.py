"""Langfuse client + LangChain prompt management.

Initialises the Langfuse client from env vars and exposes helpers to:
  - fetch a versioned prompt by name
  - convert it into a LangChain ChatPromptTemplate
  - get the LangChain callback handler for tracing

Docs: https://langfuse.com/guides/cookbook/prompt_management_langchain

Usage:
    from src.prompt.langfuse_client import get_langchain_prompt, callback_handler

    prompt_template = get_langchain_prompt("my-prompt")
    chain = prompt_template | llm
    response = chain.invoke({...}, config={"callbacks": [callback_handler]})
"""

from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langchain_core.prompts import ChatPromptTemplate

from src.utils.config import settings
from src.utils.logger import logger

# Module-level singletons — initialised once at import time.
_langfuse = get_client()
callback_handler = CallbackHandler(
    secret_key=settings.langfuse_secret_key,
    public_key=settings.langfuse_public_key,
    host=settings.langfuse_base_url,
)

logger.info("Langfuse client ready | host={}", settings.langfuse_base_url)


def get_langchain_prompt(
    prompt_name: str,
    label: str = "production",
) -> ChatPromptTemplate:
    """Fetch a Langfuse prompt and return a LangChain ChatPromptTemplate.

    Args:
        prompt_name: The name of the prompt in Langfuse Prompt Management.
        label: The label / version to fetch (default: ``"production"``).

    Returns:
        A ChatPromptTemplate with the Langfuse prompt linked as metadata.
    """
    logger.debug("Fetching Langfuse prompt '{}' (label={})", prompt_name, label)

    langfuse_prompt = _langfuse.get_prompt(prompt_name, label=label)

    template = ChatPromptTemplate.from_template(
        langfuse_prompt.get_langchain_prompt(),
        metadata={"langfuse_prompt": langfuse_prompt},
    )

    logger.info("Prompt '{}' loaded successfully", prompt_name)
    return template


def get_client_instance():
    """Return the raw Langfuse client for advanced usage (traces, scores, etc.)."""
    return _langfuse


__all__ = ["get_langchain_prompt", "get_client_instance", "callback_handler"]
