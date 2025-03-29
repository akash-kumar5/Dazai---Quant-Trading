import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategies.option_strategy import generate_signals

def backtest_strategy(csv_file):
    """Backtests the strategy on past option chain data."""
    df = pd.read_csv(csv_file)  # Skip first row if needed
    df.columns = ["CALLS", "PUTS", "OI", "CHNG IN OI", "VOLUME", "IV", "LTP", "CHNG",
              "BID QTY", "BID", "ASK", "ASK QTY", "STRIKE",
              "BID QTY_P", "BID_P", "ASK_P", "ASK QTY_P", "CHNG_P", "LTP_P",
              "IV_P", "VOLUME_P", "CHNG IN OI_P", "OI_P"]


    # Generate buy/sell signals
    signals = generate_signals(df)

    # Simple accuracy check: Count signals & check frequency
    total_signals = len(signals)
    if total_signals == 0:
        print("⚠️ No signals found in historical data.")
        return
    
    print(f"📊 Backtesting Results on {csv_file}")
    print(f"🔹 Total Signals: {total_signals}")
    for signal in signals:
        print(signal)

if __name__ == "__main__":
    backtest_strategy("data/historical_data.csv")
