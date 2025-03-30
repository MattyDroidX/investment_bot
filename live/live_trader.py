# live/live_trader.py
import alpaca_trade_api as tradeapi
import time

API_KEY = 'YOUR_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def check_and_trade():
    position = api.get_position("AAPL") if "AAPL" in [pos.symbol for pos in api.list_positions()] else None
    price = float(api.get_last_trade("AAPL").price)

    # Lógica de entrada (ejemplo simple)
    if price < 150 and not position:
        api.submit_order(symbol="AAPL", qty=10, side="buy", type="market", time_in_force="gtc")
        print("📈 Orden de compra enviada")
    elif price > 160 and position:
        api.submit_order(symbol="AAPL", qty=10, side="sell", type="market", time_in_force="gtc")
        print("📉 Orden de venta enviada")

if __name__ == "__main__":
    while True:
        check_and_trade()
        time.sleep(60)
