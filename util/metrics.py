import numpy as np

def total_return(trades):
    """Sum of all PnL from trades."""
    return sum(t['pnl'] for t in trades)


def average_return(trades):
    """Average PnL per trade."""
    if not trades:
        return 0
    return sum(t['pnl'] for t in trades) / len(trades)


def win_rate(trades):
    """Ratio of profitable trades to total trades."""
    if not trades:
        return 0
    wins = sum(1 for t in trades if t['pnl'] > 0)
    return wins / len(trades)


def loss_rate(trades):
    """Ratio of losing trades to total trades."""
    if not trades:
        return 0
    losses = sum(1 for t in trades if t['pnl'] < 0)
    return losses / len(trades)


def max_drawdown(trades):
    """Maximum drawdown from equity curve."""
    equity = 0
    peak = 0
    drawdowns = []

    for t in trades:
        equity += t['pnl']
        peak = max(peak, equity)
        drawdown = peak - equity
        drawdowns.append(drawdown)

    return max(drawdowns) if drawdowns else 0


def profit_factor(trades):
    """Gross profit / gross loss"""
    gross_profit = sum(t['pnl'] for t in trades if t['pnl'] > 0)
    gross_loss = abs(sum(t['pnl'] for t in trades if t['pnl'] < 0))
    if gross_loss == 0:
        return float('inf')  # Avoid division by zero
    return gross_profit / gross_loss


def sharpe_ratio(trades, risk_free_rate=0.0):
    returns = [trade["pnl"] for trade in trades]
    if len(returns) < 2:  # Avoid unreliable ratios for small datasets
        return None
    avg_return = np.mean(returns)
    std_dev = np.std(returns)
    return (avg_return - risk_free_rate) / (std_dev + 1e-10)


def sortino_ratio(trades, risk_free_rate=0.0):
    returns = [trade["pnl"] for trade in trades]
    negative_returns = [r for r in returns if r < 0]
    downside_std = np.std(negative_returns) if negative_returns else 0
    avg_return = np.mean(returns)
    return (avg_return - risk_free_rate) / (downside_std + 1e-10)


def expectancy(trades):
    if not trades:
        return 0
    win_trades = [t for t in trades if t["pnl"] > 0]
    loss_trades = [t for t in trades if t["pnl"] <= 0]
    win_rate = len(win_trades) / len(trades)
    avg_win = np.mean([t["pnl"] for t in win_trades]) if win_trades else 0
    avg_loss = abs(np.mean([t["pnl"] for t in loss_trades])) if loss_trades else 0
    return (win_rate * avg_win) - ((1 - win_rate) * avg_loss)


def avg_win(trades):
    wins = [t["pnl"] for t in trades if t["pnl"] > 0]
    if not wins:
        return 0
    return np.mean(wins)


def avg_loss(trades):
    losses = [t["pnl"] for t in trades if t["pnl"] <= 0]
    if not losses:
        return 0
    return np.mean(losses)


def payoff_ratio(trades):
    aw = avg_win(trades)
    al = abs(avg_loss(trades))
    return aw / (al + 1e-10)


def highest_win(trades):
    """Highest winning trade."""
    wins = [t["pnl"] for t in trades if t["pnl"] > 0]
    return max(wins) if wins else 0


def initial_capital(trades):
    """Initial capital at the start of the first trade."""
    if not trades:
        return 0
    return trades[0].get("entry_price", 0)
