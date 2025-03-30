# main.py
from data.data_loader import download_data
from models.ml_model import create_features, train_model
from backtest.backtester import run_backtest

def main():
    data = download_data("AAPL", "2018-01-01", "2023-01-01")
    data = create_features(data)
    model = train_model(data)
    run_backtest(data)

if __name__ == "__main__":
    main()
