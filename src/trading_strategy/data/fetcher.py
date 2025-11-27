"""
Data fetcher manager with fallback support.

Coordinates multiple data providers with automatic fallback.
Providers are located in the providers/ subdirectory for better modularity.

Architecture:
- Primary: YFinance (free, unlimited)
- Backup: Alpha Vantage (requires API key, 25 calls/day free)
- Extensible: Easy to add new providers by implementing DataProvider interface
"""

import logging
from typing import List, Optional, Tuple

from trading_strategy.config.stocks import StockInfo
from trading_strategy.data.models import FetchError, StockData
from trading_strategy.data.providers import (
    AlphaVantageProvider,
    DataProvider,
    YFinanceProvider,
)

logger = logging.getLogger(__name__)


class DataFetcherManager:
    """
    Manager that coordinates multiple data providers with fallback support.

    Uses primary provider (yfinance), falls back to secondary if needed.
    Extensible design makes it easy to add more data sources.
    """

    def __init__(self, alpha_vantage_api_key: Optional[str] = None):
        """
        Initialize data fetcher manager.

        Args:
            alpha_vantage_api_key: Optional API key for Alpha Vantage backup
        """
        # Primary provider
        self.primary_provider: DataProvider = YFinanceProvider()

        # Secondary provider (if API key provided)
        self.secondary_provider: Optional[DataProvider] = None
        if alpha_vantage_api_key:
            self.secondary_provider = AlphaVantageProvider(alpha_vantage_api_key)

        logger.info(f"Initialized DataFetcherManager with primary: {self.primary_provider.get_name()}")
        if self.secondary_provider:
            logger.info(f"Secondary provider available: {self.secondary_provider.get_name()}")

    def fetch_stock_data(
        self,
        stock_info: StockInfo,
        days: int = 120
    ) -> Tuple[Optional[StockData], Optional[FetchError]]:
        """
        Fetch stock data with automatic fallback.

        Tries primary provider first, falls back to secondary if primary fails.

        Args:
            stock_info: Stock information
            days: Number of days of historical data

        Returns:
            Tuple of (StockData or None, FetchError or None)
            - On success: (StockData, None)
            - On failure: (None, FetchError with details)
        """
        errors: List[str] = []

        # Try primary provider
        logger.info(f"Fetching {stock_info.symbol} using {self.primary_provider.get_name()}")
        data, error = self.primary_provider.fetch_stock_data(stock_info, days)

        if data is not None:
            return data, None

        # Record primary error
        if error:
            errors.append(f"{self.primary_provider.get_name()}: {error}")

        # Primary failed, try secondary if available
        if self.secondary_provider:
            logger.warning(
                f"Primary provider failed for {stock_info.symbol}, "
                f"trying {self.secondary_provider.get_name()}"
            )
            data, error = self.secondary_provider.fetch_stock_data(stock_info, days)

            if data is not None:
                return data, None

            # Record secondary error
            if error:
                errors.append(f"{self.secondary_provider.get_name()}: {error}")

        # All providers failed - create FetchError
        logger.error(f"All providers failed for {stock_info.symbol}")

        combined_error = " | ".join(errors) if errors else "Unknown error"
        fetch_error = FetchError(
            symbol=stock_info.symbol,
            name=stock_info.name,
            provider="all_providers",
            error_message=combined_error
        )

        return None, fetch_error
