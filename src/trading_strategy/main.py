"""
Main entry point for the trading strategy system.

This script orchestrates the entire workflow:
1. Initialize all components (data fetcher, strategy, state manager, notifier)
2. Fetch stock data for all tracked symbols
3. Evaluate strategy for each stock
4. Generate and send notifications
5. Update and persist state

Runs twice daily via GitHub Actions (9:30 AM ET and 3:00 PM ET).
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List

from trading_strategy.config.settings import settings
from trading_strategy.config.stocks import TRACKED_STOCKS
from trading_strategy.data.fetcher import DataFetcherManager
from trading_strategy.data.models import FetchError, Signal, StockData
from trading_strategy.i18n.translator import Translator
from trading_strategy.notifications.message_formatter import MessageFormatter
from trading_strategy.notifications.telegram import TelegramNotifier
from trading_strategy.storage.state_manager import StateManager
from trading_strategy.strategies.ma120_deviation import MA120DeviationStrategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("Trading Strategy Bot - Starting")
    logger.info("=" * 60)

    run_time = datetime.now()
    all_signals: List[Signal] = []
    all_stock_data: List[StockData] = []
    fetch_errors: List[FetchError] = []

    try:
        # Initialize components
        logger.info("Initializing components...")

        # Data fetcher (with optional Alpha Vantage backup)
        data_fetcher = DataFetcherManager(
            alpha_vantage_api_key=settings.alpha_vantage_api_key
        )

        # Strategy
        strategy = MA120DeviationStrategy()
        logger.info(f"Using strategy: {strategy.get_name()}")

        # State manager
        state_manager = StateManager(settings.state_file)

        # Translator and message formatter
        translator = Translator(settings.locale, settings.locale_dir)
        formatter = MessageFormatter(translator)

        # Telegram notifier
        notifier = TelegramNotifier(
            bot_token=settings.telegram_bot_token,
            chat_id=settings.telegram_chat_id,
        )

        logger.info("All components initialized successfully")

        # Process each stock
        logger.info(f"Processing {len(TRACKED_STOCKS)} stocks...")

        for stock_info in TRACKED_STOCKS:
            logger.info(f"\n--- Processing {stock_info.symbol} ({stock_info.name}) ---")

            try:
                # Fetch stock data
                stock_data, fetch_error = data_fetcher.fetch_stock_data(stock_info)

                if stock_data is None:
                    logger.warning(f"Skipping {stock_info.symbol} - no data available")
                    if fetch_error:
                        fetch_errors.append(fetch_error)
                    continue

                # Collect stock data for summary
                all_stock_data.append(stock_data)

                logger.info(
                    f"{stock_info.symbol}: Price=${stock_data.current_price:.2f}, "
                    f"MA120=${stock_data.ma120:.2f}, "
                    f"Deviation={stock_data.ma120_deviation:.2f}%"
                )

                # Load state
                state = state_manager.load_state(stock_info.symbol)

                # Evaluate strategy
                signals = strategy.evaluate(stock_data, state)

                if signals:
                    logger.info(f"{stock_info.symbol}: Generated {len(signals)} signal(s)")

                    for signal in signals:
                        # Update state
                        state = strategy.update_state(signal, state)

                        # Add to all signals list
                        all_signals.append(signal)

                    # Save updated state
                    state_manager.save_state(state)
                else:
                    logger.info(f"{stock_info.symbol}: No signals generated")

            except Exception as e:
                logger.error(f"Error processing {stock_info.symbol}: {e}", exc_info=True)
                # Continue with next stock
                continue

        # Send notification summary
        logger.info("\n--- Sending Notifications ---")

        if all_signals:
            logger.info(f"Total signals generated: {len(all_signals)}")
        else:
            logger.info("No signals generated in this run")

        # Format and send summary message (include all stock data for status display)
        summary_message = formatter.format_summary(all_signals, run_time, all_stock_data, fetch_errors)

        success = notifier.send_message(summary_message)

        if success:
            logger.info("Notification sent successfully")
        else:
            logger.error("Failed to send notification")

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("Trading Strategy Bot - Completed Successfully")
        logger.info(f"Stocks processed: {len(TRACKED_STOCKS)}")
        logger.info(f"Signals generated: {len(all_signals)}")
        logger.info(f"Run time: {run_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error("Fatal error in main execution", exc_info=True)

        # Try to send error notification
        try:
            translator = Translator(settings.locale, settings.locale_dir)
            formatter = MessageFormatter(translator)
            notifier = TelegramNotifier(
                bot_token=settings.telegram_bot_token,
                chat_id=settings.telegram_chat_id,
            )

            error_message = formatter.format_error(str(e))
            notifier.send_message(error_message)

        except Exception as notify_error:
            logger.error(f"Failed to send error notification: {notify_error}")

        return 1


if __name__ == "__main__":
    sys.exit(main())
