"""
Data provider modules for stock market data.

This package contains implementations for various data sources:
- YFinance (primary, free)
- Alpha Vantage (backup, requires API key)
- Extensible for future providers
"""

from trading_strategy.data.providers.base import DataProvider
from trading_strategy.data.providers.yfinance_provider import YFinanceProvider
from trading_strategy.data.providers.alphavantage_provider import AlphaVantageProvider

__all__ = [
    "DataProvider",
    "YFinanceProvider",
    "AlphaVantageProvider",
]
