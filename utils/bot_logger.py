# utils/bot_logger.py
import os
import json
import pandas as pd
from datetime import datetime

SIGNALS_FILE = "data/last_signals.csv"
PORTFOLIO_FILE = "data/portfolio_status.json"

def log_signal(signal_type, current_price, predicted_price, strategy_name):
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strategy": strategy_name,
        "signal": signal_type,
        "price": current_price,
        "predicted": predicted_price
    }

    df = pd.DataFrame([row])

    if not os.path.exists(SIGNALS_FILE):
        df.to_csv(SIGNALS_FILE, index=False)
    else:
        df.to_csv(SIGNALS_FILE, mode='a', index=False, header=False)

def update_portfolio(cash, position, portfolio_value):
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cash": cash,
        "position": position,
        "portfolio_value": portfolio_value
    }

    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(data, f, indent=4)
