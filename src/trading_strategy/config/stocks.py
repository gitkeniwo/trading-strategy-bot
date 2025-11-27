"""
Stock symbols configuration for the trading strategy.

Tracks:
- S&P 500 (SPY ETF)
- Magnificent 7: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class StockInfo:
    """Information about a stock to track."""

    symbol: str
    name: str
    category: str  # "index" or "mag7"


# Stock symbols to monitor
TRACKED_STOCKS: List[StockInfo] = [
    # S&P 500 ETF
    StockInfo(symbol="SPY", name="SPDR S&P 500 ETF", category="index"),
    # Magnificent 7
    StockInfo(symbol="AAPL", name="Apple Inc.", category="mag7"),
    StockInfo(symbol="MSFT", name="Microsoft Corporation", category="mag7"),
    StockInfo(symbol="GOOGL", name="Alphabet Inc.", category="mag7"),
    StockInfo(symbol="AMZN", name="Amazon.com Inc.", category="mag7"),
    StockInfo(symbol="NVDA", name="NVIDIA Corporation", category="mag7"),
    StockInfo(symbol="META", name="Meta Platforms Inc.", category="mag7"),
    StockInfo(symbol="TSLA", name="Tesla Inc.", category="mag7"),
]


def get_all_symbols() -> List[str]:
    """Get list of all stock symbols to track."""
    return [stock.symbol for stock in TRACKED_STOCKS]


def get_stock_info(symbol: str) -> StockInfo:
    """Get information for a specific stock symbol."""
    for stock in TRACKED_STOCKS:
        if stock.symbol == symbol:
            return stock
    raise ValueError(f"Unknown stock symbol: {symbol}")
