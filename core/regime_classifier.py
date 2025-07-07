#Detect trend / range / squeeze
import numpy as np

class MarketRegimeClassifier:
    def classify_market_regime(df, window=15):
            recent = df.iloc[-window:]
            atr = recent['High'].max() - recent['Low'].min()
            avg_body = np.mean(np.abs(recent['Close'] - recent['Open']))
            wick_ratio = np.mean((recent['High'] - recent['Low']) / (np.abs(recent['Close'] - recent['Open']) + 1e-5))

            if atr > avg_body * 2 and wick_ratio < 2:
                return 'trend'
            elif wick_ratio > 3 and avg_body < atr * 0.5:
                return 'range'
            else:
                return 'squeeze'