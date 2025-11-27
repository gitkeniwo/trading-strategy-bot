"""
YFinance data provider.

Primary data source using the yfinance library.
Free, unlimited, no API key required.
"""

import logging
from typing import Optional, Tuple

import yfinance as yf

from trading_strategy.config.stocks import StockInfo
from trading_strategy.data.models import StockData
from trading_strategy.data.providers.base import DataProvider

logger = logging.getLogger(__name__)


class YFinanceProvider(DataProvider):
    """
    Data provider using yfinance library.

    Advantages:
    - Free, no API key required
    - Unlimited requests
    - Excellent pandas integration
    - Reliable for educational/personal use

    Data source: Yahoo Finance
    """

    def get_name(self) -> str:
        """Get provider name."""
        return "yfinance"

    def fetch_stock_data(
        self,
        stock_info: StockInfo,
        days: int = 120
    ) -> Tuple[Optional[StockData], Optional[str]]:
        """
        Fetch stock data using yfinance.

        Args:
            stock_info: Stock information
            days: Number of days of historical data (default: 120)

        Returns:
            Tuple of (StockData or None, error_message or None)
        """
        try:
            # Fetch more days than needed to ensure we have enough data after cleaning
            ticker = yf.Ticker(stock_info.symbol)

            # Download historical data (extra days for safety)
            hist = ticker.history(period=f"{days + 30}d")

            if hist.empty:
                error_msg = f"No data returned for {stock_info.symbol} - Yahoo Finance may be experiencing issues"
                logger.error(error_msg)
                return None, error_msg

            # Clean data: remove NaN values
            hist = hist.dropna()

            if len(hist) < days:
                error_msg = (
                    f"Insufficient data for {stock_info.symbol}: "
                    f"only {len(hist)} days available, need at least {days}"
                )
                logger.warning(error_msg)
                return None, error_msg

            # Calculate MA120 (use last 120 days of closing prices)
            recent_closes = hist["Close"].tail(days)
            ma120 = recent_closes.mean()

            # Get current (most recent) price
            current_price = hist["Close"].iloc[-1]

            # Get timestamp of most recent data
            timestamp = hist.index[-1].to_pydatetime()

            return StockData(
                symbol=stock_info.symbol,
                name=stock_info.name,
                current_price=float(current_price),
                ma120=float(ma120),
                timestamp=timestamp,
                days_of_data=len(hist),
            ), None

        except Exception as e:
            error_msg = f"yfinance error: {str(e)}"
            logger.error(f"Error fetching data for {stock_info.symbol} via yfinance: {e}")
            return None, error_msg
