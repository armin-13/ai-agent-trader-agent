
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

API_KEY = "pieViHuBmbhtWc1sh5OeilrGGfVr9gTYnRJIA6Jc1kmjytTNE93xiINrtvOONqtO"
API_SECRET = "KnXDPzKzoAJjgMDigHPDmU0rBUFZGkVp9tU7GEserpKZVWEN2Z8LDcavCb9un4d4"
# اتصال به بایننس (تست‌نت)
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

def get_price():
    # Platzhalter: In der echten Version kannst du aktuelle Preise von Binance holen
    return 64000.0
from binance.client import Client
from binance.exceptions import BinanceAPIException

API_KEY = "your_testnet_api_key"
API_SECRET = "your_testnet_api_secret"

client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

initial_capital_usdt = 100
risk_percentage = 0.05
MIN_NOTIONAL = 10

def get_price():
    ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    return float(ticker['price'])

def place_order(symbol="BTCUSDT", side="BUY"):
    try:
        amount_in_usdt = initial_capital_usdt * risk_percentage

        print(f"[⚙️] Trying to {side} {symbol} with ${amount_in_usdt:.2f}")

        if amount_in_usdt < MIN_NOTIONAL:
            print(f"[⛔️] Order skipped: ${amount_in_usdt:.2f} is below Binance MIN_NOTIONAL (${MIN_NOTIONAL})")
            return {"status": "skipped", "reason": "below min notional"}

        if side == "BUY":
            order = client.order_market_buy(symbol=symbol, quoteOrderQty=amount_in_usdt)
        else:
            order = client.order_market_sell(symbol=symbol, quoteOrderQty=amount_in_usdt)

        print(f"[✅] Order placed: {order}")
        return order

    except BinanceAPIException as e:
        print(f"[❌] Binance API Error: {e.message}")
        return {"status": "error", "message": e.message}
    except Exception as e:
        print(f"[‼️] General Error: {str(e)}")
        return {"status": "error", "message": str(e)}

def trade_if_needed(signal: str):
    if signal == "BUY":
        return place_order(side="BUY")
    elif signal == "SELL":
        return place_order(side="SELL")
    else:
        return {"status": "no_action", "message": "Signal was HOLD"}

# 📌 کلید API تست‌نت بایننس (از حساب تست‌نت بگیر)


# سرمایه اولیه کاربر (برای مثال)
initial_capital_usdt = 100

# درصد سرمایه برای هر ترید
risk_percentage = 0.05  # یعنی ۵٪

# حداقل مجاز برای سفارش در بایننس (برای BTCUSDT معمولاً ۱۰ دلار)
MIN_NOTIONAL = 10

def place_order(symbol="BTCUSDT", side="BUY"):
    try:
        amount_in_usdt = initial_capital_usdt * risk_percentage

        print(f"[⚙️] Trying to {side} {symbol} with ${amount_in_usdt:.2f}")

        if amount_in_usdt < MIN_NOTIONAL:
            print(f"[⛔️] Order skipped: ${amount_in_usdt:.2f} is below Binance MIN_NOTIONAL (${MIN_NOTIONAL})")
            return

        if side == "BUY":
            order = client.order_market_buy(
                symbol=symbol,
                quoteOrderQty=amount_in_usdt
            )
        else:
            order = client.order_market_sell(
                symbol=symbol,
                quoteOrderQty=amount_in_usdt
            )

        print(f"[✅] Order placed: {order}")
        return order

    except BinanceAPIException as e:
        print(f"[❌] Binance API Error: {e.message}")
    except Exception as e:
        print(f"[‼️] General Error: {str(e)}")
