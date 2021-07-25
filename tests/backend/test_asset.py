from backend.asset import Asset, Pair, pair_registry


def test_asset_convertion():
    asset = Asset("BTC", 1)

    assert pair_registry.convert_asset_to(asset, "USDT") == Asset("USDT", 35919.667930132)
    assert asset.to("USDT") == Asset("USDT", 35919.667930132)


def test_asset_impossible_convertion():
    asset = Asset("BTC", 1)

    assert pair_registry.convert_asset_to(asset, "NONE") is None
    assert asset.to("NONE") is None


def test_asset_convertion_via_triangular_arbitrage():
    asset = Asset("BTC", 1)

    assert pair_registry.convert_asset_to(asset, "ETH") == Asset("ETH", 16.590680245098763)
    assert asset.to("ETH") == Asset("ETH", 16.590680245098763)


def test_asset_registry_getting_asset_methods(pairs):
    btcusdt = pairs.get("BTCUSDT")

    asset = pair_registry.get_symbol("BTCXXX")
    assert asset is None

    asset = pair_registry.get_symbol("BTCUSDT")
    assert asset == btcusdt

    asset = pair_registry.get_asset("BTC", "XXX")
    assert asset is None

    asset = pair_registry.get_asset("BTC", "USDT")
    assert asset == btcusdt
    assert asset.reverse is False

    asset = pair_registry.get_asset("USDT", "BTC")
    assert asset == btcusdt
    assert asset.reverse is True


def test_asset_registry_filtering():
    assert pair_registry.filter("BTC") == {
        Pair(base="ZEC", quote="BTC", ask=0.003526403, bid=0.003522798),
        Pair(base="ETH", quote="BTC", ask=0.06027575, bid=0.060274804),
        Pair(base="LTC", quote="BTC", ask=0.00401809, bid=0.004016999),
        Pair(base="BTC", quote="USDT", ask=35919.678402335, bid=35919.667930132),
        Pair(base="ADA", quote="BTC", ask=3.825e-05, bid=3.8239e-05),
        Pair(base="BCH", quote="BTC", ask=0.014597, bid=0.014594807),
        Pair(base="DOGE", quote="BTC", ask=7.33e-06, bid=7.317e-06),
    }
    assert pair_registry.filter("ETH") == {
        Pair(base="TRX", quote="ETH", ask=3.1385e-05, bid=3.135e-05),
        Pair(base="DASH", quote="ETH", ask=0.065227079, bid=0.065079817),
        Pair(base="ETH", quote="BTC", ask=0.06027575, bid=0.060274804),
    }
    assert pair_registry.filter("DOGE") == {
        Pair(base="DOGE", quote="BTC", ask=7.33e-06, bid=7.317e-06),
        Pair(base="DOGE", quote="USDT", ask=0.263582276, bid=0.263569094),
    }
    assert pair_registry.filter("NONE") == set()
