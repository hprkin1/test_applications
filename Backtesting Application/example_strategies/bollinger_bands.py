"""
Bollinger Bands Mean Reversion Strategy

This strategy buys when price touches the lower Bollinger Band and sells
when price touches the upper Bollinger Band.

Parameters:
- window: Period for moving average (default: 20)
- num_std: Number of standard deviations for bands (default: 2)
"""

class BollingerBandsStrategy:
    def __init__(self, window=20, num_std=2):
        self.window = window
        self.num_std = num_std
    
    def execute(self, data):
        """
        Execute Bollinger Bands strategy.
        
        Args:
            data: pandas DataFrame with OHLCV columns
            
        Returns:
            signals: pandas Series with trading signals
        """
        import pandas as pd
        
        # Calculate Bollinger Bands
        data['SMA'] = data['Close'].rolling(window=self.window).mean()
        data['STD'] = data['Close'].rolling(window=self.window).std()
        data['Upper_Band'] = data['SMA'] + (data['STD'] * self.num_std)
        data['Lower_Band'] = data['SMA'] - (data['STD'] * self.num_std)
        
        # Generate signals
        signals = pd.Series(0, index=data.index)
        
        # Buy when price touches or goes below lower band
        signals[data['Close'] <= data['Lower_Band']] = 1
        
        # Sell when price touches or goes above upper band
        signals[data['Close'] >= data['Upper_Band']] = -1
        
        # Exit positions when price returns to middle band
        signals[(data['Close'] > data['Lower_Band']) & 
                (data['Close'] < data['Upper_Band'])] = 0
        
        return signals
