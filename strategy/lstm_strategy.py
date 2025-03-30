# strategy/lstm_strategy.py
import backtrader as bt
import numpy as np
import joblib
from tensorflow.keras.models import load_model

class LSTMStrategy(bt.Strategy):
    def __init__(self):
        self.model = load_model('models/lstm_model.h5')
        self.scaler = joblib.load('models/lstm_scaler.pkl')
        self.dataclose = self.datas[0].close
        self.lookback = 30

    def next(self):
        if len(self.dataclose) < self.lookback + 1:
            return

        window = np.array(self.dataclose.get(size=self.lookback)).reshape(-1, 1)
        scaled_window = self.scaler.transform(window)
        X = np.reshape(scaled_window, (1, self.lookback, 1))

        predicted_scaled = self.model.predict(X, verbose=0)
        predicted_price = self.scaler.inverse_transform(predicted_scaled)[0][0]

        current_price = self.dataclose[0]

        if predicted_price > current_price * 1.01 and not self.position:
            self.buy()
        elif predicted_price < current_price * 0.99 and self.position:
            self.close()
