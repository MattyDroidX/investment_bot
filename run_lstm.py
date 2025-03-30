# run_lstm.py
from data.data_loader import download_data
from models.lstm_model import train_lstm_model
from strategy.lstm_strategy import LSTMStrategy
import backtrader as bt

def run_lstm_backtest():
    data = download_data("AAPL", "2018-01-01", "2023-01-01")
    train_lstm_model(data)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(LSTMStrategy)
    feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(feed)
    cerebro.broker.setcash(100000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()

if __name__ == "__main__":
    run_lstm_backtest()
