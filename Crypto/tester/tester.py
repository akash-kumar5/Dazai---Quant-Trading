import pandas as pd

# Load the data
df = pd.read_csv("log/2025-04-04_TrendSurferStrategy.csv", header=0, names=["Timestamp", "Event", "Price", "VWAP"])

df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

df_signals = df[df["Event"].str.contains("Signal Generated", na=False)].copy()
df_signals["Signal"] = df_signals["Event"].str.split(": ").str[-1]

# Track positions
position_tracker = []  # Stores open BUY trades
completed_trades = []  # Stores closed trades

for _, row in df_signals.iterrows():
    if row["Signal"] == "BUY":
        position_tracker.append({"Entry Time": row["Timestamp"], "Entry Price": row["Price"], "Position Size": 1})  # Assuming 1 unit per trade
    elif row["Signal"] == "SELL" and position_tracker:
        entry_trade = position_tracker.pop(0)  # FIFO matching of BUY & SELL
        exit_trade = {"Exit Time": row["Timestamp"], "Exit Price": row["Price"]}
        
        pnl = (exit_trade["Exit Price"] - entry_trade["Entry Price"]) * entry_trade["Position Size"]  # PnL Calculation
        completed_trades.append({**entry_trade, **exit_trade, "PnL": pnl})

# Convert to DataFrame
pnl_df = pd.DataFrame(completed_trades)
if not pnl_df.empty:
    pnl_df["Cumulative PnL"] = pnl_df["PnL"].cumsum()

# Check for unmatched trades
if position_tracker:
    print(f"\nWarning: {len(position_tracker)} open BUY positions remain unmatched!")

# Print results
print("Signal Counts:\n", df_signals["Signal"].value_counts())
print("\nPrice Stats:\n", {
    "Min Price": df["Price"].min(),
    "Max Price": df["Price"].max(),
    "Mean Price": df["Price"].mean()
})
print("\nPnL Data:")
print(pnl_df)

