from pandas import DataFrame
from pytest import fixture

from app.settings import settings
from backend.asset import KlinesRepository, Pair, pair_registry
from utils.dataframe import DataFrameToolbox

fixtures_folder = settings.ROOT_FOLDER / "tests" / "fixtures"


@fixture
def pairs():
    return {
        "ADABTC": Pair(base="ADA", quote="BTC", ask=0.000038250, bid=0.000038239),
        "ADAUSDT": Pair(base="ADA", quote="USDT", ask=1.373221487, bid=1.373110743),
        "BCHBTC": Pair(base="BCH", quote="BTC", ask=0.014597000, bid=0.014594807),
        "BCHUSDT": Pair(base="BCH", quote="USDT", ask=524.193657751, bid=524.182179141),
        "BNBUSDT": Pair(base="BNB", quote="USDT", ask=300.869090221, bid=300.849317666),
        "BTCUSDT": Pair(base="BTC", quote="USDT", ask=35919.678402335, bid=35919.667930132),
        "DASHETH": Pair(base="DASH", quote="ETH", ask=0.065227079, bid=0.065079817),
        "DOGEBTC": Pair(base="DOGE", quote="BTC", ask=0.000007330, bid=0.000007317),
        "DOGEUSDT": Pair(base="DOGE", quote="USDT", ask=0.263582276, bid=0.263569094),
        "DOTUSDT": Pair(base="DOT", quote="USDT", ask=16.319951040, bid=16.318777449),
        "EOSUSDT": Pair(base="EOS", quote="USDT", ask=4.129348720, bid=4.128675639),
        "ETHBTC": Pair(base="ETH", quote="BTC", ask=0.060275750, bid=0.060274804),
        "LTCBTC": Pair(base="LTC", quote="BTC", ask=0.004018090, bid=0.004016999),
        "LTCUSDT": Pair(base="LTC", quote="USDT", ask=144.291367020, bid=144.279946142),
        "PAXUSDT": Pair(base="PAX", quote="USDT", ask=1.000100060, bid=1.000000000),
        "SOLUSDT": Pair(base="SOL", quote="USDT", ask=33.966501424, bid=33.959504274),
        "TRXETH": Pair(base="TRX", quote="ETH", ask=0.000031385, bid=0.000031350),
        "TRXUSDT": Pair(base="TRX", quote="USDT", ask=0.067989120, bid=0.067977296),
        "XRPUSDT": Pair(base="XRP", quote="USDT", ask=0.706300000, bid=0.706184798),
        "ZECBTC": Pair(base="ZEC", quote="BTC", ask=0.003526403, bid=0.003522798),
    }


@fixture
def pair_dataframes(pairs):
    dataframes = {}

    for symbol in pairs.keys():
        dataframes[symbol] = DataFrameToolbox.read(fixtures_folder / f"{symbol}.json")

    return dataframes


@fixture(autouse=True)
def prepare_pair_registry(pairs):
    pair_registry.set_pairs(pairs)

    yield

    pair_registry.set_pairs({})


@fixture(autouse=True)
def prepare_pair_registry_dataframes(pair_dataframes, monkeypatch):
    def _get_klines(symbol, *args, **kwargs):
        df = pair_dataframes.get(symbol)
        if isinstance(df, DataFrame) and not df.empty:
            return df

        return DataFrame()

    monkeypatch.setattr(KlinesRepository, "get_klines", _get_klines)
