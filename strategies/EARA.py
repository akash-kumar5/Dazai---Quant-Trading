import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import numpy as np
from collections import deque
from util.logger import log_signal
from core.regime_classifier import MarketRegimeClassifier
from core.indicators import Indicators


class TrendSurferStrategy:
    def __init__(self, ema_period=20, adx_period=14, rsi_period=12, atr_period=14, data_window=100):
        self.ema_period = ema_period
        self.adx_period = adx_period
        self.rsi_period = rsi_period
        self.atr_period = atr_period
        self.data_window = data_window
        self.capital = 60
        self.risk_per_trade_pct = 0.065
        self.data = deque(maxlen=data_window)
        self.trades = []
        self.active_trade = None
    
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
            if not signal_df.empty:
                signal_df['Timestamp'] = i
                all_signals.append(signal_df)

        return pd.concat(all_signals).reset_index(drop=True) if all_signals else pd.DataFrame()

    def update(self, price, high, low, volume):
        self.data.append({
            'Price': price,
            'High': high,
            'Low': low,
            'Open': price,
            'Close': price,
            'Volume': volume
        })

    def calculate_indicators(self):
        df = pd.DataFrame(self.data)
        if len(df) < max(self.ema_period, self.adx_period, self.rsi_period, self.atr_period):
            return None

        df['EMA'] = df['Price'].ewm(span=self.ema_period, adjust=False).mean()
        df['RSI'] = Indicators.rsi(df, self.rsi_period)
        df['ATR'] = Indicators.atr(df, self.atr_period)
        df['ADX'], df['+DI'], df['-DI'] = Indicators.adx(df, self.adx_period)
        df['Volume_EMA'] = df['Volume'].ewm(span=20).mean()
        df['Upper_BB'], df['Lower_BB'] = Indicators.bollinger_bands(df)

        return df

    def decide_entry(self, df, regime):
        latest_row = df.iloc[-1]
        if regime == 'trend':
            return self.trend_entry_logic(latest_row)
        elif regime == 'range':
            return self.range_entry_logic(latest_row)
        elif regime == 'squeeze':
            return self.squeeze_entry_logic(df)
        return False

    def trend_entry_logic(self, row):
        return (
            row['Price'] > row['EMA'] * 1.02 and
            row['RSI'] > 62.5 and
            row['ADX'] > 25 and
            row['+DI'] > row['-DI'] and
            row['Volume'] > row['Volume_EMA']
        )

    def range_entry_logic(self, row):
        return (
            row['ADX'] < 20 and (
                (row['RSI'] < 30 and row['Price'] < row['Lower_BB']) or
                (row['RSI'] > 70 and row['Price'] > row['Upper_BB'])
            )
        )

    def squeeze_entry_logic(self, df):
        if len(df) < 21 or df['ATR'].isna().any():
            return False
        atr_mean = df['ATR'].rolling(20).mean().iloc[-1]
        latest_atr = df['ATR'].iloc[-1]
        volume_mean = df['Volume'].rolling(20).mean().iloc[-1]
        latest_volume = df['Volume'].iloc[-1]
        latest_price = df['Price'].iloc[-1]
        upper_band = df['Upper_BB'].iloc[-1]
        lower_band = df['Lower_BB'].iloc[-1]

        is_squeeze = latest_atr < atr_mean * 0.8
        volume_spike = latest_volume > volume_mean * 1.2
        breakout = latest_price > upper_band or latest_price < lower_band

        return is_squeeze and volume_spike and breakout

    def trailing_stop_loss(self, high_since_entry, trail_pct=1.5):
        return high_since_entry * (1 - trail_pct / 100)

    def volatility_exit(self, df):
        latest = df.iloc[-1]
        return latest['Price'] < latest['EMA'] - latest['ATR'] * 3.5

    def rsi_ema_exit(self, df):
        latest = df.iloc[-1]
        return latest['RSI'] < 50 and latest['Price'] < latest['EMA']

    def regime_shift_exit(self, df):
        return MarketRegimeClassifier.classify_market_regime(df) != self.active_trade['Regime']

    def check_exit_signal(self, current_price, df):
        if not self.active_trade:
            return False

        stop_loss = self.active_trade['StopLoss']
        high_since_entry = max([bar['High'] for bar in self.data if bar['Price'] >= self.active_trade['Entry']])
        trail_stop = self.trailing_stop_loss(high_since_entry)

        return (
            current_price <= trail_stop or
            self.volatility_exit(df) or
            self.rsi_ema_exit(df) or
            self.regime_shift_exit(df)
        )

    def calculate_volatility_based_risk(self, df):
        volatility = df['ATR'].iloc[-1] if not df['ATR'].isna().all() else 0
        atr_avg = df['ATR'].rolling(self.atr_period).mean().iloc[-1]
        volatility_factor = volatility / atr_avg if atr_avg != 0 else 1.0
        risk_pct = self.risk_per_trade_pct * (1 / volatility_factor)
        return risk_pct

    def generate_signals(self):
        df = self.calculate_indicators()
        if df is None:
            log_signal("TrendSurferStrategy", "Not enough data for signal", None)
            return pd.DataFrame()

        regime = MarketRegimeClassifier.classify_market_regime(df)
        latest_row = df.iloc[-1]
        signal = 'HOLD'

        # Get dynamic risk per trade based on volatility
        risk_pct = self.calculate_volatility_based_risk(df)

        if self.active_trade and self.check_exit_signal(latest_row['Price'], df):
            exit_price = latest_row['Price']
            profit_or_loss = (exit_price - self.active_trade['Entry']) * self.active_trade['PositionSize']
            self.capital += profit_or_loss  # Update capital with profit/loss
            self.active_trade = None
            signal = 'SELL'

        elif not self.active_trade:
            entry_signal = self.decide_entry(df, regime)
            if entry_signal:
                risk_amount = self.capital * risk_pct  # Use dynamic risk percentage
                stop_loss_price = self.trailing_stop_loss(latest_row['Price'])
                sl_distance = latest_row['Price'] - stop_loss_price

                if sl_distance > 0:
                    position_size = risk_amount / sl_distance
                    self.capital -= risk_amount  # Deduct risk amount from capital
                    self.active_trade = {
                        'Entry': latest_row['Price'],
                        'StopLoss': stop_loss_price,
                        'PositionSize': position_size,
                        'Regime': regime
                    }
                    signal = 'BUY'
        print(f"Current Capital: {self.capital:.2f} | Active Trade: {self.active_trade}")
        log_signal("TrendSurferStrategy", f"{regime.upper()} | Signal: {signal}", latest_row['Price'])
        return pd.DataFrame({
            'Price': [latest_row['Price']],
            'Signal': [signal],
            'Regime': [regime]
        })

        