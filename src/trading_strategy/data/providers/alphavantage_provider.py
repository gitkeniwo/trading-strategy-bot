"""
Alpha Vantage data provider.

Backup data source requiring API key.
Free tier: 25 API calls per day.
"""

import logging
from typing import Optional, Tuple

import pandas as pd
import requests

from trading_strategy.config.stocks import StockInfo
from trading_strategy.data.models import StockData
from trading_strategy.data.providers.base import DataProvider

logger = logging.getLogger(__name__)


class AlphaVantageProvider(DataProvider):
    """
    Data provider using Alpha Vantage API (backup source).

    Free tier: 25 API calls per day
    Documentation: https://www.alphavantage.co/documentation/

    Get free API key: https://www.alphavantage.co/support/#api-key
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str):
        """
        Initialize Alpha Vantage provider.

        Args:
            api_key: Alpha Vantage API key
        """
        self.api_key = api_key

    def get_name(self) -> str:
        """Get provider name."""
        return "alpha_vantage"

    def fetch_stock_data(
        self,
        stock_info: StockInfo,
        days: int = 120
    ) -> Tuple[Optional[StockData], Optional[str]]:
        """
        Fetch stock data using Alpha Vantage API.

        Uses TIME_SERIES_DAILY endpoint to get historical data.

        Args:
            stock_info: Stock information
            days: Number of days of historical data (default: 120)

        Returns:
            Tuple of (StockData or None, error_message or None)
        """
        try:
            # Alpha Vantage TIME_SERIES_DAILY endpoint
            # outputsize=compact gives last 100 days (sufficient for MA120)
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": stock_info.symbol,
                "apikey": self.api_key,
                "outputsize": "compact",  # Last 100 days
            }

            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Check for API errors
            if "Error Message" in data:
                error_msg = f"Alpha Vantage API error: {data['Error Message']}"
                logger.error(error_msg)
                return None, error_msg

            if "Note" in data:
                error_msg = f"Alpha Vantage rate limit reached: {data['Note']}"
                logger.warning(error_msg)
                return None, error_msg

            # Parse time series data
            time_series = data.get("Time Series (Daily)")
            if not time_series:
                error_msg = f"No time series data returned from Alpha Vantage for {stock_info.symbol}"
                logger.error(error_msg)
                return None, error_msg

            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient="index")
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            # Alpha Vantage returns string values, convert to float
            df = df.astype(float)

            # Rename columns (Alpha Vantage uses '4. close' etc.)
            df.columns = [col.split(". ")[1].title() for col in df.columns]

            if len(df) < days:
                logger.warning(
                    f"Only {len(df)} days of data for {stock_info.symbol}, "
                    f"expected at least {days}"
                )
                # Continue anyway if we have some data
                if len(df) < 30:
                    error_msg = (
                        f"Insufficient data for {stock_info.symbol}: "
                        f"only {len(df)} days from Alpha Vantage, need at least 30"
                    )
                    return None, error_msg

            # Calculate MA120 (use available data)
            recent_closes = df["Close"].tail(min(days, len(df)))
            ma120 = recent_closes.mean()

            # Get current (most recent) price
            current_price = df["Close"].iloc[-1]

            # Get timestamp
            timestamp = df.index[-1].to_pydatetime()

            logger.info(f"Alpha Vantage: Fetched {len(df)} days for {stock_info.symbol}")

            return StockData(
                symbol=stock_info.symbol,
                name=stock_info.name,
                current_price=float(current_price),
                ma120=float(ma120),
                timestamp=timestamp,
                days_of_data=len(df),
            ), None

        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(f"Network error fetching {stock_info.symbol} from Alpha Vantage: {e}")
            return None, error_msg

        except Exception as e:
            error_msg = f"Alpha Vantage error: {str(e)}"
            logger.error(
                f"Error fetching data for {stock_info.symbol} via Alpha Vantage: {e}",
                exc_info=True
            )
            return None, error_msg
