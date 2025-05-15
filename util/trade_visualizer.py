import pandas as pd
import plotly.graph_objects as go

import plotly.graph_objects as go

def plot_price_with_trades(df):
    fig = go.Figure()

    # Plot Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Price'],
        high=df['Price'],
        low=df['Price'],
        close=df['Price'],
        name='Price'
    ))

    # Plot Buys and Sells
    if 'Signal' in df.columns:
        buys = df[df['Signal'] == 'BUY']
        sells = df[df['Signal'] == 'SELL']

        fig.add_trace(go.Scatter(
            x=buys.index,
            y=buys['Price'],
            mode='markers',
            marker=dict(symbol='arrow-up', color='green', size=12),
            name='Buy'
        ))

        fig.add_trace(go.Scatter(
            x=sells.index,
            y=sells['Price'],
            mode='markers',
            marker=dict(symbol='arrow-down', color='red', size=12),
            name='Sell'
        ))

    fig.update_layout(
        title='Trade Chart',
        xaxis_title='Time',
        yaxis_title='Price',
        template='plotly_dark',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    return fig


def plot_equity_curve(df, starting_capital=100000):
    capital = starting_capital
    position = 0
    equity_list = []
    entry_price = None

    for idx, row in df.iterrows():
        if row['Signal'] == 'BUY' and position == 0:
            position = 1
            entry_price = row['Price']
            equity = capital
        elif row['Signal'] == 'SELL' and position == 1:
            capital += (row['Price'] - entry_price)
            position = 0
            equity = capital
        else:
            if position == 1:
                equity = capital + (row['Price'] - entry_price)
            else:
                equity = capital

        equity_list.append(equity)

    df['Equity'] = equity_list

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Equity'], mode='lines', name='Equity Curve'))
    fig.update_layout(title='Equity Curve', xaxis_title='Time', yaxis_title='Portfolio Value')
    return fig
