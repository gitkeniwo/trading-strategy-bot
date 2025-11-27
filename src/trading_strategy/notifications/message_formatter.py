"""
Message formatting for trading signals.

This module formats buy signals into human-readable messages for Telegram.
Handles:
- Signal 1 and Signal 2 formatting
- Summary messages (bundling multiple signals)
- Error notifications

Design: User requested percentage-only display (no dollar amounts)
"""

import logging
from datetime import datetime
from typing import List, Optional

from trading_strategy.config.strategy_config import StrategyConfig
from trading_strategy.data.models import FetchError, Signal, SignalState, SignalType, StockData
from trading_strategy.i18n.translator import Translator

logger = logging.getLogger(__name__)


class MessageFormatter:
    """
    Formats trading signals for Telegram notifications.

    Uses i18n system for future multi-language support.
    """

    def __init__(self, translator: Translator, strategy_key: str = "ma120_deviation"):
        """
        Initialize message formatter.

        Args:
            translator: Translator instance for i18n
            strategy_key: Strategy identifier for descriptions (default: ma120_deviation)
        """
        self.t = translator
        self.strategy_key = strategy_key
        self.strategy_config = StrategyConfig()

    def format_signal(self, signal: Signal, state: SignalState) -> str:
        """
        Format a single buy signal.

        Args:
            signal: The buy signal to format
            state: Current state for this stock (for Signal 2 context)

        Returns:
            Formatted message string
        """
        if signal.signal_type == SignalType.SIGNAL_1:
            return self._format_signal_1(signal, state)
        else:
            return self._format_signal_2(signal, state)

    def _format_signal_1(self, signal: Signal, state: SignalState) -> str:
        """Format Signal 1 (15% below MA120)."""
        lines = [
            self.t.get("buy_signal.title"),
            "",
            f"{self.t.get('buy_signal.stock_label')}: {signal.symbol} ({signal.name})",
            f"{self.t.get('buy_signal.signal_type_label')}: {self.t.get('buy_signal.signal_1_subtitle')}",
            "",
            self.t.get("sections.current_metrics"),
            f"• {self.t.get('buy_signal.current_price')}: ${signal.current_price:.2f}",
            f"• {self.t.get('buy_signal.ma120_value')}: ${signal.ma120:.2f}",
            f"• {self.t.get('buy_signal.deviation')}: {abs(signal.ma120_deviation_pct):.2f}% below MA120",
            f"• {self.t.get('buy_signal.date')}: {signal.timestamp.strftime('%Y-%m-%d %H:%M ET')}",
            "",
            self.t.get("sections.recommendation"),
            f"• {self.t.get('buy_signal.position_size')}: {signal.position_size_display} {self.t.get('buy_signal.of_allocated_capital')}",
            "",
            self.t.get("sections.next_steps"),
        ]

        # Calculate Signal 2 trigger price
        signal_2_trigger = signal.current_price * 0.80
        lines.append(f"• {self.t.get('buy_signal.signal_2_will_trigger', price=signal_2_trigger)}")
        lines.append(f"  {self.t.get('buy_signal.signal_2_additional_drop')}")
        lines.append(f"• {self.t.get('buy_signal.signal_2_additional_position', size=signal.position_size_display)}")

        return "\n".join(lines)

    def _format_signal_2(self, signal: Signal, state: SignalState) -> str:
        """Format Signal 2 (20% below Signal 1 price)."""
        lines = [
            self.t.get("buy_signal.title"),
            "",
            f"{self.t.get('buy_signal.stock_label')}: {signal.symbol} ({signal.name})",
            f"{self.t.get('buy_signal.signal_type_label')}: {self.t.get('buy_signal.signal_2_subtitle')}",
            "",
            self.t.get("sections.current_metrics"),
            f"• {self.t.get('buy_signal.current_price')}: ${signal.current_price:.2f}",
            f"• Signal 1 Price: ${signal.signal_1_price:.2f}",
            f"• Additional Drop: {abs(((signal.current_price - signal.signal_1_price) / signal.signal_1_price) * 100):.2f}%",
            f"• {self.t.get('buy_signal.date')}: {signal.timestamp.strftime('%Y-%m-%d %H:%M ET')}",
            "",
            self.t.get("sections.recommendation"),
            f"• {self.t.get('buy_signal.position_size')}: {signal.position_size_display} {self.t.get('buy_signal.of_allocated_capital')}",
            "",
            self.t.get("sections.next_steps"),
            f"• {self.t.get('buy_signal.both_signals_complete')}",
        ]

        return "\n".join(lines)

    def format_summary(
        self,
        signals: List[Signal],
        run_time: datetime,
        all_stock_data: Optional[List[StockData]] = None,
        fetch_errors: Optional[List[FetchError]] = None
    ) -> str:
        """
        Format a summary of all signals from this run.

        User preference: Bundle all signals into ONE message per run.

        Args:
            signals: List of all signals generated in this run
            run_time: Timestamp of the run
            all_stock_data: List of all stock data (for status display when no signals)
            fetch_errors: List of fetch errors for stocks that failed

        Returns:
            Formatted summary message
        """
        if not signals:
            # No signals - send status update with all stock data
            lines = [
                self.t.get("summary.title"),
                "",
                f"{self.t.get('summary.date')}: {run_time.strftime('%Y-%m-%d %H:%M ET')}",
                f"{self.t.get('summary.signals_generated')}: 0",
                "",
                self.t.get("summary.no_signals"),
            ]

            # Add current stock status if available
            if all_stock_data:
                lines.append("")
                lines.append("📊 **Current Stock Status:**")
                lines.append("")

                for stock in all_stock_data:
                    deviation = stock.ma120_deviation
                    direction = "above" if deviation > 0 else "below"

                    # Add marker for stocks closest to trigger (15% below = -15%)
                    marker = ""
                    if deviation < -10:  # Within 5% of trigger
                        if deviation < -12:
                            marker = " ⚠️ closest to trigger"
                        else:
                            marker = " 📍 approaching trigger"

                    lines.append(
                        f"• **{stock.symbol}**: ${stock.current_price:.2f} "
                        f"({abs(deviation):.2f}% {direction} MA120){marker}"
                    )

            # Add fetch errors if any
            if fetch_errors:
                lines.append("")
                lines.append("⚠️ **Data Fetch Errors:**")
                lines.append("")
                for error in fetch_errors:
                    lines.append(f"• **{error.symbol}** ({error.name}):")
                    lines.append(f"  `{error.error_message}`")

            lines.append("")
            lines.append(self._format_footer())

            return "\n".join(lines)

        # Build summary with all signals
        lines = [
            self.t.get("summary.title"),
            "",
            f"{self.t.get('summary.date')}: {run_time.strftime('%Y-%m-%d %H:%M ET')}",
            f"{self.t.get('summary.signals_generated')}: {len(signals)}",
            "",
            "─" * 40,
        ]

        # Add each signal
        for i, signal in enumerate(signals, 1):
            signal_type_name = (
                "Signal 1" if signal.signal_type == SignalType.SIGNAL_1 else "Signal 2"
            )

            lines.append("")
            lines.append(f"**{i}. {signal.symbol}** ({signal.name})")
            lines.append(f"   Type: {signal_type_name}")
            lines.append(f"   Price: ${signal.current_price:.2f}")

            if signal.signal_type == SignalType.SIGNAL_1:
                lines.append(f"   MA120: ${signal.ma120:.2f} ({abs(signal.ma120_deviation_pct):.2f}% below)")
            else:
                lines.append(f"   Signal 1 Price: ${signal.signal_1_price:.2f}")

            lines.append(f"   Position: {signal.position_size_display}")
            lines.append("─" * 40)

        lines.append("")
        lines.append(self._format_footer())

        return "\n".join(lines)

    def _format_footer(self) -> str:
        """
        Format footer with strategy description.

        Returns:
            Formatted footer string with separator and strategy info
        """
        lines = [
            "─" * 40,
            f"_{self.t.get('summary.footer')}_",
        ]

        # Get strategy description
        strategy_desc = self.strategy_config.get_description(
            self.strategy_key,
            self.t.locale
        )

        if strategy_desc:
            lines.append("")
            lines.append("📖 **Strategy Info:**")
            # Format multiline description with proper indentation
            for line in strategy_desc.split('\n'):
                if line.strip():
                    lines.append(line)

        return "\n".join(lines)

    def format_error(self, error_message: str) -> str:
        """
        Format an error notification.

        Args:
            error_message: Error details

        Returns:
            Formatted error message
        """
        return "\n".join([
            self.t.get("notification.error_title"),
            "",
            self.t.get("notification.error_details"),
            "",
            f"```\n{error_message}\n```",
            "",
            self.t.get("notification.check_logs"),
        ])
