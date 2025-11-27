# Local Setup and Testing Guide

This guide walks through setting up the trading strategy bot on your local machine for development and testing.

## Prerequisites

- Python 3.11 or higher
- Git
- Telegram account
- Code editor (VS Code, PyCharm, etc.)

## Step 1: Clone and Setup Environment

```bash
# Clone the repository
cd ~/ws  # or your preferred directory
git clone https://github.com/yourusername/basic-strategy.git
cd basic-strategy

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify Python version
python --version  # Should be 3.11+

# Upgrade pip
pip install --upgrade pip
```

## Step 2: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional but recommended)
pip install -r requirements-dev.txt

# Verify installation
pip list | grep yfinance
pip list | grep pydantic
pip list | grep requests
```

## Step 3: Configure Telegram Bot

Follow [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md) to:
1. Create bot via @BotFather
2. Get bot token
3. Get your chat ID

## Step 4: Create Environment File

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

Add your credentials:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
TELEGRAM_CHAT_ID=123456789
LOCALE=en
TIMEZONE=America/New_York
```

**Important**: Never commit `.env` to git! It's already in `.gitignore`.

## Step 5: Test Configuration

### Test 1: Import Check
```bash
python -c "import sys; sys.path.insert(0, 'src'); from trading_strategy.config import settings; print('Config OK')"
```

### Test 2: Telegram Connection
```bash
python -c "
import sys
sys.path.insert(0, 'src')
from trading_strategy.config.settings import settings
from trading_strategy.notifications.telegram import TelegramNotifier

notifier = TelegramNotifier(settings.telegram_bot_token, settings.telegram_chat_id)
success = notifier.test_connection()
print('Telegram test:', 'SUCCESS' if success else 'FAILED')
"
```

You should receive a message in Telegram!

### Test 3: Data Fetch
```bash
python -c "
import sys
sys.path.insert(0, 'src')
from trading_strategy.config.stocks import StockInfo
from trading_strategy.data.fetcher import DataFetcherManager

fetcher = DataFetcherManager()
stock = StockInfo(symbol='AAPL', name='Apple Inc.', category='test')
data = fetcher.fetch_stock_data(stock)
print(f'AAPL Price: \${data.current_price:.2f}, MA120: \${data.ma120:.2f}')
"
```

## Step 6: Run the Strategy

```bash
# Add src to PYTHONPATH and run
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
python -m trading_strategy.main
```

Or simpler:

```bash
# Run from project root
python -m src.trading_strategy.main
```

You should see:
- Log messages showing processing of each stock
- Telegram notification with summary
- `signals.json` created/updated

## Development Workflow

### Running Tests (when added)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/trading_strategy --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

### Code Formatting

```bash
# Format all code
black src/ tests/

# Check formatting without changes
black --check src/ tests/
```

### Linting

```bash
# Lint code
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Type Checking (future)

```bash
# Run mypy
mypy src/
```

## Project Structure Overview

```
basic-strategy/
├── src/trading_strategy/      # Main package
│   ├── config/                 # Settings and stock configuration
│   ├── data/                   # Data models and fetchers
│   ├── strategies/             # Trading strategies
│   ├── storage/                # State management
│   ├── notifications/          # Telegram integration
│   ├── i18n/                   # Internationalization
│   └── main.py                 # Entry point
├── tests/                      # Tests (to be added)
├── docs/                       # Documentation
├── .github/workflows/          # GitHub Actions
├── signals.json                # State file (created on first run)
├── .env                        # Local config (YOU CREATE THIS)
└── venv/                       # Virtual environment
```

## Modifying the Strategy

### Change Tracked Stocks

Edit [src/trading_strategy/config/stocks.py](../src/trading_strategy/config/stocks.py):

```python
TRACKED_STOCKS: List[StockInfo] = [
    StockInfo(symbol="SPY", name="SPDR S&P 500 ETF", category="index"),
    # Add your stocks here
    StockInfo(symbol="TSLA", name="Tesla Inc.", category="custom"),
]
```

### Adjust Strategy Parameters

Edit [src/trading_strategy/strategies/ma120_deviation.py](../src/trading_strategy/strategies/ma120_deviation.py):

```python
class MA120DeviationStrategy(Strategy):
    SIGNAL_1_THRESHOLD = 0.85  # Change to 0.90 for 10% threshold
    SIGNAL_2_THRESHOLD = 0.80  # Change to 0.85 for 15% threshold
    SIGNAL_1_POSITION_SIZE = 0.20  # Change to 0.10 for 10% position
    SIGNAL_2_POSITION_SIZE = 0.20
```

### Test Changes

```bash
# Run strategy
python -m src.trading_strategy.main

# Check signals.json
cat signals.json | python -m json.tool

# Check Telegram messages
```

## Debugging Tips

### Enable Debug Logging

Edit [src/trading_strategy/main.py](../src/trading_strategy/main.py):

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    # ...
)
```

### Check State File

```bash
# Pretty print signals.json
python -m json.tool signals.json

# Or use jq (if installed)
jq . signals.json
```

### Manual State Reset

```bash
# Clear all signals (be careful!)
echo '{}' > signals.json

# Or delete specific stock
python -c "
import json
with open('signals.json', 'r') as f:
    data = json.load(f)
del data['AAPL']  # Remove AAPL state
with open('signals.json', 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Test Without Telegram

Comment out the notification in [src/trading_strategy/main.py](../src/trading_strategy/main.py):

```python
# success = notifier.send_message(summary_message)
print(summary_message)  # Print instead of sending
```

## Common Issues

### ModuleNotFoundError: No module named 'trading_strategy'

**Solution**: Run from project root and ensure src is in Python path:

```bash
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
python -m trading_strategy.main
```

### Pydantic ValidationError

**Solution**: Check `.env` file has all required variables:

```bash
cat .env | grep -E "TELEGRAM_BOT_TOKEN|TELEGRAM_CHAT_ID"
```

### yfinance download fails

**Solutions**:
1. Check internet connection
2. Try a different stock symbol
3. Wait and retry (sometimes temporary)
4. Add Alpha Vantage backup (see main README)

### "No data returned for SYMBOL"

This can happen if:
- Market is closed (weekends, holidays)
- Stock symbol is invalid
- yfinance is experiencing issues

**Solution**: Test with a known-good symbol:

```bash
python -c "import yfinance as yf; print(yf.Ticker('SPY').history(period='1mo'))"
```

## Next Steps

1. ✅ Local setup complete
2. ✅ Strategy runs successfully
3. ✅ Telegram notifications working

Now you can:
- Deploy to GitHub Actions (see main README)
- Customize strategy parameters
- Add new strategies
- Implement backtesting

## Additional Resources

- [Main README](../README.md) - Project overview
- [Telegram Setup](TELEGRAM_SETUP.md) - Detailed bot configuration
- [Strategy Explanation](STRATEGY_EXPLANATION.md) - Theory and rationale
- [yfinance docs](https://pypi.org/project/yfinance/) - Data source documentation

## Getting Help

If you encounter issues:

1. Check this guide thoroughly
2. Review logs for specific error messages
3. Search GitHub Issues
4. Create new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (Python version, OS)

Happy coding! 🚀
