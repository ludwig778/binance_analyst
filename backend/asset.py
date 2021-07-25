from dataclasses import dataclass, field
from datetime import datetime
from itertools import product
from typing import Dict

import pandas as pd
from cachetools import TTLCache, cached

from backend.binance import binance


@dataclass(unsafe_hash=True)
class Asset:
    name: str
    amount: float

    def to(self, target):
        return self.registry.convert_asset_to(self, target)


@dataclass(unsafe_hash=True)
class Pair:
    base: str
    quote: str
    ask: float
    bid: float

    @property
    def symbol(self):
        return self.base + self.quote

    @property
    def tuple(self):
        return self.base, self.quote

    @property
    def spread(self):
        return self.ask - self.bid

    @property
    def klines(self):
        return Pair.kline_repo.get_klines(self.symbol)


class KlinesRepository:
    @staticmethod
    def get_klines(symbol, interval="1d"):
        klines = [
            {
                "timestamp": datetime.fromtimestamp((kline_data[6] + 1) / 1000),
                "open": float(kline_data[1]),
                "high": float(kline_data[2]),
                "low": float(kline_data[3]),
                "close": float(kline_data[4]),
                "volumes": float(kline_data[5]),
                "trades": kline_data[8],
            }
            for kline_data in binance.get_historical_klines(symbol, interval)
        ]

        df = pd.DataFrame(klines)
        df["timestamp"] = pd.DatetimeIndex(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        return df


@dataclass(unsafe_hash=True)
class PairRegistry:
    pairs: Dict[str, Pair] = field(default_factory=dict)

    def set_pairs(self, pairs):
        self.pairs = pairs

    def get_symbol(self, symbol):
        return self.pairs.get(symbol)

    def get_asset(self, base, quote):
        if pair := self.pairs.get(base + quote):
            pair.reverse = False
            return pair

        elif pair := self.pairs.get(quote + base):
            pair.reverse = True
            return pair

    def filter(self, *assets):
        pairs = set()

        for pair in self.pairs.values():
            if pair.base in assets or pair.quote in assets:
                pairs.add(pair)

        return pairs

    @classmethod
    @cached(cache=TTLCache(maxsize=1, ttl=600))
    def retrieve_pairs(self):
        symbols = binance.get_exchange_info()
        prices = binance.get_prices()

        pairs = {}
        for symbol_data in symbols:
            if symbol_data.get("status") not in ("TRADING",):
                continue

            symbol = symbol_data.get("symbol")
            pairs[symbol] = Pair(
                base=symbol_data.get("baseAsset"),
                quote=symbol_data.get("quoteAsset"),
                ask=prices[symbol]["ask"],
                bid=prices[symbol]["bid"],
            )

        return pairs

    def triangular_resolution(self, asset: Asset, target: str, amount: float = None):
        resolutions = {}

        for ours, theirs in product(self.filter(asset.name), self.filter(target)):
            intersect = set(ours.tuple) & set(theirs.tuple)
            if intersect:
                intermediate = intersect.pop()

                resolutions[intermediate] = self.convert_asset_to(
                    self.convert_asset_to(asset, intermediate), target
                )

        return resolutions

    def best_resolution(self, asset: Asset, target: str, amount):
        if resolutions := self.triangular_resolution(asset, target, amount):
            _, asset = sorted(resolutions.items(), key=lambda r: r[1].amount, reverse=True)[0]

            return asset

    def convert_asset_to(self, asset: Asset, target: str, amount: float = None):
        if asset.name == target:
            return asset

        pair = self.get_asset(asset.name, target)

        if not pair:
            if asset := self.best_resolution(asset, target, amount):
                return asset

            else:
                return

        if pair.reverse:
            asset = Asset(target, (amount or asset.amount) / pair.bid)
        else:
            asset = Asset(target, (amount or asset.amount) * pair.bid)

        return asset


pair_registry = PairRegistry()

Asset.registry = pair_registry
Pair.registry = pair_registry
Pair.kline_repo = KlinesRepository
