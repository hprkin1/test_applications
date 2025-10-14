# QuantFlow Strategy Format Guide

## Overview

QuantFlow accepts Python strategy files (`.py`) that define trading logic. Your strategy must contain **either**:
1. A **class** with a `run()`, `execute()`, or `backtest()` method, **OR**
2. A **function** named `strategy()`, `run_strategy()`, or `backtest()`

## Validation

When you upload a strategy, QuantFlow:
- Parses the Python file using AST (Abstract Syntax Tree)
- Checks for required methods/functions
- Validates Python syntax
- Stores the file securely

## Format 1: Class-Based Strategy (Recommended)

```python
"""
Simple Moving Average Crossover Strategy
"""

class Strategy:
    def __init__(self, short_window=20, long_window=50):
        """Initialize strategy parameters"""
        self.short_window = short_window
        self.long_window = long_window
    
    def run(self, data):
        """
        Execute the strategy on the given data.
        
        Args:
            data: pandas DataFrame with OHLCV columns
                  Columns: Date, Open, High, Low, Close, Volume
            
        Returns:
            signals: pandas Series with trading signals
                     1 = buy, -1 = sell, 0 = hold
        """
        import pandas as pd
        
        # Calculate moving averages
        data['SMA_short'] = data['Close'].rolling(window=self.short_window).mean()
        data['SMA_long'] = data['Close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        data['signal'] = 0
        data.loc[data['SMA_short'] > data['SMA_long'], 'signal'] = 1  # Buy
        data.loc[data['SMA_short'] < data['SMA_long'], 'signal'] = -1  # Sell
        
        return data['signal']
```

## Format 2: Function-Based Strategy

```python
"""
RSI Mean Reversion Strategy
"""

def strategy(data, rsi_period=14, oversold=30, overbought=70):
    """
    RSI-based mean reversion strategy.
    
    Args:
        data: pandas DataFrame with OHLCV data
        rsi_period: Period for RSI calculation
        oversold: RSI level to trigger buy
        overbought: RSI level to trigger sell
    
    Returns:
        signals: pandas Series with 1 (buy), -1 (sell), 0 (hold)
    """
    import pandas as pd
    import numpy as np
    
    # Calculate RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Generate signals
    signals = pd.Series(0, index=data.index)
    signals[rsi < oversold] = 1   # Buy when oversold
    signals[rsi > overbought] = -1  # Sell when overbought
    
    return signals
```

## Format 3: Alternative Method Names

You can use any of these method/function names:

### Class Methods:
- `run(self, data)`
- `execute(self, data)`
- `backtest(self, data)`

### Functions:
- `strategy(data)`
- `run_strategy(data)`
- `backtest(data)`

## Data Format

The `data` parameter passed to your strategy is a **pandas DataFrame** with these columns:

| Column | Type | Description |
|--------|------|-------------|
| Date | datetime | Trading date/time |
| Open | float | Opening price |
| High | float | Highest price |
| Low | float | Lowest price |
| Close | float | Closing price |
| Volume | float | Trading volume |

**Note:** Column names may be lowercase (`open`, `high`, `low`, `close`, `volume`) depending on the dataset source.

## Signal Format

Your strategy should return a **pandas Series** with integer signals:
- `1` = **Buy/Long** signal
- `-1` = **Sell/Short** signal
- `0` = **Hold/No action**

## Example Strategies

### 1. Bollinger Bands Strategy

```python
class BollingerBandsStrategy:
    def __init__(self, window=20, num_std=2):
        self.window = window
        self.num_std = num_std
    
    def run(self, data):
        import pandas as pd
        
        # Calculate Bollinger Bands
        data['SMA'] = data['Close'].rolling(window=self.window).mean()
        data['STD'] = data['Close'].rolling(window=self.window).std()
        data['Upper'] = data['SMA'] + (data['STD'] * self.num_std)
        data['Lower'] = data['SMA'] - (data['STD'] * self.num_std)
        
        # Generate signals
        signals = pd.Series(0, index=data.index)
        signals[data['Close'] < data['Lower']] = 1   # Buy at lower band
        signals[data['Close'] > data['Upper']] = -1  # Sell at upper band
        
        return signals
```

### 2. MACD Strategy

```python
def strategy(data):
    """MACD Crossover Strategy"""
    import pandas as pd
    
    # Calculate MACD
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=9, adjust=False).mean()
    
    # Generate signals
    signals = pd.Series(0, index=data.index)
    signals[macd > signal_line] = 1   # Buy when MACD crosses above signal
    signals[macd < signal_line] = -1  # Sell when MACD crosses below signal
    
    return signals
```

### 3. Momentum Strategy

```python
class MomentumStrategy:
    def __init__(self, lookback=10, threshold=0.02):
        self.lookback = lookback
        self.threshold = threshold
    
    def run(self, data):
        import pandas as pd
        
        # Calculate momentum
        data['momentum'] = data['Close'].pct_change(self.lookback)
        
        # Generate signals based on momentum threshold
        signals = pd.Series(0, index=data.index)
        signals[data['momentum'] > self.threshold] = 1   # Strong upward momentum
        signals[data['momentum'] < -self.threshold] = -1  # Strong downward momentum
        
        return signals
```

## Best Practices

1. **Import libraries inside methods/functions** - This ensures they're available when executed in the sandboxed environment.

2. **Handle NaN values** - Moving averages and indicators create NaN values at the start:
   ```python
   signals.fillna(0, inplace=True)
   ```

3. **Use vectorized operations** - Pandas vectorized operations are much faster than loops:
   ```python
   # Good
   signals[data['Close'] > data['SMA']] = 1
   
   # Avoid
   for i in range(len(data)):
       if data['Close'].iloc[i] > data['SMA'].iloc[i]:
           signals.iloc[i] = 1
   ```

4. **Add docstrings** - Document your strategy logic for future reference.

5. **Test locally first** - Test your strategy with sample data before uploading:
   ```python
   import pandas as pd
   
   # Load sample data
   data = pd.read_csv('sample_data.csv')
   
   # Test strategy
   strategy = Strategy()
   signals = strategy.run(data)
   print(signals.value_counts())
   ```

## Common Errors

### ❌ Missing Required Method
```python
class Strategy:
    def calculate(self, data):  # Wrong method name!
        return signals
```
**Fix:** Use `run()`, `execute()`, or `backtest()`

### ❌ No Class or Function
```python
# Just calculations, no callable strategy
sma = data['Close'].rolling(20).mean()
```
**Fix:** Wrap in a class or function

### ❌ Wrong Return Type
```python
def strategy(data):
    return data  # Should return signals, not full DataFrame
```
**Fix:** Return a pandas Series with signals

## Current Limitations (MVP)

⚠️ **Note:** The current MVP implementation runs a simple buy-and-hold backtest and doesn't execute uploaded strategy code yet. Full strategy execution with sandboxing is coming in the next iteration.

The validation still checks your strategy format to ensure it's ready for when execution is implemented.

## Next Steps

Once uploaded, your strategy will be:
1. Validated for correct format
2. Stored securely
3. Available for selection in backtests
4. Executed in a sandboxed Docker container (coming soon)

## Questions?

Check the example strategies in the repository or refer to the API documentation at `http://localhost:8000/docs`
