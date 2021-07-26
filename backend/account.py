from dataclasses import dataclass, field, replace
from typing import Dict

from backend.asset import Asset
from backend.binance import binance


@dataclass
class Account:
    assets: Dict[str, Asset] = field(default_factory=dict)

    def convert_to(self, asset_name):
        base_asset = Asset(asset_name, 0)

        for asset in self.assets.values():
            converted = asset.to(asset_name)
            if converted:
                base_asset = replace(base_asset, amount=base_asset.amount + converted.amount)
            else:
                raise Exception("Couldn't find a way to convert {asset.name} to {asset_name}")

        return base_asset


def load_account():
    account_info = binance.get_account_info()

    assets = {}
    for asset in account_info.get("balances"):
        amount = float(asset.get("free", 0))

        if amount:
            name = asset.get("asset")
            assets[name] = Asset(name, amount)

    return Account(assets=assets)
