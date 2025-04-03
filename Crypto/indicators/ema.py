import numpy as np

def calculate_ema(prices, period):
    if not prices or len(prices) < period:
        return [np.nan] * len(prices)  # Return NaN list if insufficient data

    ema_values = []
    multiplier = 2 / (period + 1)
    ema_values.append(prices[0])  # Seed with first price
    
    for price in prices[1:]:
        ema_values.append((price - ema_values[-1]) * multiplier + ema_values[-1])

    return ema_values
