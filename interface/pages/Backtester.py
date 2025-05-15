import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import streamlit as st
from datetime import datetime
from backtest.backtester import Backtester
from strategies.MA import SimpleMovingAverageStrategy
from backtest.result_analyzer import ResultAnalyzer
import pandas as pd

st.title("Backtester")

# Strategy dropdown
strategy = st.selectbox("Select Strategy", ['EARA', 'Moving Average'])

# Dataset dropdown (dynamic from data folder)
data_folder = 'data'
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
dataset = st.selectbox('Select Dataset', csv_files)

# Run backtest button
if st.button('Run Backtest'):
    if strategy == 'Moving Average':
        df = pd.read_csv(f"data/{dataset}")
        df["Time"] = pd.to_datetime(df["Time"])
        df.set_index("Time", inplace=True)
        df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

        bt = Backtester(SimpleMovingAverageStrategy)
        signals_df = bt.run(df)

        log_path = f"log/{datetime.now().strftime('%Y-%m-%d')}_SMA_Strategy.csv"
        signals_df.to_csv(log_path, index=False)
        print(log_path)

        st.success(f"Backtest completed. Signals saved to {log_path}")

        analyzer = ResultAnalyzer()
        metrics = analyzer.analyze_file(log_path)

        if metrics:
            st.subheader("Performance Metrics")
            st.table(pd.DataFrame(metrics.items(), columns=["Metric", "Value"]))
        else:
            st.warning("No valid trades found.")
