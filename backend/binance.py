import hashlib
import hmac

import requests

from app.settings import API, API_KEY, SECRET_KEY


class BinanceHandler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": API_KEY})

    def get_account_info(self):
        server_time = self.get_time()
        params = f"timestamp={server_time}"
        signature = hmac.new(
            SECRET_KEY.encode("utf-8"),
            params.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        r = self.session.get(
            f"{API}/api/v3/account",
            params={
                "timestamp": server_time,
                "signature": signature
            }
        )

        return r.json()

    def get_exchange_info(self):
        return (
            self.session
            .get(f"{API}/api/v3/exchangeInfo")
            .json()
            .get("symbols")
        )

    def get_time(self):
        return self.session.get(f"{API}/api/v3/time").json().get("serverTime")

    def get_weights(self):
        return {
            k: v
            for k, v in self.session.get(f"{API}/api/v3/ping").headers.items()
            if k.startswith("x-mbx-used")
        }

    def get_ping(self):
        return self.session.get(f"{API}/api/v3/ping").json()

    def get_prices(self):
        return {
            ticker.get("symbol"): {
                "ask": float(ticker.get("askPrice")),
                "bid": float(ticker.get("bidPrice"))
            }
            for ticker in self.session.get(f"{API}/api/v3/ticker/bookTicker").json()
        }

    def get_historical_klines(self, symbol, interval, limit=1000):
        return self.session.get(
            f"{API}/api/v3/klines",
            params={
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            }
        ).json()


binance = BinanceHandler()
