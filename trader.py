
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

# 📌 کلید API تست‌نت بایننس (از حساب تست‌نت بگیر)
API_KEY = "pieViHuBmbhtWc1sh5OeilrGGfVr9gTYnRJIA6Jc1kmjytTNE93xiINrtvOONqtO"
API_SECRET = "KnXDPzKzoAJjgMDigHPDmU0rBUFZGkVp9tU7GEserpKZVWEN2Z8LDcavCb9un4d4"

# اتصال به بایننس (تست‌نت)
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

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
