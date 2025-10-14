"""
RSI (Relative Strength Index) Mean Reversion Strategy

This strategy buys when RSI indicates oversold conditions and sells when
RSI indicates overbought conditions.

Parameters:
- rsi_period: Period for RSI calculation (default: 14)
- oversold: RSI threshold for buy signal (default: 30)
- overbought: RSI threshold for sell signal (default: 70)
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
    
    # Avoid division by zero
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    
    # Generate signals
    signals = pd.Series(0, index=data.index)
    signals[rsi < oversold] = 1   # Buy when oversold
    signals[rsi > overbought] = -1  # Sell when overbought
    
    return signals
