# models/lstm_model.py
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

def prepare_lstm_data(data, lookback=30):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(data[['Close']])

    X, y = [], []
    for i in range(lookback, len(scaled)):
        X.append(scaled[i-lookback:i, 0])
        y.append(scaled[i, 0])

    X = np.array(X)
    y = np.array(y)

    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    joblib.dump(scaler, 'models/lstm_scaler.pkl')
    return X, y, scaler

def train_lstm_model(data, lookback=30):
    X, y, _ = prepare_lstm_data(data, lookback)

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=20, batch_size=32, verbose=0)

    model.save('models/lstm_model.h5')
    return model
