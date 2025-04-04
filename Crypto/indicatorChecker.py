import pandas as pd
import numpy as np

from indicators.rsi import calculate_rsi
from indicators.macd import calculate_macd
from indicators.vwap import calculate_vwap
from indicators.ema import calculate_ema
from indicators.bollinger_bands import calculate_bollinger_bands

# Sample Data
sample_data = pd.DataFrame({
    'close': [83000, 83100, 83200, 83300, 83400, 83500, 83400, 83700, 83500, 83900],
    'volume': [43000, 43100, 43200, 43300, 43400, 43500, 43600, 43700, 43800, 43900]
})

print("\n--- Checking Indicators ---\n")

try:
    print("RSI:")
    print(calculate_rsi(sample_data, period=3))
except Exception as e:
    print(f"Error calculating RSI: {e}")

try:
    print("\nMACD:")
    macd, signal, hist = calculate_macd(sample_data, short_window=3, long_window=6, signal_window=3)
    print("MACD Line:", macd)
    print("Signal Line:", signal)
    print("Histogram:", hist)
except Exception as e:
    print(f"Error calculating MACD: {e}")

try:
    print("\nVWAP:")
    print(calculate_vwap(sample_data))
except Exception as e:
    print(f"Error calculating VWAP: {e}")

try:
    print("\nEMA Calculation Test:")
    print(calculate_ema(sample_data, period=3))
except Exception as e:
    print(f"Error during EMA calculation: {e}")
    
try:
    print("\nBollinger Bands:")
    upper, lower = calculate_bollinger_bands(sample_data, period=3, std_dev=2)
    print("Upper Band:", upper)
    print("Lower Band:", lower)
except Exception as e:
    print(f"Error calculating Bollinger Bands: {e}")
