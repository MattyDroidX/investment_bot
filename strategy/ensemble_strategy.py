# strategy/ensemble_strategy.py
import backtrader as bt
import numpy as np
import pandas as pd
import json
from datetime import datetime
import joblib
from utils.bot_logger import log_signal, update_portfolio
from tensorflow.keras.models import load_model

class EnsembleStrategy(bt.Strategy):
    def __init__(self):
        # Random Forest
        self.rf_model = joblib.load('models/rf_model.pkl')
        self.scaler_rf = joblib.load('models/scaler.pkl')

        # LSTM
        self.lstm_model = load_model('models/lstm_model.h5')
        self.scaler_lstm = joblib.load('models/lstm_scaler.pkl')
        self.lookback = 30

        self.dataclose = self.datas[0].close

    def next(self):
        if len(self.dataclose) < 50:
            return

        ### Señal 1: Random Forest
        sma_10 = np.mean(self.dataclose.get(size=10))
        sma_50 = np.mean(self.dataclose.get(size=50))
        returns = pd.Series(self.dataclose.get(size=11)).pct_change()
        vol = returns[-10:].std()

        features_rf = np.array([[sma_10, sma_50, vol]])
        scaled_rf = self.scaler_rf.transform(features_rf)
        rf_signal = self.rf_model.predict(scaled_rf)[0]

        ### Señal 2: LSTM
        window = np.array(self.dataclose.get(size=self.lookback)).reshape(-1, 1)
        scaled_window = self.scaler_lstm.transform(window)
        X_lstm = np.reshape(scaled_window, (1, self.lookback, 1))
        predicted_scaled = self.lstm_model.predict(X_lstm, verbose=0)
        predicted_price = self.scaler_lstm.inverse_transform(predicted_scaled)[0][0]

        current_price = self.dataclose[0]
        lstm_signal = 1 if predicted_price > current_price * 1.01 else 0  # Buy threshold

        ### Estrategia combinada
        if rf_signal == 1 and lstm_signal == 1 and not self.position:
            self.buy()
            log_signal("BUY", current_price, predicted_price, "EnsembleStrategy")

        elif rf_signal == 0 and lstm_signal == 0 and self.position:
            self.close()
            log_signal("SELL", current_price, predicted_price, "EnsembleStrategy")
        else:
            log_signal("HOLD", current_price, predicted_price, "EnsembleStrategy")

        # Actualizar estado del portafolio en cada paso
        update_portfolio(
            cash=self.broker.get_cash(),
            position=self.position.size,
            portfolio_value=self.broker.get_value()
        )

    def log_signal(signal_type, price, prediction):
        row = {
            "date": datetime.now(),
            "signal": signal_type,
            "price": price,
            "predicted": prediction
        }
        df = pd.DataFrame([row])
        df.to_csv("data/last_signals.csv", mode='a', header=not os.path.exists("data/last_signals.csv"), index=False)

    def update_portfolio(cash, position, value):
        data = {
            "cash": cash,
            "position": position,
            "portfolio_value": value
        }
        with open("data/portfolio_status.json", "w") as f:
            json.dump(data, f)
