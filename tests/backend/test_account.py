from backend.account import Account
from backend.asset import Asset, Pair, pair_registry


def test_account():
    pair_registry.set_pairs(
        {
            "BTCUSDT": Pair("BTC", "USDT", 10000, 10000),
            "BTCETH": Pair("BTC", "ETH", 100, 100),
            "ETHUSDT": Pair("ETH", "USDT", 100, 100),
            "BTCDOGE": Pair("BTC", "DOGE", 10000, 10000),
            "ETHDASH": Pair("ETH", "DASH", 10000, 10000),
        }
    )

    account = Account(
        {
            "BTC": Asset("BTC", 1),
            "ETH": Asset("ETH", 100),
        }
    )
    assert account.convert_to("BTC") == Asset("BTC", 2)
    assert account.convert_to("USDT") == Asset("USDT", 20000)
