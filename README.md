# Trading Strategy Bot

**Automated MA120 Deviation Trading Strategy with Telegram Notifications**

A Python-based quantitative trading system that monitors S&P 500 and Magnificent 7 stocks, detects buy signals based on moving average deviations, and sends real-time notifications via Telegram. Runs automatically twice daily on GitHub Actions.

## Features

- 📊 **MA120 Deviation Strategy**: Identifies buy opportunities when prices deviate significantly from 120-day moving average
- 📱 **Telegram Notifications**: Real-time alerts with detailed signal information and stock status
- ⏰ **Automated Execution**: Runs twice daily (9:30 AM & 3:00 PM ET) via GitHub Actions
- 💾 **State Persistence**: Git-based state management (no database required)
- 🌐 **i18n Ready**: Designed for multi-language support (English implemented, Chinese planned)
- 🔧 **Modular Architecture**: Extensible design for adding new strategies and data sources

## Tracked Stocks

- **S&P 500**: SPY (SPDR S&P 500 ETF)
- **Magnificent 7**:
  - AAPL (Apple)
  - MSFT (Microsoft)
  - GOOGL (Alphabet)
  - AMZN (Amazon)
  - NVDA (NVIDIA)
  - META (Meta)
  - TSLA (Tesla)

## Strategy Overview

### Signal 1: 15% Below MA120
- **Trigger**: Price / MA120 ≤ 0.85
- **Action**: Recommend buying 20% position
- **Purpose**: Value accumulation at discount

### Signal 2: 20% Below Signal 1
- **Trigger**: Price / Signal1Price ≤ 0.80
- **Action**: Recommend additional 20% position
- **Purpose**: Dollar-cost averaging at deeper discount

### Reset Logic
After Signal 2 triggers, state resets to allow future Signal 1 opportunities.

📚 **Read more**: [Strategy Explanation](docs/STRATEGY_EXPLANATION.md)

## Quick Start

### Prerequisites

- **Python 3.11+** (3.12 recommended)
- **GitHub account** (for automated runs)
- **Telegram account** (for notifications)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/basic-strategy.git
cd basic-strategy
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
uv venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
uv sync --no-dev
# or
uv pip install -r requirements.txt
```

### 3. Set Up Telegram Bot

Follow the detailed guide: [Telegram Setup](docs/TELEGRAM_SETUP.md)

Quick summary:
1. Create bot via @BotFather
2. Get bot token
3. Get your chat ID via @userinfobot
4. Add to `.env` file

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

nvim .env 
```

Required variables:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 5. Test Locally

```bash
# Run the trading strategy
python -m trading_strategy.main
```

You should receive a notification in Telegram!

### 6. Set Up GitHub Actions

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial setup"
   git push origin main
   ```

2. **Add GitHub Secrets**:
   - Go to repository Settings > Secrets and variables > Actions
   - Or `gh secret set <KEY> --body <value>`
   - Add `TELEGRAM_BOT_TOKEN`
   - Add `TELEGRAM_CHAT_ID`

3. **Enable Actions**:
   - Go to Actions tab
   - Enable workflows if prompted

4. **Manual Test**:
   - Go to Actions → Trading Strategy Bot
   - Click "Run workflow"
   - Check Telegram for notification

5. **Test Locally with `act`**
   - Install `act` and start your `docker`
   - The secrets must be passed to `act` through a file 
   - Use command:

```sh
act workflow_dispatch \
   -j run-strategy 
   --secret-file .env
```

## Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | ✅ | Bot token from @BotFather | - |
| `TELEGRAM_CHAT_ID` | ✅ | Your Telegram chat or Channel ID | - |
| `ALPHA_VANTAGE_API_KEY` | ❌ | Backup data source (not needed for MVP) | - |
| `LOCALE` | ❌ | Language for notifications | `en` |
| `TIMEZONE` | ❌ | Timezone for timestamps | `America/New_York` |

### Modifying Tracked Stocks

Edit [src/trading_strategy/config/stocks.py](src/trading_strategy/config/stocks.py):

```python
TRACKED_STOCKS: List[StockInfo] = [
    StockInfo(symbol="SPY", name="SPDR S&P 500 ETF", category="index"),
    StockInfo(symbol="AAPL", name="Apple Inc.", category="mag7"),
    # Add more stocks here
]
```

### Adjusting Strategy Thresholds

Edit [src/trading_strategy/strategies/ma120_deviation.py](src/trading_strategy/strategies/ma120_deviation.py):

```python
SIGNAL_1_THRESHOLD = 0.85  # 15% below MA120
SIGNAL_2_THRESHOLD = 0.80  # 20% below Signal 1
SIGNAL_1_POSITION_SIZE = 0.20  # 20%
SIGNAL_2_POSITION_SIZE = 0.20  # 20%
```

## Notification Examples

### No Signals
```
📊 Trading Strategy Daily Summary

Date: 2025-11-26 14:30 ET
Signals Generated: 0

No buy signals triggered today. All stocks are above their thresholds.

📊 Current Stock Status:

• SPY: $679.68 (3.84% above MA120)
• AAPL: $277.55 (14.56% above MA120)
• META: $633.61 (11.61% below MA120) 📍 approaching trigger

────────────────────────────────────────
_Strategy: MA120 Deviation | Automated via GitHub Actions_

📖 Strategy Info:
MA120 Deviation Strategy monitors stocks for significant price deviations from their 120-day moving average.
• Signal 1: Triggers when price drops 15% below MA120 (suggests 20% position)
• Signal 2: Triggers when price drops additional 20% below Signal 1 price (suggests another 20% position)
This strategy aims to identify potential value opportunities during market corrections.
```

### Signal 1 Triggered
```
📊 Trading Strategy Daily Summary

