# backtest/backtester.py
import backtrader as bt
from strategy.ml_strategy import MLStrategy

def run_backtest(data):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MLStrategy)

    datafeed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(datafeed)

    cerebro.broker.setcash(100000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.run()
    cerebro.plot()
