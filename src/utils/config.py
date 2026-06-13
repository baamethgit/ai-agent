"""Application configuration loaded from environment variables.

Uses pydantic-settings: raises a clear ValidationError at startup
if any required variable is missing or has the wrong type.

Usage:
    from src.utils.config import settings
    print(settings.groq_model)
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Langfuse ---
    langfuse_secret_key: str = Field(..., alias="LANGFUSE_SECRET_KEY")
    langfuse_public_key: str = Field(..., alias="LANGFUSE_PUBLIC_KEY")
    langfuse_base_url: str = Field("https://us.cloud.langfuse.com", alias="LANGFUSE_BASE_URL")
    langfuse_prompt: str = Field("", alias="LANGFUSE_PROMPT")

    # --- GroqCloud ---
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    groq_base_url: str = Field("https://api.groq.com/openai/v1", alias="GROQ_BASE_URL")
    groq_model: str = Field(..., alias="GROQ_MODEL")
    groq_temperature: float = Field(0.5, alias="GROQ_TEMPERATURE")


def _load_settings() -> Settings:
    try:
        return Settings()
    except Exception as exc:
        from src.utils.logger import logger
        logger.error("Configuration error — check your .env file:\n{}", exc)
        raise SystemExit(1) from exc


settings: Settings = _load_settings()

__all__ = ["settings"]
