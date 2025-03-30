# models/ml_model.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib

def create_features(data):
    data['Return'] = data['Close'].pct_change()
    data['Direction'] = np.where(data['Return'] > 0, 1, 0)
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['Volatility'] = data['Return'].rolling(window=10).std()
    data = data.dropna()
    return data

def train_model(data):
    features = ['SMA_10', 'SMA_50', 'Volatility']
    X = data[features]
    y = data['Direction']
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train_scaled, y_train)

    joblib.dump(model, 'models/rf_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    return model