Date: 2025-11-26 14:30 ET
Signals Generated: 1


**1. AAPL** (Apple Inc.)
   Type: Signal 1
   Price: $170.50
   MA120: $200.00 (14.75% below)
   Position: 20%


_Strategy: MA120 Deviation | Automated via GitHub Actions_
```

## GitHub Actions Schedule

The workflow runs automatically:
- **9:30 AM ET** (14:30 UTC): Before market open analysis
- **3:00 PM ET** (20:00 UTC): Before market close check
- **Monday-Friday only**: Weekdays during market hours

Note: During daylight saving time (EDT), runs will be 1 hour earlier. This is acceptable for MVP.

## State Management

The strategy tracks signal states in `signals.json`:

```json
{
  "AAPL": {
    "symbol": "AAPL",
    "signal_1_triggered": true,
    "signal_1_price": 170.50,
    "signal_1_date": "2025-11-26",
    "signal_2_triggered": false,
    "signal_2_price": null,
    "signal_2_date": null
  }
}
```

**Important**: This file is committed to the repository to maintain state across GitHub Actions runs.

## Data Sources

### Primary: yfinance
- Free, unlimited API
- No API key required
- Reliable for educational/personal use
- Excellent pandas integration

### Backup: Alpha Vantage (Optional)
- Free tier: 25 calls/day
- Requires API key
- Enterprise-grade reliability
- Not needed for MVP (yfinance is sufficient)

To add Alpha Vantage:
1. Get free API key from [alphavantage.co](https://www.alphavantage.co/support/#api-key)
2. Add to `.env`: `ALPHA_VANTAGE_API_KEY=your_key`
3. Add to GitHub secrets

## Modular Provider Architecture

Data providers are now modularized in `src/trading_strategy/data/providers/`:

```
providers/
├── __init__.py              # Exports all providers
├── base.py                  # DataProvider abstract base class
├── yfinance_provider.py     # YFinance implementation (primary)
├── alphavantage_provider.py # Alpha Vantage implementation (backup)
└── README.md                # Provider documentation
```

**Benefits**:
- Easy to add new data sources
- Each provider is self-contained
- Clear separation of concerns
- Better testability

See [Provider README](src/trading_strategy/data/providers/README.md) for details on adding new providers.

## Troubleshooting

### No notifications received

**Check 1**: Verify Telegram setup
```bash
python -c "
from trading_strategy.config.settings import settings
from trading_strategy.notifications.telegram import TelegramNotifier

notifier = TelegramNotifier(settings.telegram_bot_token, settings.telegram_chat_id)
notifier.test_connection()
"
```

**Check 2**: Verify environment variables
```bash
python -c "from trading_strategy.config.settings import settings; print(settings.telegram_bot_token[:10])"
```

**Check 3**: Check GitHub Actions logs
- Go to Actions tab
- Click on latest workflow run
- Review logs for errors

### "No module named 'trading_strategy'"

You need to run from the project root:
```bash
python -m trading_strategy.main
```

Not:
```bash
cd src
python main.py  # This won't work
```

### Data fetch errors

**yfinance issues**: Usually temporary. The workflow will retry automatically.

**Add Alpha Vantage backup**:
1. Get API key from alphavantage.co
2. Add to environment variables
3. Automatic fallback will activate

### Workflow not running on schedule

**Check 1**: Ensure workflows are enabled
- Go to repository Settings → Actions → General
- Enable "Allow all actions and reusable workflows"

**Check 2**: Verify cron syntax
- GitHub Actions uses UTC time
- Current schedule: 14:30 UTC and 20:00 UTC (EST times)

**Check 3**: Check for errors in previous runs
- Failed runs may prevent scheduling

## Development

### Running Tests

```bash
# Install development dependencies
uv sync

# Run tests
pytest

# Run with coverage
pytest --cov=src/trading_strategy --cov-report=html
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking (future)
# mypy src/
```

### Adding a New Strategy

1. Create new file in `src/trading_strategy/strategies/`
2. Inherit from `Strategy` base class
3. Implement required methods: `get_name()`, `evaluate()`, `update_state()`
4. Add strategy description to `src/trading_strategy/config/strategy_descriptions.yaml`
5. Update `main.py` to use new strategy

Example: See [Strategy 1 (Monthly MA5)](docs/STRATEGY_EXPLANATION.md#future-enhancements) for planned addition.


## Roadmap

### ✅ MVP (Current)
- [x] MA120 Deviation Strategy
- [x] Telegram notifications with stock status
- [x] GitHub Actions automation
- [x] State persistence
- [x] i18n architecture
- [x] Modular provider architecture
- [x] Strategy description system

### 🔜 Planned Features
- [ ] Strategy 1: Monthly MA5 crossover
- [ ] Chart generation in notifications
- [ ] Chinese language support (zh_CN)
- [ ] Backtesting framework
- [ ] Web dashboard for visualization
- [ ] Sell signal logic
- [ ] Portfolio tracking
- [ ] Risk metrics (Sharpe ratio, max drawdown)

## License

GLWTPL

## Disclaimer

Use at your own risk.

## Resources

- [Telegram Setup Guide](docs/TELEGRAM_SETUP.md)
- [Strategy Explanation](docs/STRATEGY_EXPLANATION.md)
- [Data Providers](src/trading_strategy/data/providers/README.md)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
