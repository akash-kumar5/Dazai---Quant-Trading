import os
import sys
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# --- CONFIG ---
DATA_PATH = 'data/BTCUSDT_May_1d.csv'
LOG_DIR = 'log/'

# --- PATH FIX FOR IMPORTS ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

COLORS = {
    'background': '#0E1117',
    'text': '#FAFAFA',
    'bull': '#3D9970',
    'bear': '#FF4136',
    'buy': '#2ECC40',
    'sell': '#FF851B',
    'grid': '#2A2E39'
}

# --- LOADERS ---
def load_ohlc_data(path):
    df = pd.read_csv(path, parse_dates=['Time'])
    df.set_index('Time', inplace=True)
    return df[['Open', 'High', 'Low', 'Close']]

def load_signal_log(path):
    df = pd.read_csv(path, parse_dates=['Timestamp'])
    df.rename(columns={'Timestamp': 'Time', 'Signal Type': 'Signal'}, inplace=True)
    df.set_index('Time', inplace=True)
    return df[['Signal', 'Price']]

def merge_signals(ohlc_df, signals_df):
    return ohlc_df.merge(signals_df, how='left', left_index=True, right_index=True)

def calculate_cumulative_pnl(signals_df):
    trades = signals_df.dropna().copy()
    trades = trades[trades['Signal'].isin(['BUY', 'SELL'])]

    records = []
    cumulative = 0
    position = None
    entry_price = 0
    entry_time = None

    for time, row in trades.iterrows():
        signal = row['Signal']
        price = row['Price']

        if signal == 'BUY' and position is None:
            position = 'LONG'
            entry_price = price
            entry_time = time
            records.append({
                'Time': entry_time,
                'Cumulative PNL': cumulative,
                'Signal': 'BUY'
            })

        elif signal == 'SELL' and position == 'LONG':
            pnl = price - entry_price
            cumulative += pnl
            records.append({
                'Time': time,
                'Cumulative PNL': cumulative,
                'Signal': 'SELL'
            })
            position = None

    pnl_df = pd.DataFrame(records)
    pnl_df.set_index('Time', inplace=True)
    pnl_df['Peak'] = pnl_df['Cumulative PNL'].cummax()
    pnl_df['Drawdown'] = pnl_df['Cumulative PNL'] - pnl_df['Peak']
    return pnl_df


# --- PLOTTERS ---
def plot_candlestick(merged_df, tick_size=1):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=merged_df.index,
        open=merged_df['Open'],
        high=merged_df['High'],
        low=merged_df['Low'],
        close=merged_df['Close'],
        increasing_line_color=COLORS['bull'],
        decreasing_line_color=COLORS['bear'],
        name='OHLC',
    ))

    if 'Signal' in merged_df.columns:
        buys = merged_df[merged_df['Signal'] == 'BUY']
        sells = merged_df[merged_df['Signal'] == 'SELL']

        fig.add_trace(go.Scatter(
            x=buys.index,
            y=buys['Price'],
            mode='markers',
            name='BUY',
            marker=dict(symbol='triangle-up', color=COLORS['buy'], size=12)
        ))

        fig.add_trace(go.Scatter(
            x=sells.index,
            y=sells['Price'],
            mode='markers',
            name='SELL',
            marker=dict(symbol='triangle-down', color=COLORS['sell'], size=12)
        ))

    # Set 3-hour visible range by default
    if not merged_df.empty:
        end_time = merged_df.index[-1]
        start_time = end_time - pd.Timedelta(hours=3)

        visible_df = merged_df[(merged_df.index >= start_time) & (merged_df.index <= end_time)]
        min_price = visible_df['Low'].min()
        max_price = visible_df['High'].max()
        padding = (max_price - min_price) * 0.05

        fig.update_xaxes(range=[start_time, end_time + pd.Timedelta(minutes=1)], showgrid=False)
        fig.update_yaxes(range=[min_price - padding, max_price + padding])

    fig.update_layout(
        title='Dazai Trade Chart',
        template='plotly_dark',
        xaxis_title='Time',
        yaxis_title='Price',
        autosize=True,
        height=700,
        xaxis=dict(
            rangeslider=dict(visible=False),
            rangeselector=dict(
                buttons=[
                    dict(count=1, label='1H', step='hour', stepmode='backward'),
                    dict(count=3, label='3H', step='hour', stepmode='backward'),
                    dict(count=1, label='1D', step='day', stepmode='backward'),
                    dict(count=7, label='1W', step='day', stepmode='backward'),
                    dict(count=1, label='1M', step='month', stepmode='backward'),
                    dict(step='all')
                ]
            ),
            type='date',
            tickformat="%H:%M",
            ticklabelmode="instant",
            tickangle=0
        )
    )
    return fig

def plot_equity_curve(pnl_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pnl_df.index,
        y=pnl_df['Cumulative PNL'],
        mode='lines+markers',
        line=dict(color=COLORS['bull'], width=2),
        name='Equity Curve'
    ))

    fig.add_trace(go.Scatter(
        x=pnl_df.index,
        y=pnl_df['Drawdown'],
        mode='lines',
        line=dict(color=COLORS['bear'], dash='dot'),
        name='Drawdown'
    ))

    fig.add_trace(go.Scatter(
        x=pnl_df[pnl_df['Signal'] == 'SELL'].index,
        y=pnl_df[pnl_df['Signal'] == 'SELL']['Cumulative PNL'],
        mode='markers',
        marker=dict(color=COLORS['sell'], symbol='triangle-down', size=10),
        name='Sell Exit'
    ))

    fig.add_trace(go.Scatter(
        x=pnl_df[pnl_df['Signal'] == 'BUY'].index,
        y=pnl_df[pnl_df['Signal'] == 'BUY']['Cumulative PNL'],
        mode='markers',
        marker=dict(color=COLORS['buy'], symbol='triangle-up', size=10),
        name='Buy Entry'
    ))

    fig.update_layout(
        title='Cumulative PNL (Equity Curve)',
        template='plotly_dark',
        xaxis_title='Time',
        yaxis_title='Cumulative PNL',
        height=400,
        margin=dict(t=40, b=40)
    )
    return fig

# --- STREAMLIT APP ---
st.set_page_config(layout='wide')
st.title('Dazai Trade Visualizer')

ohlc_df = load_ohlc_data(DATA_PATH)
log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.csv')]

if log_files:
    selected_file = st.selectbox('Select a Trade Log', log_files)
    tick_size_option = st.selectbox('Select Tick Size', ['1m', '5m', '15m', '30m', '45m', '1d'])
    if selected_file:
        signals_df = load_signal_log(os.path.join(LOG_DIR, selected_file))
        merged_df = merge_signals(ohlc_df, signals_df)
        fig = plot_candlestick(merged_df, tick_size=tick_size_option)
        st.plotly_chart(fig, use_container_width=True)

        pnl_df = calculate_cumulative_pnl(signals_df)
        pnl_fig = plot_equity_curve(pnl_df)
        print(pnl_df)
        st.plotly_chart(pnl_fig, use_container_width=True)
else:
    st.warning('No trade logs found in the log directory.')
