import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st


st.title("Dazai - Dashboard")

st.write("Loader Page : Used to load historical data of Cryptocurreny (currently only for BTC)" \
" and store it in csv format in data folder")

st.write("Backtester Page : Allows to choose strategy and dataset available." \
" Will log the signals in csv file. And a result analyzer will go through the signals log to give equity curve and results of other metrics  like sharpe ratio, max drawdown, etc.")

st.write("Visualizer Page : Will show the price with trades and equity curve of the strategy." \
" Will show the trades with entry and exit points on the price chart." \
    
    )
st.write("Stats page(in progress): Will show the best strategy and performance with metrics result and charts.")