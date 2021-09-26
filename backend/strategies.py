from abc import ABC
from dataclasses import dataclass, replace, field
from datetime import timedelta
from typing import Dict, Generator, List, Union

from backend.account import Account
from backend.asset import Asset, PairRegistry, pair_registry
from backend.trade import Trade, TradeDispatcher
from backend.trade import Trade, TradeDispatcher
from backend.helpers import trim_dataframe_by_timeframe, filter_dataframe_columns
from utils.pair_registry import update_pairs_with_series



@dataclass
class StrategyAbstract(ABC):
    config: Dict = field(default_factory=dict)


@dataclass
class NoStrategy(StrategyAbstract):
    pass


@dataclass
class RebalancingStrategy(StrategyAbstract):
    sensibility: int = 0.01
    def process(self, account):
        total_usdt = account.convert_to("USDT").amount

        total_weight = sum(self.config.values())

        print()
        print()
        print("total")
        print(total_usdt)

        new_account = False
        new_assets = {"USDT": replace(account.assets["USDT"])}

        for k, weight in sorted(self.config.items(), key=lambda x: x[1]):
            percent = weight / total_weight
            tt = total_usdt * percent

            if not (asset := account.assets.get(k)):
                asset = Asset(k, 0.0)

            asset_in_usdt = asset.to("USDT").amount

            print()
            print(weight, total_weight, percent, k, f"{(asset_in_usdt/total_usdt)*100:.1f}%")
            print(
                "aaaaa",
                asset_in_usdt,
                tt,
                percent,
                "-",
                asset_in_usdt / total_usdt,
                (asset_in_usdt / total_usdt) - percent,
                percent - (asset_in_usdt / total_usdt),
                "-=====",
                (asset_in_usdt / total_usdt) - percent > self.sensibility,
                percent - (asset_in_usdt / total_usdt) > self.sensibility,
                #(100 * asset_in_usdt / total_usdt),
                #(100 * asset_in_usdt / total_usdt) - percent,
                percent - (100 * asset_in_usdt / tt)
            )

            if k == "USDT":
                continue
            
            #if asset_in_usdt > (tt * (1 + (self.sensibility / 100))):
            #if self.sensibility < (100 * asset_in_usdt * tt) - percent:
            if (asset_in_usdt / total_usdt) - percent > self.sensibility:
                new_account = True
                diff = abs(tt - asset_in_usdt)
                print(f"Transfering {k} to {tt} USDT")
                
                new_assets[k] = replace(
                    asset,
                    amount=asset.amount - Asset("USDT", diff).to(k).amount
                )
                new_assets["USDT"] = replace(
                    account.assets["USDT"],
                    amount=account.assets["USDT"].amount + diff
                )

            #elif self.sensibility < percent - (100 * asset_in_usdt * tt):
            elif percent - (asset_in_usdt / total_usdt) > self.sensibility:
                new_account = True
                diff = abs(tt - asset_in_usdt)
                print(f"Transfering {tt} USDT to {k}")

                new_assets[k] = replace(
                    asset,
                    amount=asset.amount + Asset("USDT", diff).to(k).amount
                )
                new_assets["USDT"] = replace(
                    account.assets["USDT"],
                    amount=account.assets["USDT"].amount - diff
                )
            else:
                new_assets[k] = asset

        return Account(assets=new_assets)


@dataclass
class StrategyTester:
    dispatcher: TradeDispatcher
    strategy: StrategyAbstract
    timeframe: timedelta

    def prepare(self, df, pairs):
        df = trim_dataframe_by_timeframe(df, timeframe=self.timeframe)
        df = filter_dataframe_columns(df, perc=100)

        pair_names = list(pairs.keys())
        for name in pair_names:
            #if name not in ("BNBUSDT", "DOGEUSDT", "BTCUSDT", "ETHBTC"):
            #    del pairs[name]
            #    if name in df:
            #        del df[name]
            if name not in df:
                del pairs[name]

        return df, pairs

    def step(self):
        pass

    def run(self, df, pairs):
        print("SETUP")
        old_pair_registry = replace(pair_registry)

        df, pairs = self.prepare(df, pairs)

        from pprint import pprint
        i = 0

        account = self.dispatcher.start_account

        for timestamp, row in df.iterrows():

            pair_registry.set_pairs(
                update_pairs_with_series(
                    pairs, row
                )
            )

            print(timestamp)
            print(account.convert_to("USDT"))
            pprint(account.assets)
            if i > 3:
                i = 0
                continue
            account = self.strategy.process(account)
            i += 1

        print("CLEAN")
        pair_registry.set_pairs(old_pair_registry.pairs)

    def clean(self):
        pass

    #strategy: Strategy
    #config: Config
