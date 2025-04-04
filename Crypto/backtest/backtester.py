from binance.client import Client
import pandas as pd
import time

# Replace with your Binance API keys (leave empty for public access but lower limits)
API_KEY = "ItFMygh3PlB7ftuFKdX9qx2ewTu2O8azEjZAvhzDZdbX2L2ih8OVws2uS27YScQs"
API_SECRET = "plDC99R0tFZ3wYN0pbC5SkuexnoYSBg0eCIJoBLpiq2tFPswFFlVrf0xZz8BOyKb"

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Define parameters
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1MINUTE
start_date = "2024-03-01"
end_date = "2024-03-14"  # Binance uses exclusive end dates

# Fetch historical data
def fetch_historical_data(symbol, interval, start_str, end_str):
    """Fetches all 1-minute OHLCV data from Binance between start and end dates."""
    klines = []
    start_ts = int(pd.Timestamp(start_str).timestamp() * 1000)
    end_ts = int(pd.Timestamp(end_str).timestamp() * 1000)

    while start_ts < end_ts:
        new_candles = client.get_klines(
            symbol=symbol, interval=interval, startTime=start_ts, limit=1000
        )
        if not new_candles:
            break  # No more data available

        klines.extend(new_candles)
        start_ts = new_candles[-1][0] + 1  # Move start time forward
        time.sleep(0.5)  # Sleep to avoid rate limits

    return klines

# Fetch data
candles = fetch_historical_data(symbol, interval, start_date, end_date)

# Convert to DataFrame
df = pd.DataFrame(candles, columns=[
    "Time", "Open", "High", "Low", "Close", "Volume", "CloseTime", 
    "QuoteAssetVolume", "Trades", "TakerBaseVolume", "TakerQuoteVolume", "Ignore"
])

# Convert timestamp to readable date
df["Time"] = pd.to_datetime(df["Time"], unit="ms")

# Convert numeric columns to float
df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

# Save to CSV
df.to_csv("backtest/data/BTCUSDT_Jan_1Week.csv", index=False)

print("Data saved successfully!")
print(df.head())  # Show first few rows
