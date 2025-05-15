import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from collections import deque


class SimpleMovingAverageStrategy:
    def __init__(self, short_period=20, long_period=50):
        self.short_period = short_period
        self.long_period = long_period
        self.data = deque(maxlen=max(short_period, long_period))
        self.trades = []
        self.active_trade = None

    def update(self, price, high, low, volume):
        self.data.append({'Price': price, 'High': high, 'Low': low, 'Volume': volume})
    
    def calculate_indicators(self):
        df = pd.DataFrame(self.data)
        if len(df) < self.long_period:
            return None

        # Calculate moving averages
        df['Short_MA'] = df['Price'].rolling(window=self.short_period).mean()
        df['Long_MA'] = df['Price'].rolling(window=self.long_period).mean()
        
        return df

    def generate_signals(self):
        df = self.calculate_indicators()
        if df is None:
            return pd.DataFrame()

        latest_row = df.iloc[-1]
        signal = 'HOLD'

        # Force signal on every bar based on MA comparison
        if latest_row['Short_MA'] > latest_row['Long_MA']:
            signal = 'BUY'
        else:
            signal = 'SELL'

        print(f"Signal generated: {signal} at price {latest_row['Price']}")
        return pd.DataFrame({
            'Price': [latest_row['Price']],
            'Signal': [signal]
        })


    def run_backtest(self, data):
        all_signals = []

        for i, row in data.iterrows():
            self.update(
                price=row['Close'],
                high=row['High'],
                low=row['Low'],
                volume=row['Volume']
            )
            signal_df = self.generate_signals()
            print(f"Signal DataFrame: {signal_df}")
            if not signal_df.empty:
                signal_df['Timestamp'] = i
                all_signals.append(signal_df)

        return pd.concat(all_signals).reset_index(drop=True) if all_signals else pd.DataFrame()

