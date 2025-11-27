"""Quick test to see the formatted message output."""

from datetime import datetime
from trading_strategy.data.models import StockData
from trading_strategy.i18n.translator import Translator
from trading_strategy.notifications.message_formatter import MessageFormatter
from pathlib import Path

# Create translator
locale_dir = Path("src/trading_strategy/i18n/locales")
translator = Translator("en", locale_dir)

# Create formatter
formatter = MessageFormatter(translator, strategy_key="ma120_deviation")

# Create mock stock data
mock_stocks = [
    StockData(
        symbol="SPY",
        name="SPDR S&P 500 ETF",
        current_price=679.68,
        ma120=654.55,
        timestamp=datetime.now(),
        days_of_data=100
    ),
    StockData(
        symbol="AAPL",
        name="Apple Inc.",
        current_price=277.55,
        ma120=242.28,
        timestamp=datetime.now(),
        days_of_data=100
    ),
    StockData(
        symbol="META",
        name="Meta Platforms Inc.",
        current_price=633.61,
        ma120=716.80,
        timestamp=datetime.now(),
        days_of_data=100
    ),
]

# Format summary with no signals
message = formatter.format_summary(
    signals=[],
    run_time=datetime.now(),
    all_stock_data=mock_stocks
)

print(message)
