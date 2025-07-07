import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from util.loader import BinanceDataFetcher

st.write("Data Loader")

# Inputs
start = st.date_input("Start Date")
end = st.date_input("End Date")
file_name = st.text_input("File Name (example: May_1d)")

# Button
if st.button("Download data"):
    if not file_name:
        st.error("Please enter a valid file name.")
    else:
        with st.spinner("Downloading the historic data...."):
            # Convert date to string format
            start_str = start.strftime('%Y-%m-%d')
            end_str = end.strftime('%Y-%m-%d')
            file_name='BTCUSDT_'+file_name+'.csv'
            try:
                BinanceDataFetcher.fetch_ohlcv_to_csv(start_str, end_str, file_name)
                st.success(f"Data downloaded and saved to data/{file_name}")
            except Exception as e:
                st.error(f"Error: {e}")