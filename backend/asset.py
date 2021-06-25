from datetime import datetime
from itertools import product

import pandas as pd
from cachetools import TTLCache, cached

from backend.binance import binance
from repository.json import json_manager


class Asset:
    def __init__(self, name, amount):
        self.name = name
        self.amount = float(amount)

    def __add__(self, other):
        if self.name != other.name:
            print("the 2 assets must be the same")
            return

        return Asset(self.name, self.amount + other.amount)

    def __repr__(self):
        return f"<Asset {self.name} : {self.amount}>"

    def triangular_resolution(self, asset, amount=None):
        resolutions = {}

        for ours, theirs in product(Pair.filter(self.name), Pair.filter(asset)):
            intersect = set(ours.tuple) & set(theirs.tuple)
            if intersect:
                intermediate = intersect.pop()

                resolutions[intermediate] = (
                    self
                    .to(intermediate)
                    .to(asset)
                )

        return resolutions

    def best_resolution(self, asset, amount):
        if resolutions := self.triangular_resolution(asset, amount):
            _, asset = sorted(
                resolutions.items(),
                key=lambda r: r[1].amount,
                reverse=True
            )[0]

            return asset

    def to(self, asset, amount=None):
        if self.name == asset:
            return self

        pair = Pair.get(self.name, asset)

        if not pair:
            if asset := self.best_resolution(asset, amount):
                return asset

            else:
                print("Couldn't find pair")
                return

        if pair.reverse:
            asset = Asset(asset, self.amount / pair.bid)
        else:
            asset = Asset(asset, self.amount * pair.bid)

        # Calculate Fees here

        return asset


class Pair:
    def __init__(self, base, quote, ask, bid):
        self.base = base
        self.quote = quote
        self.ask = ask
        self.bid = bid

    @property
    def symbol(self):
        return self.base + self.quote

    @property
    def tuple(self):
        return self.base, self.quote

    @property
    def spread(self):
        return self.ask - self.bid

    def __repr__(self):
        return f"<Pair {self.symbol} : {self.ask} {self.bid}>"

    @property
    def klines_1d(self):
        return self.get_klines()

    @cached(cache=TTLCache(maxsize=1200, ttl=3600))
    def get_klines(self, interval="1d"):
        filename = f"{self.__class__.__name__.lower()}_{self.symbol}_{interval}.json"

        klines = json_manager.get(filename) or []

        if not klines:
            for kline_data in binance.get_historical_klines(f"{self.base}{self.quote}", "1d"):
                kline = {
                    "timestamp": datetime.fromtimestamp((kline_data[6] + 1) / 1000),
                    "open": float(kline_data[1]),
                    "high": float(kline_data[2]),
                    "low": float(kline_data[3]),
                    "close": float(kline_data[4]),
                    "volumes": float(kline_data[5]),
                    "trades": kline_data[8]
                }
                klines.append(kline)

            json_manager.save(filename, klines)

        df = pd.DataFrame(klines)
        df["timestamp"] = pd.DatetimeIndex(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        return df

    @classmethod
    def get_symbol(cls, symbol):
        pairs = cls.load()

        return pairs.get(symbol)

    @classmethod
    def get(cls, base, quote):
        pairs = cls.load()

        if pair := pairs.get(f"{base}{quote}"):
            pair.reverse = False
            return pair

        elif pair := pairs.get(f"{quote}{base}"):
            pair.reverse = True
            return pair

    @classmethod
    def filter(cls, *assets):
        pairs = []

        for pair in cls.load().values():
            if pair.base in assets or pair.quote in assets:
                pairs.append(pair)

        return pairs

    @classmethod
    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def load(cls):
        symbols = binance.get_exchange_info()
        prices = binance.get_prices()

        pairs = {}
        for symbol_data in symbols:
            if symbol_data.get("status") not in ("TRADING",):
                continue

            symbol = symbol_data.get("symbol")
            pairs[symbol] = cls(
                base=symbol_data.get("baseAsset"),
                quote=symbol_data.get("quoteAsset"),
                ask=prices[symbol]["ask"],
                bid=prices[symbol]["bid"]
            )

        return pairs
