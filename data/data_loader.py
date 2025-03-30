# data/data_loader.py
import yfinance as yf
import pandas as pd

def download_data(ticker="AAPL", start="2020-01-01", end="2023-01-01"):
    raw = yf.download(ticker, start=start, end=end)

    # Detecta y aplana si hay MultiIndex
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    raw.dropna(inplace=True)
    return raw

