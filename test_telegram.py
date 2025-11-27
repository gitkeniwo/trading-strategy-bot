#!/usr/bin/env python3
import sys
import logging

# Add src to path
sys.path.insert(0, 'src')

from trading_strategy.config.settings import settings
from trading_strategy.notifications.telegram import TelegramNotifier

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

print("Testing Telegram connection...")
print(f"Bot token (first 10 chars): {settings.telegram_bot_token[:10]}...")
print(f"Chat ID: {settings.telegram_chat_id}")

notifier = TelegramNotifier(settings.telegram_bot_token, settings.telegram_chat_id)
success = notifier.test_connection()

if success:
    print("\n✅ SUCCESS! Check your Telegram for the test message.")
else:
    print("\n❌ FAILED! Check the error messages above.")

sys.exit(0 if success else 1)
