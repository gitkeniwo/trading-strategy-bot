"""Test error message formatting."""

from datetime import datetime
from pathlib import Path
from trading_strategy.data.models import FetchError
from trading_strategy.i18n.translator import Translator
from trading_strategy.notifications.message_formatter import MessageFormatter

# Create translator
locale_dir = Path("src/trading_strategy/i18n/locales")
translator = Translator("en", locale_dir)

# Create formatter
formatter = MessageFormatter(translator, strategy_key="ma120_deviation")

# Create mock fetch errors
mock_errors = [
    FetchError(
        symbol="SPY",
        name="SPDR S&P 500 ETF",
        provider="all_providers",
        error_message="yfinance: No data returned for SPY - Yahoo Finance may be experiencing issues | alpha_vantage: No time series data returned from Alpha Vantage for SPY"
    ),
    FetchError(
        symbol="AAPL",
        name="Apple Inc.",
        provider="all_providers",
        error_message="yfinance: No data returned for AAPL - Yahoo Finance may be experiencing issues | alpha_vantage: Alpha Vantage rate limit reached: Thank you for using Alpha Vantage! Our standard API call frequency is 25 calls per day."
    ),
]

# Format summary with errors
message = formatter.format_summary(
    signals=[],
    run_time=datetime.now(),
    all_stock_data=[],
    fetch_errors=mock_errors
)

print(message)
