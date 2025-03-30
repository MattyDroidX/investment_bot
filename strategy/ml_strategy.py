# strategy/ml_strategy.py
import backtrader as bt
import joblib
import pandas as pd
import numpy as np

class MLStrategy(bt.Strategy):
    def __init__(self):
        self.model = joblib.load('models/rf_model.pkl')
        self.scaler = joblib.load('models/scaler.pkl')
        self.dataclose = self.datas[0].close
        self.order = None

    def next(self):
        if len(self.data) < 50:
            return

        sma_10 = np.mean(self.dataclose.get(size=10))
        sma_50 = np.mean(self.dataclose.get(size=50))
        returns = pd.Series(self.dataclose.get(size=11)).pct_change()
        vol = returns[-10:].std()

        features = np.array([[sma_10, sma_50, vol]])
        scaled = self.scaler.transform(features)
        prediction = self.model.predict(scaled)[0]

        if prediction == 1 and not self.position:
            self.buy()
        elif prediction == 0 and self.position:
            self.close()
