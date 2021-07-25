from datetime import datetime

from pandas import DataFrame, concat

from backend.constants import DAY, NO_DAY, YEAR


def get_pairs_column_as_dataframes(pairs, column="close"):
    df = DataFrame()

    for pair in pairs:
        pair_df = pair.klines[[column]].rename(columns={column: pair.symbol})

        df = concat([df, pair_df], axis=1)

    return df


def filter_dataframe_columns(df, perc=None, **kwargs):
    if perc:
        rows = len(df)
        kwargs.setdefault("thresh", int(rows / (100 / perc)))

    return df.dropna(axis=1, **kwargs)


def trim_dataframe_by_timeframe(df, timeframe=YEAR, offset=NO_DAY, shift=NO_DAY):
    date = datetime.fromtimestamp(df.index[-1].timestamp()) - shift

    first_date = date - timeframe - offset + DAY
    if first_date < df.iloc[0].name:
        return DataFrame()

    df = df.loc[first_date:date]

    return df


def split_dataframe_by_periods(df, periods=YEAR, offset=NO_DAY, shift=NO_DAY):
    dfs = []

    while 1:
        period_df = trim_dataframe_by_timeframe(df, timeframe=periods, offset=offset, shift=shift)

        if period_df.empty:
            break

        dfs.insert(0, period_df)

        shift += periods

    return dfs
