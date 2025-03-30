# run_ensemble.py
from data.data_loader import download_data
from models.lstm_model import train_lstm_model
from models.ml_model import create_features, train_model
from strategy.ensemble_strategy import EnsembleStrategy
import backtrader as bt
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def run_ensemble_backtest():
    data = download_data("AAPL", "2018-01-01", "2023-01-01")

    # Entrenamiento previo (si no lo hiciste antes)
    enriched = create_features(data.copy())
    train_model(enriched)
    train_lstm_model(data)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(EnsembleStrategy)
    feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(feed)
    cerebro.broker.setcash(100000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()

if __name__ == "__main__":
    run_ensemble_backtest()
