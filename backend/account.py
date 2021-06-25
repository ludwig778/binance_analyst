from backend.asset import Asset
from backend.binance import binance


class Account:
    def __init__(self):
        self.assets = {}
        self.load()

    def load(self):
        account_info = binance.get_account_info()

        for asset in account_info.get("balances"):
            amount = float(asset.get("free"))
            if amount:
                name = asset.get("asset")
                self.assets[name] = Asset(name, amount)

    def convert_to(self, asset_name):
        base_asset = Asset(asset_name, 0)

        for asset in self.assets.values():
            converted = asset.to(asset_name)
            if converted:
                base_asset += converted
            else:
                print("NOT FOUND", asset, "to", asset_name)

        return base_asset

    def __repr__(self):
        strings = ["<Account"]

        for asset in sorted(self.assets.values(), key=lambda c: c.amount, reverse=True):
            strings.append(f"  {asset}")

        strings.append(">")

        return "\n".join(strings)
