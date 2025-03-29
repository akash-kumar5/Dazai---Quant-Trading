import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Fetch Market Data
stock_symbol = "IRCON.NS"  # Change this to any stock (Example: RELIANCE.NS, INFY.NS)
data = yf.download(stock_symbol, period="1y", interval="1d")  # 1 year daily data
data.to_csv(f"{stock_symbol}_data.csv")  # Save for offline analysis

# Step 2: Calculate Indicators (Moving Averages)
data["SMA_50"] = data["Close"].rolling(window=50).mean()
data["SMA_200"] = data["Close"].rolling(window=200).mean()

# Step 3: Generate Buy/Sell Signals
data["Signal"] = 0
data.loc[data["SMA_50"] > data["SMA_200"], "Signal"] = 1  # Buy Signal
data.loc[data["SMA_50"] < data["SMA_200"], "Signal"] = -1  # Sell Signal

# Step 4: Plot Price & Indicators
plt.figure(figsize=(12, 6))
plt.plot(data["Close"], label="Stock Price", color="blue")
plt.plot(data["SMA_50"], label="50-day SMA", color="green")
plt.plot(data["SMA_200"], label="200-day SMA", color="red")
plt.title(f"{stock_symbol} Price with Moving Averages")
plt.legend()
plt.show()

# Step 5: Backtesting - Calculate Strategy Performance
data["Returns"] = data["Close"].pct_change()  # Daily returns
data["Strategy"] = data["Returns"] * data["Signal"].shift(1)  # Apply signals

# Step 6: Evaluate Performance
total_return = np.exp(data["Strategy"].sum()) - 1  # Cumulative return
win_rate = (data["Strategy"] > 0).sum() / (data["Strategy"] != 0).sum()  # Win ratio

# Step 7: Print Results
print(data.tail(10))  # Show last 10 rows with signals
print(f"Total Strategy Return: {total_return:.2%}")
print(f"Win Rate: {win_rate:.2%}")
