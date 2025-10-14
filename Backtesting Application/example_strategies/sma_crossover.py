"""
Simple Moving Average (SMA) Crossover Strategy

This strategy generates buy signals when a short-term moving average crosses
above a long-term moving average, and sell signals when it crosses below.

Parameters:
- short_window: Period for short-term SMA (default: 20)
- long_window: Period for long-term SMA (default: 50)
"""

class Strategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window
    
    def run(self, data):
        """
        Execute the SMA crossover strategy.
        
        Args:
            data: pandas DataFrame with OHLCV columns
            
        Returns:
            signals: pandas Series with 1 (buy), -1 (sell), 0 (hold)
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
