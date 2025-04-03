from indicators.sma import calculate_sma

def calculate_bollinger_bands(prices, period, std_dev):
    sma = calculate_sma(prices, period)
    bands = []
    for i in range(len(sma)):
        slice_prices = prices[i+period-len(sma):i+period]
        std_deviation = (sum([(p - sma[i]) ** 2 for p in slice_prices]) / period) ** 0.5
        upper_band = sma[i] + (std_deviation * std_dev)
        lower_band = sma[i] - (std_deviation * std_dev)
        bands.append((upper_band, sma[i], lower_band))
    return bands
# Compare this snippet from indicators/__init__.py:
