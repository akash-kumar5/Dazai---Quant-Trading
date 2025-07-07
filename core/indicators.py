import numpy as np
import pandas as pd

class Indicators:
     def rsi(df,rsi_period):
        delta = df['Price'].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(rsi_period).mean()
        avg_loss = pd.Series(loss).rolling(rsi_period).mean()
        rs = avg_gain / (avg_loss + 1e-10)
        return 100 - (100 / (1 + rs))

     def atr( df, atr_period):
        df['TR'] = np.maximum(df['High'] - df['Low'],
                              np.maximum(abs(df['High'] - df['Price'].shift(1)),
                                         abs(df['Low'] - df['Price'].shift(1))))
        return df['TR'].rolling(atr_period).mean()

     def adx(df, adx_period):
        high_diff = df['High'].diff()
        low_diff = df['Low'].diff()
        df['+DM'] = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
        df['-DM'] = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)
        tr_smooth = df['ATR']
        df['+DI'] = 100 * df['+DM'].rolling(adx_period).mean() / tr_smooth
        df['-DI'] = 100 * df['-DM'].rolling(adx_period).mean() / tr_smooth
        df['DX'] = (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'] + 1e-10)) * 100
        return df['DX'].rolling(adx_period).mean(), df['+DI'], df['-DI']

     def bollinger_bands(df):
        moving_avg = df['Price'].rolling(20).mean()
        moving_std = df['Price'].rolling(20).std()
        return moving_avg + 2 * moving_std, moving_avg - 2 * moving_std