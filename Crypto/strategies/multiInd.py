import numpy as np
import pandas as pd
from util.logger import log_signal
from indicators.rsi import calculate_rsi
from indicators.macd import calculate_macd
from indicators.vwap import calculate_vwap
from indicators.ema import calculate_ema
from indicators.bollinger_bands import calculate_bollinger_bands

class MultiIndicatorStrategy:
    def __init__(self, rsi_period=3, macd_fast=3, macd_slow=6, macd_signal=3, vwap_period=3):
        self.rsi_period = rsi_period
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.vwap_period = vwap_period
        self.data = pd.DataFrame(columns=['close', 'volume'])

    def update(self, price, volume):
        try:
            price, volume = float(price), float(volume)
            new_data = pd.DataFrame({'close': [price], 'volume': [volume]})
            self.data = pd.concat([self.data, new_data], ignore_index=True)

            max_len = max(self.rsi_period, self.macd_slow, self.vwap_period)
            if len(self.data) > max_len:
                self.data = self.data.iloc[-max_len:]

            self.data['close'] = pd.to_numeric(self.data['close'], errors='coerce')
            self.data['volume'] = pd.to_numeric(self.data['volume'], errors='coerce')
            self.data.dropna(inplace=True)
        except ValueError:
            print("Invalid price or volume data")

    def generate_signals(self):
        # print(self.data.tail(10))  # See indicator values before signal generation

        if len(self.data) < max(self.rsi_period, self.macd_slow, self.vwap_period,10):
            return pd.DataFrame({'Signal': ['HOLD'], 'Reason': ["Not enough data"]})

        try:
            self.data['RSI'] = calculate_rsi(self.data, self.rsi_period)
            self.data['MACD'], self.data['MACD_Signal'], _ = calculate_macd(self.data, self.macd_fast, self.macd_slow, self.macd_signal)
            self.data['VWAP'] = calculate_vwap(self.data)
            ema_values = calculate_ema(self.data['close'].tolist(), self.vwap_period)
            if not ema_values or len(ema_values) < self.vwap_period:
                return pd.DataFrame({'Signal': ['HOLD'], 'Reason': ["Insufficient data for EMA"]})
            self.data['EMA'] = pd.Series(ema_values)
            try:
                self.data['Bollinger_Upper'], self.data['Bollinger_Lower'] = calculate_bollinger_bands(
                    self.data, period=10, std_dev=2
                )
            except Exception as e:
                print("Error calculating Bollinger Bands:", e)
                return pd.DataFrame({'Signal': ['HOLD'], 'Reason': ["Bollinger Bands calculation failed"]})

        except Exception as e:
            print(f"Error calculating indicators: {e}")

        print("Latest Data:")
        print(self.data.tail())

        latest_price = self.data.iloc[-1]['close']
        latest_vwap = self.data.iloc[-1]['VWAP']

        if latest_vwap == 0.0:
            log_signal("MultiIndicatorStrategy", "HOLD", latest_price, "VWAP not ready yet")
            return "HOLD"

        if latest_price < latest_vwap and self.data.iloc[-1]['RSI'] < 30:
            log_signal("MultiIndicatorStrategy", "BUY", latest_price, "RSI Oversold + Below VWAP")
            return pd.DataFrame({'Signal': ['BUY'], 'Reason': ["RSI Oversold + Below VWAP"]})

        if latest_price > latest_vwap and self.data.iloc[-1]['RSI'] > 70:
            if self.data.iloc[-1]['MACD'] < self.data.iloc[-1]['MACD_Signal']:  # MACD Bearish Crossover
                log_signal("MultiIndicatorStrategy", "SELL", latest_price, "RSI Overbought + Above VWAP + MACD Bearish")
                return "SELL"


        if latest_price > self.data.iloc[-1]['Bollinger_Upper']:
            log_signal("MultiIndicatorStrategy", "SELL", latest_price, "Price Above Bollinger Upper Band")
            return pd.DataFrame({'Signal': ['SELL'], 'Reason': ["Price Above Bollinger Upper Band"]})

        log_signal("MultiIndicatorStrategy", "HOLD", latest_price, f"Price: {latest_price} = VWAP: {latest_vwap}")
        return pd.DataFrame({'Signal': ['HOLD'], 'Reason': [f"Price: {latest_price} = VWAP: {latest_vwap}"]})
