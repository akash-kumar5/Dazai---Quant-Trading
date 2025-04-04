import pandas as pd
import numpy as np
from collections import deque
from util.logger import log_signal

class TrendSurferStrategy:
    def __init__(self, ema_period=20, adx_period=14, rsi_period=14, atr_period=14, data_window=100):
        self.ema_period = ema_period
        self.adx_period = adx_period
        self.rsi_period = rsi_period
        self.atr_period = atr_period
        self.data_window = data_window  # Limit stored data for efficiency
        
        self.data = deque(maxlen=data_window)
    
    def update(self, price, high, low, volume):
        """Updates historical data with new OHLCV values."""
        self.data.append({'Price': price, 'High': high, 'Low': low, 'Volume': volume})
        # log_signal("TrendSurferStrategy", "Updated Data", price, volume)

    def calculate_indicators(self):
        """Calculates EMA, ADX, RSI, ATR."""
        df = pd.DataFrame(self.data)
        if len(df) < max(self.ema_period, self.adx_period, self.rsi_period, self.atr_period):
            return None  # Not enough data yet

        # Calculate EMA
        df["EMA"] = df["Price"].ewm(span=self.ema_period, adjust=False).mean()
        
        # Calculate RSI
        delta = df["Price"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(self.rsi_period).mean()
        avg_loss = pd.Series(loss).rolling(self.rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-10)  # Avoid division by zero
        df["RSI"] = 100 - (100 / (1 + rs))
        
        # Calculate ATR
        df["TR"] = np.maximum(df["High"] - df["Low"], np.maximum(abs(df["High"] - df["Price"].shift(1)), abs(df["Low"] - df["Price"].shift(1))))
        df["ATR"] = df["TR"].rolling(self.atr_period).mean()
        
        # Calculate ADX
        df["+DM"] = np.where(df["High"].diff() > df["Low"].diff(), df["High"].diff(), 0)
        df["-DM"] = np.where(df["Low"].diff() > df["High"].diff(), df["Low"].diff(), 0)
        df["+DI"] = 100 * df["+DM"].rolling(self.adx_period).mean() / df["ATR"]
        df["-DI"] = 100 * df["-DM"].rolling(self.adx_period).mean() / df["ATR"]
        df["DX"] = (abs(df["+DI"] - df["-DI"]) / (df["+DI"] + df["-DI"] + 1e-10)) * 100
        df["ADX"] = df["DX"].rolling(self.adx_period).mean()
        
        return df

    def generate_signals(self):
        """Generates trading signals based on indicators."""
        df = self.calculate_indicators()
        if df is None:
            log_signal("TrendSurferStrategy", "Not enough data for signal", None)
            return pd.DataFrame()
        
        latest_row = df.iloc[-1]
        
        # Trading logic with ADX filter
        if latest_row["Price"] > latest_row["EMA"] and latest_row["RSI"] > 50 and latest_row["ADX"] > 20:
            signal = "BUY"
        elif latest_row["Price"] < latest_row["EMA"] and latest_row["RSI"] < 50 and latest_row["ADX"] > 20:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        log_signal("TrendSurferStrategy", f"Signal Generated: {signal}", latest_row["Price"])
        
        return pd.DataFrame({"Price": [latest_row["Price"]], "Signal": [signal]})
