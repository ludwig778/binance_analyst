from pytest import fixture

from backend.constants import DAY, WEEK, YEAR
from backend.helpers import (
    filter_dataframe_columns,
    get_pairs_column_as_dataframes,
    split_dataframe_by_periods,
    trim_dataframe_by_timeframe,
)
from tests.utils.pairs import get_pairs


@fixture(autouse=True)
def setup(prepare_pair_registry_dataframes):
    pass


def test_get_pairs_column_as_dataframes(pairs):
    sample_pairs = get_pairs(pairs, ["BTCUSDT", "ETHBTC"])

    close_df = get_pairs_column_as_dataframes(sample_pairs, column="close")

    assert len(close_df) == 913
    assert set(close_df.columns) == {"BTCUSDT", "ETHBTC"}

    btcusdt, _ = sample_pairs
    assert btcusdt.klines.close.equals(close_df.BTCUSDT)


def test_filter_dataframe_columns(pairs):
    df = get_pairs_column_as_dataframes(pairs.values(), column="close")

    assert len(pairs) == 20
    assert len(df.columns) == 20

    df_50_perc = filter_dataframe_columns(df, perc=50)
    assert len(df_50_perc.columns) == 18

    df_100_perc = filter_dataframe_columns(df, perc=100)
    assert len(df_100_perc.columns) == 14

    df_300_thresh = filter_dataframe_columns(df, thresh=300)
    assert len(df_300_thresh.columns) == 20

    df_700_thresh = filter_dataframe_columns(df, thresh=700)
    assert len(df_700_thresh.columns) == 16

    df_900_thresh = filter_dataframe_columns(df, thresh=913)
    assert len(df_900_thresh.columns) == 14


def test_trim_dataframe_by_timeframe(pairs):
    df = get_pairs_column_as_dataframes(pairs.values(), column="close")

    assert trim_dataframe_by_timeframe(df, timeframe=YEAR).iloc[-1].name == df.iloc[-1].name

    assert len(trim_dataframe_by_timeframe(df, timeframe=YEAR)) == 365

    assert len(trim_dataframe_by_timeframe(df, timeframe=WEEK)) == 7

    assert len(trim_dataframe_by_timeframe(df, timeframe=YEAR, offset=DAY)) == 366

    assert len(trim_dataframe_by_timeframe(df, timeframe=WEEK, offset=DAY)) == 8

    assert len(trim_dataframe_by_timeframe(df, timeframe=WEEK, shift=4 * DAY)) == 7

    assert trim_dataframe_by_timeframe(df, timeframe=WEEK, shift=4 * DAY).iloc[-1].name == df.iloc[
        -1
    ].name - (4 * DAY)


def test_split_dataframe_by_periods(pairs):
    origin_df = get_pairs_column_as_dataframes(pairs.values(), column="close")

    # Checking with basic 2 weeks periods
    df = trim_dataframe_by_timeframe(origin_df, timeframe=10 * WEEK)
    biweekly_dataframes = split_dataframe_by_periods(df, periods=2 * WEEK)

    assert len(biweekly_dataframes) == 5

    assert len(biweekly_dataframes[0]) == 14
    assert len(biweekly_dataframes[-1]) == 14

    first_item_datetime = df.iloc[0].name
    last_item_datetime = df.iloc[-1].name

    assert biweekly_dataframes[0].iloc[0].name == first_item_datetime
    assert biweekly_dataframes[-1].iloc[-1].name == last_item_datetime

    # Checking with simple offset and shift
    df = trim_dataframe_by_timeframe(origin_df, timeframe=10 * WEEK)
    custom_dataframes = split_dataframe_by_periods(df, periods=WEEK * 2, offset=WEEK, shift=WEEK)

    assert len(custom_dataframes) == 4

    assert len(custom_dataframes[0]) == 21
    assert len(custom_dataframes[-1]) == 21

    assert custom_dataframes[-1].iloc[-1].name == last_item_datetime - WEEK

    # Checking with big parameters so dataframe filtering returns empty dataframes
    df = trim_dataframe_by_timeframe(origin_df, timeframe=WEEK * 2)
    short_dataframes = split_dataframe_by_periods(
        df,
        periods=WEEK,
        offset=WEEK,
        shift=DAY * 3,
    )

    assert len(short_dataframes) == 0
