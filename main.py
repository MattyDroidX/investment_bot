# main.py
from data.data_loader import download_data
from models.ml_model import create_features, train_model
from backtest.backtester import run_backtest
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def main():
    data = download_data("AAPL", "2018-01-01", "2023-01-01")
    # print("COLUMNS:", data.columns)
    print(type(data))
    print(data)
    data = create_features(data)
    print(type(data))
    print(data)
    model = train_model(data)
    print(model)
    print(type(data))
    print(data)
    run_backtest(data)
    print(type(data))
    print(data)

if __name__ == "__main__":
    main()
