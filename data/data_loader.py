# data/data_loader.py
import yfinance as yf
import pandas as pd

def download_data(ticker="AAPL", start="2020-01-01", end="2023-01-01"):
    data = yf.download(ticker, start=start, end=end)
    data = data.dropna()
    return data
