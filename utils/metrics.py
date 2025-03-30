# utils/metrics.py
import numpy as np

def sharpe_ratio(returns, risk_free=0.0):
    excess_returns = returns - risk_free
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

def compute_metrics(portfolio_values):
    returns = np.diff(portfolio_values) / portfolio_values[:-1]
    sharpe = (np.mean(returns) / np.std(returns)) * np.sqrt(252) if np.std(returns) > 0 else 0
    drawdowns = 1 - portfolio_values / np.maximum.accumulate(portfolio_values)
    max_drawdown = np.max(drawdowns)

    return {
        "Total Return": round((portfolio_values[-1] / portfolio_values[0] - 1) * 100, 2),
        "Sharpe Ratio": round(sharpe, 2),
        "Max Drawdown": round(max_drawdown * 100, 2)
    }
