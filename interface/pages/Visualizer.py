import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from util.trade_visualizer import plot_price_with_trades, plot_equity_curve

st.set_page_config(layout="wide", page_title="Trade Visualizer")

st.title("📊 Trade Visualizer")

data_folder = 'log'
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
selected_file = st.selectbox('Select Log File', csv_files)

if selected_file:
    df = pd.read_csv(os.path.join(data_folder, selected_file))
    df.rename(columns={'Signal Type': 'Signal'}, inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)

    # Create dummy OHLC from 'Price'
    df['Open'] = df['Price']
    df['High'] = df['Price']
    df['Low'] = df['Price']
    df['Close'] = df['Price']

    # Resample candles
    timeframe = st.selectbox('Select Timeframe', ['1T', '5T', '15T', '30T', '1H', '4H'], index=2)

    # Trades (original precision)
    df_trades = df[df['Signal'].isin(['BUY', 'SELL'])]

    # Plot
    st.plotly_chart(plot_price_with_trades(df), use_container_width=True)
    st.plotly_chart(plot_equity_curve(df_trades), use_container_width=True)

else:
    st.info("Upload your trade log to see the charts.")
