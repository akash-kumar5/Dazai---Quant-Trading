import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from util.trade_visualizer import plot_price_with_trades, plot_equity_curve, calculate_trade_stats
import pandas as pd
from backtest.result_analyzer import ResultAnalyzer

st.title("📊 Trade Visualizer")


data_folder = 'log'
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
selected_file = st.selectbox('Select Log File', csv_files)

if selected_file:
    df = pd.read_csv(os.path.join(data_folder, selected_file))
    df.rename(columns={'Signal Type': 'Signal'}, inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    
    st.plotly_chart(plot_price_with_trades(df), use_container_width=True)
    st.plotly_chart(plot_equity_curve(df), use_container_width=True)

else:
    st.info("Upload your trade log to see the charts.")
