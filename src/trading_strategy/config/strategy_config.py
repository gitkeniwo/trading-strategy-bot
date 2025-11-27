"""
Strategy configuration and description loader.

Loads strategy metadata from YAML for use in notifications and documentation.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

import yaml

logger = logging.getLogger(__name__)


class StrategyConfig:
    """
    Loads and provides strategy descriptions from YAML config.

    This allows easy maintenance and i18n support for strategy explanations.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize strategy config loader.

        Args:
            config_path: Path to strategy_descriptions.yaml (defaults to this module's directory)
        """
        if config_path is None:
            config_path = Path(__file__).parent / "strategy_descriptions.yaml"

        self.config_path = config_path
        self.strategies: Dict = {}
        self._load_config()

    def _load_config(self):
        """Load strategy descriptions from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.strategies = data.get('strategies', {})

            logger.debug(f"Loaded {len(self.strategies)} strategy descriptions")

        except FileNotFoundError:
            logger.warning(f"Strategy config file not found: {self.config_path}")
            self.strategies = {}

        except Exception as e:
            logger.error(f"Error loading strategy config: {e}")
            self.strategies = {}

    def get_description(self, strategy_key: str, locale: str = "en") -> str:
        """
        Get strategy description for a given strategy and locale.

        Args:
            strategy_key: Strategy identifier (e.g., 'ma120_deviation')
            locale: Language code (e.g., 'en', 'zh_CN')

        Returns:
            Strategy description string, or empty string if not found
        """
        if strategy_key not in self.strategies:
            logger.warning(f"Strategy '{strategy_key}' not found in config")
            return ""

        strategy = self.strategies[strategy_key]
        descriptions = strategy.get('descriptions', {})

        # Try requested locale, fall back to English
        description = descriptions.get(locale) or descriptions.get('en', '')

        return description.strip()

    def get_name(self, strategy_key: str) -> str:
        """
        Get strategy display name.

        Args:
            strategy_key: Strategy identifier

        Returns:
            Strategy name, or the key itself if not found
        """
        if strategy_key not in self.strategies:
            return strategy_key

        return self.strategies[strategy_key].get('name', strategy_key)

    def list_strategies(self) -> list:
        """
        List all available strategy keys.

        Returns:
            List of strategy identifiers
        """
        return list(self.strategies.keys())
