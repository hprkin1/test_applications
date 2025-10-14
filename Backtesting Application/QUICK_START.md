# QuantFlow Quick Start Guide

## Strategy Format Summary

Your Python strategy file must contain **ONE** of these:

### ✅ Option 1: Class with Method
```python
class Strategy:
    def run(self, data):
        # Your logic here
        return signals
```

**Accepted method names:** `run()`, `execute()`, or `backtest()`

### ✅ Option 2: Standalone Function
```python
def strategy(data):
    # Your logic here
    return signals
```

**Accepted function names:** `strategy()`, `run_strategy()`, or `backtest()`

## Input/Output

### Input: `data` (pandas DataFrame)
```
Columns: Date, Open, High, Low, Close, Volume
```

### Output: `signals` (pandas Series)
```
1  = Buy/Long
-1 = Sell/Short
0  = Hold/No action
```

## Minimal Working Example

```python
class Strategy:
    def run(self, data):
        import pandas as pd
        
        # Simple logic: buy when close > 20-day average
        sma = data['Close'].rolling(20).mean()
        signals = pd.Series(0, index=data.index)
        signals[data['Close'] > sma] = 1
        signals[data['Close'] < sma] = -1
        
        return signals
```

## Example Strategies Included

Check the `example_strategies/` folder:
- `sma_crossover.py` - Moving average crossover
- `rsi_strategy.py` - RSI mean reversion
- `bollinger_bands.py` - Bollinger Bands strategy
- `macd_crossover.py` - MACD crossover
- `momentum_strategy.py` - Momentum-based trading

## Common Mistakes

❌ **Wrong method name**
```python
class Strategy:
    def calculate(self, data):  # Should be run(), execute(), or backtest()
```

❌ **No class or function**
```python
# Just code, no callable structure
signals = data['Close'] > data['Close'].mean()
```

❌ **Wrong return type**
```python
def strategy(data):
    return data  # Should return signals (pandas Series), not DataFrame
```

## Testing Your Strategy Locally

Before uploading, test it:

```python
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Test your strategy
from your_strategy import Strategy
strategy = Strategy()
signals = strategy.run(data)

# Check output
print(signals.value_counts())  # Should show counts of 1, -1, 0
```

## Upload via Frontend

1. Go to **Strategies** page
2. Click **Upload New Strategy**
3. Fill in name and description
4. Select your `.py` file
5. Click **Upload Strategy**

The system will validate your file automatically!

## Need Help?

- See `STRATEGY_FORMAT.md` for detailed documentation
- Check example strategies in `example_strategies/`
- API docs: http://localhost:8000/docs
