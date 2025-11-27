# MA120 Deviation Strategy - Educational Guide

## Strategy Overview

The **MA120 Deviation Strategy** is a value-averaging approach for long-term stock accumulation. It uses price deviations from the 120-day moving average to identify potential buying opportunities during market dips.

### Key Concept

The strategy is based on **mean reversion**: prices that deviate significantly from their moving average tend to return toward that average over time.

## How It Works

### Signal 1: 15% Below MA120

**Trigger**: When stock price drops **15% or more** below its 120-day moving average

**Action**: Buy **20% of allocated capital** for this stock

**Rationale**:
- 120-day MA (~6 months) represents medium-term price trend
- 15% deviation suggests potential oversold condition
- Historical data shows such deviations often correct upward
- Not trying to time the bottom perfectly - starting accumulation at discount

**Example**:
```
MA120 = $200
Current Price = $170 (15% below MA120)
→ Signal 1 triggers
→ Buy 20% position
```

### Signal 2: 20% Below Signal 1 Price

**Trigger**: After Signal 1, if price drops **another 20%** from Signal 1 price

**Action**: Buy **additional 20% of allocated capital**

**Rationale**:
- Dollar-cost averaging: accumulate more at lower prices
- Reduces average cost basis
- Spreads risk across two entry points
- 20% additional drop represents significant further discount

**Example**:
```
Signal 1 Price = $170
Current Price = $136 (20% below $170)
→ Signal 2 triggers
→ Buy another 20% position
Total position: 40%
```

### State Reset

After Signal 2 triggers, the system resets for this stock, allowing future Signal 1 triggers if price rises and falls again.

## Why These Thresholds?

### 15% for Signal 1

- **Conservative enough**: Not every minor dip triggers a signal
- **Aggressive enough**: Catches meaningful corrections
- **Historical precedent**: Many market corrections are 10-20%
- **Risk-managed**: Preserves 80% of capital for other opportunities

### 20% for Signal 2

- **Meaningful discount**: Represents a crash or severe correction
- **Not trying to catch the knife**: Some decline has already occurred
- **Dollar-cost averaging**: Classic DCA strategy uses multiple entries
- **Total position**: 40% allows keeping 60% for diversification

## Position Sizing Philosophy

### 20% per signal

- **Diversification**: Can track 8 stocks (SPY + Mag 7)
- **Risk management**: No single stock is >40% of capital
- **Flexibility**: Capital remains for other opportunities
- **Psychological**: Easier to hold through volatility

### Why NOT go all-in?

- **Market timing is hard**: Can't predict exact bottom
- **Multiple opportunities**: Other stocks may also signal
- **Preservation of capital**: Keep reserves for unknown opportunities
- **Reduces regret**: Multiple entries reduce "what if" thinking

## What This Strategy Is NOT

### ❌ Not a get-rich-quick scheme
- This is for **long-term accumulation**
- Positions may take months/years to appreciate
- Requires patience and discipline

### ❌ Not market timing
- You're NOT trying to predict tops and bottoms
- You're buying at pre-defined discount levels
- Removes emotion from decision-making

### ❌ Not a complete system
- **Missing**: Sell signals (when to take profits)
- **Missing**: Position sizing based on volatility
- **Missing**: Correlation analysis across portfolio
- **Missing**: Risk management for black swan events

### ❌ Not financial advice
- This is an educational tool
- Past performance ≠ future results
- Always do your own research

## When to Sell? (Not Implemented)

The current system only generates **buy** signals. Here are considerations for future sell logic:

### Option 1: Mean Reversion Exit
- Sell when price returns to MA120
- Simple, aligns with mean reversion theory
- May exit too early in strong trends

### Option 2: Trailing Stop
- Sell if price drops X% from recent high
- Preserves gains while allowing upside
- Requires more complex state tracking

### Option 3: Time-Based
- Hold for fixed period (e.g., 1 year)
- Simple tax management (long-term capital gains)
- Ignores market conditions

### Option 4: Manual
- System notifies, you decide
- Keeps human judgment in the loop
- Requires active monitoring

## Risk Considerations

### ⚠️ Market Risk
- Strategy assumes mean reversion
- In downtrends, "buying the dip" can lead to losses
- No protection against prolonged bear markets

### ⚠️ Concentration Risk
- Mag 7 stocks are highly correlated
- All tech stocks may fall together
- Consider broader diversification

### ⚠️ Timing Risk
- Twice-daily checks may miss intraday extremes
- Uses closing prices, not optimal entries
- Acceptable for long-term strategy

### ⚠️ Data Risk
- Free APIs may have delays or errors
- yfinance is community-maintained (not official)
- Always verify critical decisions manually

## Best Practices

### ✅ Start Small
- Test with small capital first
- Validate notifications work correctly
- Ensure you understand the strategy

### ✅ Keep Records
- `signals.json` is version controlled
- Review historical signals periodically
- Learn from past triggers

### ✅ Stay Disciplined
- Don't override signals emotionally
- Don't chase stocks that didn't signal
- Trust the process over time

### ✅ Regular Review
- Check strategy performance monthly
- Adjust thresholds if needed (15% and 20% are not sacred)
- Consider adding/removing stocks

### ✅ Combine with Fundamentals
- Strategy is purely technical (price-based)
- Research company fundamentals separately
- Ensure you understand what you own

## Educational Resources

### Books
- "A Random Walk Down Wall Street" by Burton Malkiel
- "The Intelligent Investor" by Benjamin Graham
- "Common Sense on Mutual Funds" by John Bogle

### Concepts to Learn
- **Moving Averages**: SMA, EMA, and their uses
- **Mean Reversion**: Theory and evidence
- **Dollar-Cost Averaging**: Pros and cons
- **Portfolio Theory**: Diversification and correlation
- **Risk Management**: Position sizing and stops

### Free Online Resources
- Investopedia (investing basics)
- Khan Academy (finance and capital markets)
- QuantConnect / Quantopian (backtesting frameworks)

## Future Enhancements

This strategy is intentionally simple (MVP). Future versions could add:

1. **Strategy 1**: Monthly MA5 crossover (from original conversation)
2. **Backtesting**: Historical performance analysis
3. **Risk Metrics**: Sharpe ratio, max drawdown, etc.
4. **Sell Signals**: Complete the trade lifecycle
5. **Portfolio View**: Track actual positions and P&L
6. **Correlation Analysis**: Adjust sizing based on correlation
7. **Volatility Adjustment**: Larger positions for less volatile stocks
8. **Machine Learning**: Optimize thresholds based on historical data

## Disclaimer

This strategy is for **educational purposes only**.

- Not financial advice
- Not a recommendation to buy or sell
- Past performance does not guarantee future results
- Always consult a licensed financial advisor
- Only invest money you can afford to lose
- Understand all risks before trading

**Use at your own risk.**

---

## Questions?

If you have questions about the strategy:

1. Review the code in `src/trading_strategy/strategies/ma120_deviation.py`
2. Check logs in GitHub Actions for actual trigger prices
3. Backtest with historical data to understand behavior
4. Consult educational resources above

Happy learning! 📚📈
