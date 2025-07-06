import pandas as pd
import plotly.graph_objects as go


def plot_price_with_trades(df):
    fig = go.Figure()

    # Line chart for Price
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Price'],
        mode='lines',
        name='Price',
        line=dict(color='cyan')
    ))

    # Plot Buys and Sells if present
    if 'Signal' in df.columns:
        buys = df[df['Signal'] == 'BUY']
        sells = df[df['Signal'] == 'SELL']

        fig.add_trace(go.Scatter(
            x=buys.index,
            y=buys['Price'],
            mode='markers',
            marker=dict(symbol='triangle-up', color='green', size=10),
            name='Buy'
        ))

        fig.add_trace(go.Scatter(
            x=sells.index,
            y=sells['Price'],
            mode='markers',
            marker=dict(symbol='triangle-down', color='red', size=10),
            name='Sell'
        ))

    fig.update_layout(
        title='Price with Trades',
        xaxis_title='Time',
        yaxis_title='Price',
        template='plotly_dark',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    return fig



def plot_equity_curve(trades_df, starting_capital=100000):
    capital = starting_capital
    position = 0
    equity_list = []
    entry_price = None

    for idx, row in trades_df.iterrows():
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

    trades_df['Equity'] = equity_list

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trades_df.index, y=trades_df['Equity'], mode='lines', name='Equity Curve'))
    fig.update_layout(
        title='Equity Curve',
        xaxis_title='Time',
        yaxis_title='Portfolio Value',
        template='plotly_dark',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    return fig
