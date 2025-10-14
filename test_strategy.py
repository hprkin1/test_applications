"""
Simple Moving Average Crossover Strategy
"""

class Strategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window
    
    def run(self, data):
        """
        Execute the strategy on the given data.
        
        Args:
            data: pandas DataFrame with OHLCV columns
            
        Returns:
            signals: pandas Series with 1 (buy), -1 (sell), 0 (hold)
        """
        # Calculate moving averages
        data['SMA_short'] = data['close'].rolling(window=self.short_window).mean()
        data['SMA_long'] = data['close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        data['signal'] = 0
        data.loc[data['SMA_short'] > data['SMA_long'], 'signal'] = 1
        data.loc[data['SMA_short'] < data['SMA_long'], 'signal'] = -1
        
        return data['signal']
