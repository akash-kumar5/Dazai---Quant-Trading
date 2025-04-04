from indicators.sma import calculate_sma

def calculate_bollinger_bands(data, period, std_dev):
    if len(data) < period:
        print("Error calculating Bollinger Bands: Insufficient data")
        return None, None
    rolling_mean = data['close'].rolling(window=period).mean()
    rolling_std = data['close'].rolling(window=period).std()
    upper_band = rolling_mean + (rolling_std * std_dev)
    lower_band = rolling_mean - (rolling_std * std_dev)
    return upper_band, lower_band

# Compare this snippet from indicators/__init__.py:
