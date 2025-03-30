# tests/test_lstm.py
import unittest
from models.lstm_model import prepare_lstm_data
from data.data_loader import download_data

class TestLSTM(unittest.TestCase):
    def test_data_preparation(self):
        data = download_data("AAPL", "2020-01-01", "2021-01-01")
        X, y, scaler = prepare_lstm_data(data)
        self.assertEqual(len(X), len(y))
        self.assertEqual(X.shape[1], 30)  # Lookback window
        self.assertEqual(X.shape[2], 1)

if __name__ == '__main__':
    unittest.main()
