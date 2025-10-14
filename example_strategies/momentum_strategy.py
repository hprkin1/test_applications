"""
Momentum Strategy

This strategy buys when price momentum is strong and positive, and sells
when momentum is strong and negative.

Parameters:
- lookback: Period to calculate momentum (default: 10)
- threshold: Minimum momentum to trigger signal (default: 0.02 = 2%)
"""

def run_strategy(data, lookback=10, threshold=0.02):
    """
    Momentum-based trading strategy.
    
    Args:
        data: pandas DataFrame with OHLCV data
        lookback: Number of periods to look back for momentum
        threshold: Minimum momentum percentage to trigger signal
    
    Returns:
        signals: pandas Series with 1 (buy), -1 (sell), 0 (hold)
    """
    import pandas as pd
    
    # Calculate momentum (percentage change over lookback period)
    data['momentum'] = data['Close'].pct_change(lookback)
    
    # Generate signals based on momentum threshold
    signals = pd.Series(0, index=data.index)
    
    # Buy when momentum is strongly positive
    signals[data['momentum'] > threshold] = 1
    
    # Sell when momentum is strongly negative
    signals[data['momentum'] < -threshold] = -1
    
    # Hold when momentum is weak (between -threshold and +threshold)
    signals[(data['momentum'] >= -threshold) & (data['momentum'] <= threshold)] = 0
    
    return signals
