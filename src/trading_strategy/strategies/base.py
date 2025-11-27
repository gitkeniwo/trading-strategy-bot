"""
Base class for trading strategies.

This module provides an abstract base class that all strategies must implement.
Makes it easy to add new strategies (like Monthly MA5) in the future.
"""

from abc import ABC, abstractmethod
from typing import List

from trading_strategy.data.models import Signal, SignalState, StockData


class Strategy(ABC):
    """Abstract base class for trading strategies."""

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this strategy."""
        pass

    @abstractmethod
    def evaluate(self, stock_data: StockData, state: SignalState) -> List[Signal]:
        """
        Evaluate the strategy for a given stock.

        Args:
            stock_data: Current stock data with price and MA120
            state: Persistent state for this stock (tracks previous signals)

        Returns:
            List of signals generated (empty list if no signals)
        """
        pass

    @abstractmethod
    def update_state(self, signal: Signal, state: SignalState) -> SignalState:
        """
        Update the persistent state after generating a signal.

        Args:
            signal: The signal that was just generated
            state: Current state for this stock

        Returns:
            Updated state to be persisted
        """
        pass
