import csv
import os
from datetime import datetime

def initialize_logger(log_file="trade_logs.csv"):
    if not os.path.exists(log_file):
        with open(log_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Symbol", "Strike Price", "Option Type", "Signal", "Entry Price"])

def log_trade(symbol, strike_price, option_type, signal, entry_price, log_file="trade_logs.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, symbol, strike_price, option_type, signal, entry_price])

# Initialize the logger
initialize_logger()

# Example Usage
# log_trade("NIFTY", 18000, "CALL", "BUY", 120.5)
