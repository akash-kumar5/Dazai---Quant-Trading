import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from datetime import datetime
import pandas as pd

from backtest.backtester import Backtester
from backtest.result_analyzer import ResultAnalyzer

# Import your strategies
from strategies.MA import SimpleMovingAverageStrategy
from strategies.EARA import TrendSurferStrategy  # Assuming your EARA is this

# -------------------------------
# Strategy Mapping
# -------------------------------
strategy_mapping = {
    'Moving Average': SimpleMovingAverageStrategy,
    'EARA': TrendSurferStrategy
}

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("Backtester")

# Strategy selection
strategy = st.selectbox("Select Strategy", list(strategy_mapping.keys()))

# Dataset selection (dynamic)
data_folder = 'data'
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
dataset = st.selectbox('Select Dataset', csv_files)

# -------------------------------
# Backtest logic
# -------------------------------
if st.button('Run Backtest'):
    selected_strategy_class = strategy_mapping.get(strategy)

    if not selected_strategy_class:
        st.error(f"Strategy '{strategy}' not implemented.")
    else:
        with st.spinner("Running Backtester.. Please wait"):
            df = pd.read_csv(os.path.join(data_folder, dataset))
            df["Time"] = pd.to_datetime(df["Time"])
            df.set_index("Time", inplace=True)
            df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

            # Run backtest
            bt = Backtester(selected_strategy_class)
            signals_df = bt.run(df)

            # Save log
            log_path = f"log/{datetime.now().strftime('%Y-%m-%d')}_{strategy.replace(' ', '_')}_Strategy.csv"
            signals_df.to_csv(log_path, index=False)

        st.success(f"Backtest completed. Signals saved to {log_path}")

        # Analyze result
        analyzer = ResultAnalyzer()
        metrics = analyzer.analyze_file(log_path)
        

        if metrics:
            st.subheader("Performance Metrics")
            st.table(pd.DataFrame(metrics.items(), columns=["Metric", "Value"]))
        else:
            st.warning("No valid trades found.")
