import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from util.loader import BinanceDataFetcher

page = st.sidebar.radio("Select Page", ['Home','Loader','Backtester'])

if page=='Loader':
    import pages.Loader
elif page == 'Home':
    import pages.Home
elif page == 'Backtester':
    import pages.Backtester


