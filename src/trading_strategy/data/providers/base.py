"""
Base class for data providers.

Defines the interface that all data providers must implement.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union

from trading_strategy.config.stocks import StockInfo
from trading_strategy.data.models import StockData


class DataProvider(ABC):
    """
    Abstract base class for stock data providers.

    All data providers must implement this interface to ensure
    compatibility with the DataFetcherManager.
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this data provider.

        Returns:
            Provider name (e.g., 'yfinance', 'alpha_vantage')
        """
        pass

    @abstractmethod
    def fetch_stock_data(
        self,
        stock_info: StockInfo,
        days: int = 120
    ) -> Tuple[Optional[StockData], Optional[str]]:
        """
        Fetch stock data and calculate MA120.

        Args:
            stock_info: Stock information (symbol, name, category)
            days: Number of days of historical data to fetch (default: 120 for MA120)

        Returns:
            Tuple of (StockData or None, error_message or None)
            - On success: (StockData, None)
            - On failure: (None, error_message)
        """
        pass
