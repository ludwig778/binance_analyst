from pytest import fixture

from backend.asset import KlinesRepository


@fixture(autouse=True)
def setup(prepare_pair_registry_dataframes):
    pass


def test_pair_dataframe_repository(pairs):
    pair = pairs["BTCUSDT"]

    pair_df = KlinesRepository.get_klines(pair.symbol)

    assert not pair_df.empty
    assert pair_df.equals(pair.klines)
