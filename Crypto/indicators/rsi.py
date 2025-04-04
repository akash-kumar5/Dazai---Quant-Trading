import pandas as pd

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period, min_periods=1).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period, min_periods=1).mean()
    
    # Avoid division by zero
    rs = gain / (loss.replace(0, 1e-10))
    rsi = 100 - (100 / (1 + rs))
    return rsi
