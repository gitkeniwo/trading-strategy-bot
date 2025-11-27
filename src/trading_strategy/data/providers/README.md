# Data Providers

This directory contains modular data provider implementations for fetching stock market data.

## Architecture

Each data provider is isolated in its own file for better maintainability and extensibility.

```
providers/
├── __init__.py              # Exports all providers
├── base.py                  # DataProvider abstract base class
├── yfinance_provider.py     # YFinance implementation (primary)
├── alphavantage_provider.py # Alpha Vantage implementation (backup)
└── README.md                # This file
```

## Available Providers

### YFinanceProvider (Primary)

**File**: `yfinance_provider.py`

**Features**:
- Free, unlimited API access
- No API key required
- Excellent pandas integration
- Reliable for educational/personal use

**Data Source**: Yahoo Finance via `yfinance` library

**Usage**:
```python
from trading_strategy.data.providers import YFinanceProvider

provider = YFinanceProvider()
data = provider.fetch_stock_data(stock_info, days=120)
```

### AlphaVantageProvider (Backup)

**File**: `alphavantage_provider.py`

**Features**:
- Enterprise-grade reliability
- 25 API calls per day (free tier)
- Requires API key

**Data Source**: [Alpha Vantage API](https://www.alphavantage.co/)

**Get API Key**: https://www.alphavantage.co/support/#api-key

**Usage**:
```python
from trading_strategy.data.providers import AlphaVantageProvider

provider = AlphaVantageProvider(api_key="YOUR_API_KEY")
data = provider.fetch_stock_data(stock_info, days=120)
```

## Adding a New Provider

To add a new data provider, follow these steps:

### 1. Create Provider File

Create a new file in this directory (e.g., `finnhub_provider.py`):

```python
"""
Finnhub data provider.

Example of adding a new provider.
"""

import logging
from typing import Optional

from trading_strategy.config.stocks import StockInfo
from trading_strategy.data.models import StockData
from trading_strategy.data.providers.base import DataProvider

logger = logging.getLogger(__name__)


class FinnhubProvider(DataProvider):
    """Data provider using Finnhub API."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_name(self) -> str:
        return "finnhub"

    def fetch_stock_data(
        self,
        stock_info: StockInfo,
        days: int = 120
    ) -> Optional[StockData]:
        """Fetch stock data using Finnhub API."""
        # Implement API logic here
        pass
```

### 2. Export Provider

Add the new provider to `__init__.py`:

```python
from trading_strategy.data.providers.finnhub_provider import FinnhubProvider

__all__ = [
    "DataProvider",
    "YFinanceProvider",
    "AlphaVantageProvider",
    "FinnhubProvider",  # Add new provider
]
```

### 3. Use in DataFetcherManager

Update `fetcher.py` to use the new provider:

```python
from trading_strategy.data.providers import FinnhubProvider

class DataFetcherManager:
    def __init__(
        self,
        alpha_vantage_api_key: Optional[str] = None,
        finnhub_api_key: Optional[str] = None
    ):
        self.primary_provider = YFinanceProvider()
        self.secondary_provider = None

        if alpha_vantage_api_key:
            self.secondary_provider = AlphaVantageProvider(alpha_vantage_api_key)
        elif finnhub_api_key:
            self.secondary_provider = FinnhubProvider(finnhub_api_key)
```

## Provider Interface

All providers must implement the `DataProvider` abstract base class:

```python
from abc import ABC, abstractmethod
from typing import Optional
from trading_strategy.config.stocks import StockInfo
from trading_strategy.data.models import StockData

class DataProvider(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """Return provider name."""
        pass

    @abstractmethod
    def fetch_stock_data(
        self,
        stock_info: StockInfo,
        days: int = 120
    ) -> Optional[StockData]:
        """Fetch stock data and return StockData or None."""
        pass
```

## Provider Requirements

Each provider implementation should:

1. ✅ Inherit from `DataProvider` base class
2. ✅ Implement `get_name()` method
3. ✅ Implement `fetch_stock_data()` method
4. ✅ Return `StockData` model with:
   - `symbol`: Stock symbol
   - `name`: Stock name
   - `current_price`: Most recent price
   - `ma120`: 120-day moving average
   - `timestamp`: Data timestamp
   - `days_of_data`: Number of days fetched
5. ✅ Handle errors gracefully and log appropriately
6. ✅ Return `None` on failure (triggers fallback)

## Testing Providers

Test individual providers:

```python
from trading_strategy.data.providers import YFinanceProvider
from trading_strategy.config.stocks import StockInfo

provider = YFinanceProvider()
stock = StockInfo(symbol="AAPL", name="Apple Inc.", category="test")
data = provider.fetch_stock_data(stock)

if data:
    print(f"Price: ${data.current_price:.2f}")
    print(f"MA120: ${data.ma120:.2f}")
    print(f"Deviation: {data.ma120_deviation:.2f}%")
```

## Fallback Logic

The `DataFetcherManager` in `fetcher.py` coordinates providers with automatic fallback:

1. Try **primary provider** (YFinance)
2. If primary fails, try **secondary provider** (Alpha Vantage)
3. If all fail, return `None`

This ensures maximum reliability with minimal manual intervention.

## Best Practices

1. **Modular Design**: Each provider is self-contained
2. **Clear Logging**: Use appropriate log levels (INFO, WARNING, ERROR)
3. **Error Handling**: Catch specific exceptions and return None on failure
4. **Type Hints**: Use proper type annotations for better IDE support
5. **Documentation**: Document API requirements, rate limits, and features
6. **Testing**: Test with real API calls during development

## Future Providers

Potential providers to add:

- **Finnhub**: https://finnhub.io/
- **IEX Cloud**: https://iexcloud.io/
- **Polygon.io**: https://polygon.io/
- **Twelve Data**: https://twelvedata.com/
- **Tiingo**: https://www.tiingo.com/

Each new provider simply needs to implement the `DataProvider` interface!
