import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
import pandas as pd
from strategies.MA import SimpleMovingAverageStrategy
from backtest.result_analyzer import ResultAnalyzer

class Backtester:
    def __init__(self, strategy_class, initial_capital=100):
        """Initialize the backtester with the provided strategy and initial capital."""
        self.strategy = strategy_class()  # Instantiate the strategy
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.indicators_log = []  # Log of indicator values

    def run(self, df):
        """Run the backtest on the provided DataFrame."""
        signals = []

        # Iterate over each row in the DataFrame (representing a time period)
        for time, row in df.iterrows():
            self.strategy.update(row["Close"], row["High"], row["Low"], row["Volume"])
            
            signal_df = self.strategy.generate_signals()  # <<< This triggers signal logic
            
            if signal_df is not None and not signal_df.empty:
                signal_row = signal_df.iloc[-1]
                print(f"Signal generated at {time}: {signal_row['Signal']} at price {signal_row['Price']}")
                signals.append({
                    "Timestamp": time,
                    "Signal Type": signal_row["Signal"],
                    "Price": signal_row["Price"]
                })

        # Return a DataFrame of the generated signals
        return pd.DataFrame(signals)

# ============================
# RUN THE BACKTEST
# ============================

def run_backtest():
    # Load the data and prepare it for analysis
    df = pd.read_csv("data/BTCUSDT_May_1d.csv")
    df["Time"] = pd.to_datetime(df["Time"])  # Ensure time column is in datetime format
    df.set_index("Time", inplace=True)
    df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

    # Instantiate the backtester with the strategy
    bt = Backtester(SimpleMovingAverageStrategy)

    # Run the backtest
    signals_df = bt.run(df)

    # Define log file path
    log_path = f"log/{datetime.now().strftime('%Y-%m-%d')}_SMA_Strategy.csv"

    # Save the generated signals to a CSV file
    signals_df.to_csv(log_path, index=False)
    print(f"Backtest completed. Signals saved to {log_path}")

    analyzer = ResultAnalyzer()
    analyzer.analyze_file(log_path)

if __name__ == "__main__":
    run_backtest()
