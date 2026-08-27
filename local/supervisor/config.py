"""Configuration management for supervisor agent."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Handle Pydantic v2 compatibility
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    # Fallback to Pydantic v1
    from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    # Qwen Proxy Configuration
    anthropic_base_url: str = Field(
        default="https://llmproxy.gupshup.io/",
        env="ANTHROPIC_BASE_URL"
    )
    anthropic_auth_token: str = Field(
        env="ANTHROPIC_AUTH_TOKEN"
    )
    anthropic_model: str = Field(
        default="Qwen3-Coder-480B",
        env="ANTHROPIC_MODEL"
    )
    anthropic_temperature: float = Field(
        default=0.3,
        env="ANTHROPIC_TEMPERATURE"
    )
    anthropic_max_tokens: int = Field(
        default=1500,
        env="ANTHROPIC_MAX_TOKENS"
    )

    # Langfuse Configuration (for trace fetching)
    langfuse_public_key: Optional[str] = Field(
        default=None,
        env="LANGFUSE_PUBLIC_KEY"
    )
    langfuse_secret_key: Optional[str] = Field(
        default=None,
        env="LANGFUSE_SECRET_KEY"
    )
    langfuse_host: str = Field(
        default="https://cloud.langfuse.com",
        env="LANGFUSE_HOST"
    )

    # Paths
    reports_dir: Path = Field(
        default=Path("local/reports"),
        env="REPORTS_DIR"
    )
    cache_dir: Path = Field(
        default=Path("local/cache"),
        env="CACHE_DIR"
    )
    logs_dir: Path = Field(
        default=Path("local/supervisor/logs"),
        env="LOGS_DIR"
    )

    # Analysis Parameters
    max_gaps: int = Field(
        default=10,
        env="MAX_GAPS"
    )
    min_severity: float = Field(
        default=0.0,
        env="MIN_SEVERITY"
    )

    # LLM Configuration
    qwen_timeout_seconds: int = Field(
        default=60,
        env="QWEN_TIMEOUT_SECONDS"
    )

    class Config:
        """Pydantic config."""
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra fields from .env file


def load_config() -> Settings:
    """Load configuration from environment variables.

    Respects .env file and environment variables with override priority.
    Use override=True to allow environment variables to override .env values.
    """
    # Load .env with override to respect environment variables set by Docker/shell
    load_dotenv(override=True)

    return Settings()


def ensure_directories(config: Settings) -> None:
    """Create necessary directories if they don't exist."""
    for directory in [config.reports_dir, config.cache_dir, config.logs_dir]:
        directory.mkdir(parents=True, exist_ok=True)
