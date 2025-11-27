"""
Settings management using Pydantic for environment variables and configuration.

This module provides a centralized configuration system that:
- Loads settings from environment variables
- Provides defaults for optional settings
- Validates configuration at startup
- Supports both local (.env) and GitHub Actions (secrets) environments
"""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Required settings:
        - TELEGRAM_BOT_TOKEN: Bot token from @BotFather
        - TELEGRAM_CHAT_ID: Your Telegram chat ID

    Optional settings:
        - ALPHA_VANTAGE_API_KEY: Backup data source (not needed for MVP)
        - LOCALE: Language for notifications (default: en)
        - TIMEZONE: Timezone for logging (default: America/New_York)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Telegram configuration (required)
    telegram_bot_token: str = Field(
        ..., description="Telegram bot token from @BotFather"
    )
    telegram_chat_id: str = Field(..., description="Telegram chat ID for notifications")

    # Optional API keys
    alpha_vantage_api_key: Optional[str] = Field(
        None, description="Alpha Vantage API key (backup data source)"
    )

    # Localization
    locale: str = Field(default="en", description="Language for notifications (en, zh_CN)")

    # Timezone
    timezone: str = Field(
        default="America/New_York", description="Timezone for timestamps (ET/EDT)"
    )

    # Project paths
    @property
    def project_root(self) -> Path:
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent.parent

    @property
    def state_file(self) -> Path:
        """Get the path to the signals state file."""
        return self.project_root / "signals.json"

    @property
    def locale_dir(self) -> Path:
        """Get the directory containing locale files."""
        return Path(__file__).parent.parent / "i18n" / "locales"


# Singleton instance
settings = Settings()
