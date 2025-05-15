import streamlit as st

st.title("Dazai - Dashboard")

st.write("Loader Page : Used to load historical data of Cryptocurreny (currently only for BTC)" \
" and store it in csv format in data folder")

st.write("Backtester Page : Allows to choose strategy and dataset available." \
" Will log the signals in csv file. And a result analyzer will go through the signals log to give equity curve and results of other metrics  like sharpe ratio, max drawdown, etc.")

st.write("Stats page(if possible): Will show the best strategy and performance with metrics result and charts.")

