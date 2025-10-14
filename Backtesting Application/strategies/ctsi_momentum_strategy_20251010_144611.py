"""
Momentum Crypto Strategy using Accelerator Oscillator (AC) Indicator
Adapted for QuantFlow Platform

Strategy Logic:
- Long when AO > AC (Awesome Oscillator greater than Accelerator)
- Short when AO < AC (Awesome Oscillator less than Accelerator)
- Uses AC indicator derived from Awesome Oscillator (AO)

Original: CTSI_Class.py - MomentumCryptoACStrategy
"""

class Strategy:
    def __init__(self, short_sma_period=5, long_sma_period=34, ao_sma_period=5):
        """
        Initialize the Momentum AC Strategy.
        
        Parameters:
            short_sma_period: Period for short SMA of median price (default: 5)
            long_sma_period: Period for long SMA of median price (default: 34)
            ao_sma_period: Period for SMA of Awesome Oscillator (default: 5)
        """
        self.short_sma_period = short_sma_period
        self.long_sma_period = long_sma_period
        self.ao_sma_period = ao_sma_period
    
    def calculate_ac_indicator(self, data):
        """
        Calculate the Accelerator Oscillator (AC) from OHLCV data.
        
        Steps:
        1. Calculate Median Price = (High + Low) / 2
        2. Calculate short and long SMAs of Median Price
        3. Calculate Awesome Oscillator (AO) = SMA_Short - SMA_Long
        4. Calculate SMA of AO
        5. Calculate Accelerator (AC) = AO - SMA_AO
        
        Parameters:
            data: pandas DataFrame with High and Low columns
            
        Returns:
            DataFrame with AC, AO, and intermediate calculations
        """
        import pandas as pd
        
        df = data.copy()
        
        # Normalize column names to handle both uppercase and lowercase
        df.columns = [col.capitalize() for col in df.columns]
        
        # Calculate Median Price
        df['Median_Price'] = (df['High'] + df['Low']) / 2
        
        # Calculate short and long period SMAs of the Median Price
        df['SMA_Short'] = df['Median_Price'].rolling(window=self.short_sma_period).mean()
        df['SMA_Long'] = df['Median_Price'].rolling(window=self.long_sma_period).mean()
        
        # Calculate Awesome Oscillator (AO)
        df['AO'] = df['SMA_Short'] - df['SMA_Long']
        
        # Calculate SMA of the AO
        df['SMA_AO'] = df['AO'].rolling(window=self.ao_sma_period).mean()
        
        # Calculate Accelerator Oscillator (AC)
        df['AC'] = df['AO'] - df['SMA_AO']
        
        return df
    
    def run(self, data):
        """
        Execute the Momentum AC strategy on the given data.
        
        Args:
            data: pandas DataFrame with OHLCV columns
                  Expected columns: Date, Open, High, Low, Close, Volume
        
        Returns:
            signals: pandas Series with trading signals
                     1 = Long (buy)
                     -1 = Short (sell)
                     0 = Hold/No position
        """
        import pandas as pd
        
        # Calculate AC indicator
        df = self.calculate_ac_indicator(data)
        
        # Generate signals based on strategy logic
        # Long when AO > AC (Awesome Oscillator is above Accelerator)
        # Short when AO < AC (Awesome Oscillator is below Accelerator)
        signals = pd.Series(0, index=df.index)
        
        # Long signal: AO > AC
        signals[df['AO'] > df['AC']] = 1
        
        # Short signal: AO < AC
        signals[df['AO'] < df['AC']] = -1
        
        # Handle NaN values from rolling calculations
        signals.fillna(0, inplace=True)
        
        return signals
    
    def get_indicator_values(self, data):
        """
        Helper method to get AC and AO values for analysis.
        Not required by QuantFlow but useful for debugging.
        
        Args:
            data: pandas DataFrame with OHLCV columns
            
        Returns:
            DataFrame with AC, AO, and other indicators
        """
        return self.calculate_ac_indicator(data)


# Alternative function-based implementation (also valid for QuantFlow)
def strategy(data, short_sma_period=5, long_sma_period=34, ao_sma_period=5):
    """
    Momentum AC Strategy as a standalone function.
    
    Args:
        data: pandas DataFrame with OHLCV columns
        short_sma_period: Period for short SMA (default: 5)
        long_sma_period: Period for long SMA (default: 34)
        ao_sma_period: Period for AO SMA (default: 5)
    
    Returns:
        signals: pandas Series with 1 (long), -1 (short), 0 (hold)
    """
    import pandas as pd
    
    df = data.copy()
    
    # Normalize column names
    df.columns = [col.capitalize() for col in df.columns]
    
    # Calculate Median Price
    df['Median_Price'] = (df['High'] + df['Low']) / 2
    
    # Calculate SMAs
    df['SMA_Short'] = df['Median_Price'].rolling(window=short_sma_period).mean()
    df['SMA_Long'] = df['Median_Price'].rolling(window=long_sma_period).mean()
    
    # Calculate Awesome Oscillator (AO)
    df['AO'] = df['SMA_Short'] - df['SMA_Long']
    
    # Calculate SMA of AO
    df['SMA_AO'] = df['AO'].rolling(window=ao_sma_period).mean()
    
    # Calculate Accelerator Oscillator (AC)
    df['AC'] = df['AO'] - df['SMA_AO']
    
    # Generate signals
    signals = pd.Series(0, index=df.index)
    signals[df['AO'] > df['AC']] = 1   # Long
    signals[df['AO'] < df['AC']] = -1  # Short
    signals.fillna(0, inplace=True)
    
    return signals
