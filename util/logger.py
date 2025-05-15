import csv
import os
from datetime import datetime

def log_signal(strategy_name, signal_type, price, additional_info=None):
    # Ensure log directory exists
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)

    # Generate log file name with date and strategy name
    date_str = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{log_dir}/{date_str}_{strategy_name}.csv"

    # Prepare log entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = [timestamp, signal_type, price, additional_info]

    # Append to CSV
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Add header if file is new
        if os.stat(file_name).st_size == 0:
            writer.writerow(["Timestamp", "Signal Type", "Price", "Additional Info"])
        writer.writerow(log_entry)

    # print(f"Logged signal: {log_entry}")
