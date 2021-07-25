from dataclasses import replace
from pprint import pprint

from app.settings import settings
from backend.asset import KlinesRepository, pair_registry
from utils.dataframe import DataFrameToolbox

fixtures_folder = settings.ROOT_FOLDER / "tests" / "fixtures"

# selected_assets = "ADA BCH BNB BTC DASH DOGE DOT ETH LINK LTC PAX SOL TRX UNI XRP ZEC"
selected_pairs = (
    "ADAUSDT",
    "BCHUSDT",
    "BNBUSDT",
    "BTCUSDT",
    "DOGEUSDT",
    "DOTUSDT",
    "EOSUSDT",
    "ETHUSDT" "LINKUSDT",
    "LTCUSDT",
    "PAXUSDT",
    "SOLUSDT",
    "TRXUSDT",
    "XRPUSDT",
    "ADABTC",
    "BCHBTC",
    "DOGEBTC",
    "ETHBTC",
    "LTCBTC",
    "ZECBTC",
    "TRXETH",
    "DASHETH",
)


def truncate_float(n, places):
    return int(n * (10 ** places)) / 10 ** places


def retrieve_sample_dataframes():

    new_pairs = {}
    pairs = pair_registry.retrieve_pairs()
    for pair_name in selected_pairs:
        pair = pairs.get(pair_name)

        if not pair:
            continue

        filename = fixtures_folder / f"{pair.symbol}.json"

        df = KlinesRepository.klines_1d(pair.symbol)
        last_price = df.iloc[-1]
        df = df.loc["2018-12-31":"2021-06-30"]
        last_price2 = df.iloc[-1].close
        DataFrameToolbox.save(df, filename)

        perc_ask = pair.ask / last_price.close
        perc_bid = pair.bid / last_price.close

        pair = replace(
            pair,
            ask=f"{truncate_float(last_price2 * perc_ask, 9):.9f}",
            bid=f"{truncate_float(last_price2 * perc_bid, 9):.9f}",
        )
        new_pairs[pair.symbol] = pair

    pprint(new_pairs)


retrieve_sample_dataframes()
