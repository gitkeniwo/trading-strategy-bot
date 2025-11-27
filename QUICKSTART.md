# Quick Start Guide

Get your trading strategy bot running in 5 minutes!

## 1. Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

## 2. Set Up Telegram Bot (2 min)

1. Open Telegram, search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Save the **bot token**
4. Search for `@userinfobot` and send a message
5. Save your **chat ID**

Full guide: [docs/TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md)

## 3. Configure Environment (1 min)

```bash
# Copy example
cp .env.example .env

# Edit with your credentials
nano .env
```

Add:
```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## 4. Run It! (1 min)

```bash
python -m src.trading_strategy.main
```

You should get a Telegram notification! 🎉

## 5. Deploy to GitHub Actions (optional)

See [README.md](README.md#6-set-up-github-actions) for full instructions.

Quick version:
1. Push to GitHub
2. Add secrets in Settings → Secrets → Actions
3. Go to Actions tab and run workflow

---

## Troubleshooting

**No notification?**
```bash
# Test Telegram connection
python -c "
import sys; sys.path.insert(0, 'src')
from trading_strategy.config.settings import settings
from trading_strategy.notifications.telegram import TelegramNotifier
TelegramNotifier(settings.telegram_bot_token, settings.telegram_chat_id).test_connection()
"
```

**Import errors?**
```bash
# Make sure you're in project root
pwd  # Should show .../basic-strategy

# Run from root
python -m src.trading_strategy.main
```

**Still stuck?**
- Check [docs/LOCAL_SETUP.md](docs/LOCAL_SETUP.md) for detailed guide
- Review [README.md](README.md) for full documentation
- Check GitHub Issues

---

## What It Does

- Monitors **SPY + Magnificent 7 stocks** (AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA)
- Detects when price drops **15% below 120-day MA** (Signal 1)
- Detects when price drops **another 20%** (Signal 2)
- Sends detailed **Telegram notifications**
- Runs **automatically twice daily** on GitHub Actions

## Next Steps

Once working locally:
1. ✅ Test with real data
2. ✅ Deploy to GitHub Actions
3. ✅ Read [Strategy Explanation](docs/STRATEGY_EXPLANATION.md)
4. ✅ Customize stocks/thresholds if desired

Happy trading! 📈
