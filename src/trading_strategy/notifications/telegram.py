"""
Telegram Bot API integration for sending notifications.

This module handles communication with Telegram's Bot API:
- Sends formatted messages to specified chat
- Retry logic for reliability
- Error handling

Setup required:
1. Create bot via @BotFather
2. Get bot token
3. Get chat ID via @userinfobot
4. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment

See docs/TELEGRAM_SETUP.md for detailed instructions.
"""

import logging
import time
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """
    Sends notifications via Telegram Bot API.

    Features:
    - Markdown formatting support
    - Automatic retries (3 attempts)
    - Error handling and logging
    """

    BASE_URL = "https://api.telegram.org/bot{token}/sendMessage"
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier.

        Args:
            bot_token: Bot token from @BotFather
            chat_id: Chat ID where messages will be sent
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.url = self.BASE_URL.format(token=bot_token)

    def send_message(self, message: str, parse_mode: str = "Markdown") -> bool:
        """
        Send a message to Telegram.

        Args:
            message: Message text (supports Markdown formatting)
            parse_mode: Telegram parse mode (Markdown or HTML)

        Returns:
            True if message sent successfully, False otherwise
        """
        payload = {
            "chat_id": self.chat_id,
            "text": message,
        }

        # Only add parse_mode if specified
        if parse_mode is not None:
            payload["parse_mode"] = parse_mode

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                logger.info(f"Sending Telegram message (attempt {attempt}/{self.MAX_RETRIES})")

                response = requests.post(
                    self.url,
                    json=payload,
                    timeout=10,
                )

                response.raise_for_status()
                result = response.json()

                if result.get("ok"):
                    logger.info("Telegram message sent successfully")
                    return True
                else:
                    error_msg = result.get("description", "Unknown error")
                    logger.error(f"Telegram API error: {error_msg}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Network error sending Telegram message: {e}")
                # Log response details if available
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        logger.error(f"Telegram API error details: {error_detail}")
                    except:
                        logger.error(f"Response text: {e.response.text}")

            except Exception as e:
                logger.error(f"Unexpected error sending Telegram message: {e}")

            # Retry logic (except on last attempt)
            if attempt < self.MAX_RETRIES:
                logger.info(f"Retrying in {self.RETRY_DELAY} seconds...")
                time.sleep(self.RETRY_DELAY)

        logger.error("Failed to send Telegram message after all retries")
        return False

    def test_connection(self) -> bool:
        """
        Test Telegram bot connection.

        Sends a simple test message to verify configuration.

        Returns:
            True if connection successful, False otherwise
        """
        test_message = "Telegram bot connected successfully!\n\nTrading strategy notifications are ready."
        # Use plain text for test (no Markdown)
        return self.send_message(test_message, parse_mode=None)
