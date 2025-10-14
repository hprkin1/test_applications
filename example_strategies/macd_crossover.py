"""
MACD (Moving Average Convergence Divergence) Crossover Strategy

This strategy generates buy signals when MACD line crosses above the signal line
and sell signals when MACD crosses below the signal line.

Parameters:
- fast_period: Fast EMA period (default: 12)
- slow_period: Slow EMA period (default: 26)
- signal_period: Signal line EMA period (default: 9)
"""

class Strategy:
    def __init__(self, fast_period=12, slow_period=26, signal_period=9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def backtest(self, data):
        """
        Execute MACD crossover strategy.
        
        Args:
            data: pandas DataFrame with OHLCV columns
            
        Returns:
            signals: pandas Series with trading signals
        """
        import pandas as pd
        
        # Calculate MACD
        exp1 = data['Close'].ewm(span=self.fast_period, adjust=False).mean()
        exp2 = data['Close'].ewm(span=self.slow_period, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=self.signal_period, adjust=False).mean()
        
        # Calculate histogram
        histogram = macd - signal_line
        
        # Generate signals based on crossovers
        signals = pd.Series(0, index=data.index)
        
        # Buy when MACD crosses above signal line
        signals[(macd > signal_line) & (macd.shift(1) <= signal_line.shift(1))] = 1
        
        # Sell when MACD crosses below signal line
        signals[(macd < signal_line) & (macd.shift(1) >= signal_line.shift(1))] = -1
        
        return signals
