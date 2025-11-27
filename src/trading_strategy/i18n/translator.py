"""
Simple JSON-based internationalization system.

This module provides a lightweight i18n solution without heavy frameworks:
- JSON files for each locale (en.json, zh_CN.json, etc.)
- Simple key-value lookup with Python string formatting
- Easy to add new languages

Design philosophy:
- Keep it simple for MVP (English only)
- Structure for easy expansion (Chinese support planned)
- No compilation or complex tooling
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class Translator:
    """
    Translator for internationalization.

    Loads messages from JSON files in the locales directory.
    Supports Python format string placeholders.

    Example:
        t = Translator('en')
        msg = t.get('buy_signal.title', stock='AAPL')
    """

    def __init__(self, locale: str, locale_dir: Path):
        """
        Initialize translator.

        Args:
            locale: Language code (e.g., 'en', 'zh_CN')
            locale_dir: Directory containing locale JSON files
        """
        self.locale = locale
        self.locale_dir = locale_dir
        self.messages = self._load_messages()

    def _load_messages(self) -> Dict[str, Any]:
        """Load messages from JSON file."""
        locale_file = self.locale_dir / f"{self.locale}.json"

        if not locale_file.exists():
            logger.error(f"Locale file not found: {locale_file}")
            logger.info("Falling back to English")
            locale_file = self.locale_dir / "en.json"

        try:
            with open(locale_file, "r", encoding="utf-8") as f:
                messages = json.load(f)
            logger.info(f"Loaded messages for locale: {self.locale}")
            return messages

        except Exception as e:
            logger.error(f"Error loading locale file {locale_file}: {e}")
            return {}

    def get(self, key: str, **kwargs) -> str:
        """
        Get translated message with optional formatting.

        Args:
            key: Message key (dot-notation, e.g., 'buy_signal.title')
            **kwargs: Format arguments for string interpolation

        Returns:
            Translated and formatted message

        Example:
            t.get('buy_signal.title', stock='AAPL')
        """
        try:
            # Navigate nested dictionary using dot notation
            parts = key.split(".")
            value = self.messages

            for part in parts:
                value = value[part]

            # Format with provided arguments
            if isinstance(value, str):
                return value.format(**kwargs)
            else:
                return str(value)

        except (KeyError, IndexError) as e:
            logger.error(f"Translation key not found: {key}")
            return f"[Missing: {key}]"

        except Exception as e:
            logger.error(f"Error formatting message {key}: {e}")
            return f"[Error: {key}]"

    def get_raw(self, key: str) -> Any:
        """
        Get raw value without formatting.

        Useful for getting lists, dicts, or other non-string values.
        """
        try:
            parts = key.split(".")
            value = self.messages

            for part in parts:
                value = value[part]

            return value

        except (KeyError, IndexError):
            logger.error(f"Translation key not found: {key}")
            return None
