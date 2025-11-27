"""
MA120 Deviation Strategy (Strategy 2)

This strategy generates buy signals based on price deviation from the 120-day moving average:

Signal 1: When price drops 15% or more below MA120
- Position size: 20% of capital
- Saves the Signal 1 price to calculate Signal 2 trigger

Signal 2: When price drops 20% below the Signal 1 price
- Position size: Additional 20% of capital
- After Signal 2, the state resets to allow future Signal 1 triggers

Theory:
- MA120 represents the ~6-month price trend
- 15% deviation suggests potential oversold condition
- 20% additional drop from Signal 1 represents further discount (dollar-cost averaging)
- This is a value-averaging approach for long-term accumulation
"""

import logging
from datetime import datetime
from typing import List

from trading_strategy.data.models import Signal, SignalState, SignalType, StockData
from trading_strategy.strategies.base import Strategy

logger = logging.getLogger(__name__)


class MA120DeviationStrategy(Strategy):
    """
    MA120 Deviation Strategy implementation.

    Thresholds:
    - Signal 1: Price <= MA120 * 0.85 (15% below)
    - Signal 2: Price <= Signal1Price * 0.80 (20% below Signal 1)
    """

    SIGNAL_1_THRESHOLD = 0.85  # 15% below MA120
    SIGNAL_2_THRESHOLD = 0.80  # 20% below Signal 1 price
    SIGNAL_1_POSITION_SIZE = 0.20  # 20%
    SIGNAL_2_POSITION_SIZE = 0.20  # 20%

    def get_name(self) -> str:
        return "MA120 Deviation"

    def evaluate(self, stock_data: StockData, state: SignalState) -> List[Signal]:
        """
        Evaluate MA120 deviation strategy.

        Logic:
        1. Check if state should be reset (after Signal 2)
        2. Check for Signal 2 condition (if Signal 1 already triggered)
        3. Check for Signal 1 condition (if not already triggered)

        Returns:
            List of signals (empty, or containing Signal 1 or Signal 2)
        """
        signals: List[Signal] = []

        # Reset state if needed (after Signal 2 has been triggered)
        if state.should_reset():
            logger.info(f"{stock_data.symbol}: Resetting state after Signal 2 completion")
            state.reset()

        # Check for Signal 2 (only if Signal 1 was previously triggered)
        if state.signal_1_triggered and not state.signal_2_triggered:
            signal_2 = self._check_signal_2(stock_data, state)
            if signal_2:
                signals.append(signal_2)
                return signals  # Return immediately - one signal per run

        # Check for Signal 1 (only if not already triggered)
        if not state.signal_1_triggered:
            signal_1 = self._check_signal_1(stock_data, state)
            if signal_1:
                signals.append(signal_1)
                return signals

        return signals

    def _check_signal_1(self, stock_data: StockData, state: SignalState) -> Signal | None:
        """
        Check if Signal 1 condition is met.

        Condition: Price <= MA120 * 0.85 (15% or more below MA120)
        """
        trigger_price = stock_data.ma120 * self.SIGNAL_1_THRESHOLD

        if stock_data.current_price <= trigger_price:
            logger.info(
                f"{stock_data.symbol}: Signal 1 triggered! "
                f"Price ${stock_data.current_price:.2f} <= "
                f"MA120*0.85 ${trigger_price:.2f}"
            )

            return Signal(
                signal_type=SignalType.SIGNAL_1,
                symbol=stock_data.symbol,
                name=stock_data.name,
                current_price=stock_data.current_price,
                ma120=stock_data.ma120,
                ma120_deviation_pct=stock_data.ma120_deviation,
                position_size_pct=self.SIGNAL_1_POSITION_SIZE,
                timestamp=stock_data.timestamp,
            )

        return None

    def _check_signal_2(self, stock_data: StockData, state: SignalState) -> Signal | None:
        """
        Check if Signal 2 condition is met.

        Condition: Price <= Signal1Price * 0.80 (20% below Signal 1 price)
        """
        if state.signal_1_price is None:
            logger.error(f"{stock_data.symbol}: Signal 1 triggered but no price recorded")
            return None

        trigger_price = state.signal_1_price * self.SIGNAL_2_THRESHOLD

        if stock_data.current_price <= trigger_price:
            logger.info(
                f"{stock_data.symbol}: Signal 2 triggered! "
                f"Price ${stock_data.current_price:.2f} <= "
                f"Signal1*0.80 ${trigger_price:.2f}"
            )

            return Signal(
                signal_type=SignalType.SIGNAL_2,
                symbol=stock_data.symbol,
                name=stock_data.name,
                current_price=stock_data.current_price,
                ma120=stock_data.ma120,
                ma120_deviation_pct=stock_data.ma120_deviation,
                position_size_pct=self.SIGNAL_2_POSITION_SIZE,
                timestamp=stock_data.timestamp,
                signal_1_price=state.signal_1_price,
                signal_2_trigger_price=trigger_price,
            )

        return None

    def update_state(self, signal: Signal, state: SignalState) -> SignalState:
        """
        Update state after generating a signal.

        Signal 1: Record price and date, mark as triggered
        Signal 2: Mark as triggered (will cause reset on next run)
        """
        if signal.signal_type == SignalType.SIGNAL_1:
            state.signal_1_triggered = True
            state.signal_1_price = signal.current_price
            state.signal_1_date = signal.timestamp.strftime("%Y-%m-%d")
            logger.info(
                f"{signal.symbol}: Updated state with Signal 1 at ${signal.current_price:.2f}"
            )

        elif signal.signal_type == SignalType.SIGNAL_2:
            state.signal_2_triggered = True
            state.signal_2_price = signal.current_price
            state.signal_2_date = signal.timestamp.strftime("%Y-%m-%d")
            logger.info(
                f"{signal.symbol}: Updated state with Signal 2 at ${signal.current_price:.2f}"
            )

        return state
