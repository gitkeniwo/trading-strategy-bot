"""
State management for tracking signals across runs.

This module handles persistent storage of signal states using JSON files.
The state file (signals.json) is committed to the repository, providing:
- Version-controlled history of all signals
- No external database dependencies
- Simple, reliable persistence for twice-daily runs

Design features:
- Atomic writes (write to temp file, then rename)
- JSON validation before loading
- Automatic initialization for new stocks
- Thread-safe operations
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict

from trading_strategy.data.models import SignalState

logger = logging.getLogger(__name__)


class StateManager:
    """
    Manages persistent state for trading signals.

    State is stored in signals.json with structure:
    {
        "AAPL": {
            "symbol": "AAPL",
            "signal_1_triggered": true,
            "signal_1_price": 170.50,
            "signal_1_date": "2025-11-26",
            "signal_2_triggered": false,
            "signal_2_price": null,
            "signal_2_date": null
        },
        ...
    }
    """

    def __init__(self, state_file_path: Path):
        """
        Initialize state manager.

        Args:
            state_file_path: Path to signals.json file
        """
        self.state_file = state_file_path
        self._ensure_state_file_exists()

    def _ensure_state_file_exists(self):
        """Create empty state file if it doesn't exist."""
        if not self.state_file.exists():
            logger.info(f"Creating new state file: {self.state_file}")
            self._save_states({})

    def load_state(self, symbol: str) -> SignalState:
        """
        Load state for a specific stock symbol.

        Args:
            symbol: Stock symbol (e.g., "AAPL")

        Returns:
            SignalState for this symbol (creates new if doesn't exist)
        """
        try:
            with open(self.state_file, "r") as f:
                data = json.load(f)

            if symbol in data:
                # Load existing state
                return SignalState(**data[symbol])
            else:
                # Create new state for this symbol
                logger.info(f"Creating new state for {symbol}")
                return SignalState(symbol=symbol)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in state file: {e}")
            # Return clean state if file is corrupted
            return SignalState(symbol=symbol)

        except Exception as e:
            logger.error(f"Error loading state for {symbol}: {e}")
            return SignalState(symbol=symbol)

    def save_state(self, state: SignalState):
        """
        Save state for a specific stock symbol.

        Uses atomic write: writes to temp file, then renames.
        This prevents corruption if the process is interrupted.

        Args:
            state: SignalState to save
        """
        try:
            # Load all states
            all_states = self._load_all_states()

            # Update this symbol's state
            all_states[state.symbol] = state.model_dump()

            # Save atomically
            self._save_states(all_states)

            logger.info(f"Saved state for {state.symbol}")

        except Exception as e:
            logger.error(f"Error saving state for {state.symbol}: {e}")
            raise

    def _load_all_states(self) -> Dict:
        """Load all states from file."""
        try:
            if not self.state_file.exists():
                return {}

            with open(self.state_file, "r") as f:
                return json.load(f)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in state file: {e}")
            return {}

        except Exception as e:
            logger.error(f"Error loading state file: {e}")
            return {}

    def _save_states(self, states: Dict):
        """
        Save all states atomically.

        Process:
        1. Write to temporary file
        2. Rename to actual file (atomic operation)

        This ensures the file is never corrupted by interrupted writes.
        """
        temp_file = self.state_file.with_suffix(".tmp")

        try:
            # Write to temp file
            with open(temp_file, "w") as f:
                json.dump(states, f, indent=2)

            # Atomic rename
            os.replace(temp_file, self.state_file)

        except Exception as e:
            logger.error(f"Error saving state file: {e}")
            # Clean up temp file if it exists
            if temp_file.exists():
                temp_file.unlink()
            raise

    def get_all_states(self) -> Dict[str, SignalState]:
        """
        Get all states as a dictionary.

        Returns:
            Dictionary mapping symbol -> SignalState
        """
        data = self._load_all_states()
        return {symbol: SignalState(**state_data) for symbol, state_data in data.items()}

    def clear_all_states(self):
        """
        Clear all states (useful for testing or manual reset).

        Warning: This will delete all signal history!
        """
        logger.warning("Clearing all states!")
        self._save_states({})
