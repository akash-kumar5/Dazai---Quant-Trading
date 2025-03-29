import pandas as pd
import logging
from datetime import datetime
from strategies.generate_signals import generate_signals

# Setup logging
logging.basicConfig(
    filename='./data/trade_log.csv',
    level=logging.INFO,
    format='%(asctime)s,%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_trade(signal, option_type, strike_price, premium, status):
    """Logs trade details to a CSV file."""
    log_entry = f"{signal},{option_type},{strike_price},{premium},{status}"
    logging.info(log_entry)

def main():
    """Main function to run the strategy."""
    try:
        # Load data properly
        df = pd.read_csv("data/cleaned_option_data.csv")
        print(df.head())

        if df is None:
            print("⚠️ Data cleaning failed. Check the dataset formatting.")
            return

        print("✅ Data loaded and cleaned successfully.")

        # Generate signals
        signals = generate_signals(df)

        if not signals:
            print("⚠️ No signals generated. Check data formatting or criteria.")
            return

        for signal in signals:
            log_trade(*signal, "PENDING")
            print(f" Signal Generated: {signal}")

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        print("❌ Error occurred. Check logs.")

if __name__ == "__main__":
    main()
