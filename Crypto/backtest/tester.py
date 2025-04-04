import pandas as pd
from EARA import TrendSurferStrategy

# Load historical data
df = pd.read_csv("backtest/data/BTCUSDT_Jan_1Week.csv")
df["Time"] = pd.to_datetime(df["Time"])
df.set_index("Time", inplace=True)

# Ensure numeric columns are float
df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

# Initialize strategy
strategy = TrendSurferStrategy()

# Tracking trades & PnL
signals = []
trade_open = False
entry_price = 0
highest_price = 0  # For trailing stop-loss
pnl_trailing = []
trailing_stop_pct = 0.01  # 1% trailing stop

# Iterate through data
for time, row in df.iterrows():
    strategy.update(row["Close"], row["High"], row["Low"], row["Volume"])
    signal_df = strategy.generate_signals()
    
    if not signal_df.empty:
        action = signal_df.iloc[0]["Signal"]
        price = signal_df.iloc[0]["Price"]
        
        if action == "BUY" and not trade_open:
            trade_open = True
            entry_price = price
            highest_price = price
            signals.append({"Time": time, "Action": "BUY", "Price": entry_price, "PnL_Trailing": None})
        
        elif trade_open:
            highest_price = max(highest_price, price)  # Update highest price
            trailing_stop_loss = highest_price * (1 - trailing_stop_pct)
            
            if price <= trailing_stop_loss:  # Stop-loss triggered
                trade_open = False
                exit_price = price
                pnl = exit_price - entry_price
                pnl_trailing.append(pnl)
                
                signals.append({
                    "Time": time,
                    "Action": "SELL",
                    "Price": exit_price,
                    "PnL_Trailing": pnl
                })

# Convert signals to DataFrame and save
signals_df = pd.DataFrame(signals)
signals_df.to_csv("backtest/log/backtest_results.csv", index=False)
print("Backtest completed. Signals with PnL saved.")
print("Trailing Stop-Loss PnL:", sum(pnl_trailing))