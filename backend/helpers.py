from datetime import datetime

import pandas as pd

from backend.asset import Pair
from backend.commands import load_klines
from backend.constants import DAY, NO_DAY, YEAR
from repository.json import json_manager


def update_df(perc=None, thresh=None, **kwargs):

    def wrapper(df):
        if perc:
            rows = len(df)
            kwargs.setdefault(
                "thresh",
                int(rows / (100 / perc))
            )

        return df.dropna(axis=1, **kwargs)

    return wrapper


def get_pairs_df(period="1y", refresh=False):
    filename = f"df_{period}.json"

    if (
        not refresh and
        (
            df := json_manager.get(filename, is_df=True)
        ) is not None
    ):
        df.index.rename("timestamp", inplace=True)

    else:
        df = _get_pairs_df()

        json_manager.save(filename, df, is_df=True)

    return df


def _get_pairs_df():
    pairs = Pair.load().values()
    load_klines(pairs)

    df = pd.DataFrame()
    for pair in pairs:
        pair_df = (
            pair
            .klines_1d[["close"]]
            .rename(columns={"close": pair.symbol})
        )

        df = pd.concat([df, pair_df], axis=1)

    # Clean dirty binance data for 1d klines
    timestamps = [str(d)[:10] for d in df.index]
    for ts in set(timestamps):
        if timestamps.count(ts) > 1:
            for index in df.loc[ts].iloc[1:].index:
                df.drop(index=index, inplace=True)

    return df


def get_timeframe(df, timeframe=YEAR, shift=NO_DAY, offset=NO_DAY, update=None):
    date = datetime.fromtimestamp(df.index[-1].timestamp()) - shift
    df = df.loc[date - timeframe - offset:date]

    if update:
        df = update(df)

    return df


def get_periods(df, period=YEAR, shift=NO_DAY, offset=NO_DAY, update=None):
    date = datetime.fromtimestamp(df.index[-1].timestamp()) - shift
    dfs = []

    is_first = True
    while 1:
        loop_offset = period + offset
        if is_first:
            loop_offset += DAY

        period_df = df.loc[date - loop_offset:date]
        if period_df.empty:
            break

        if update:
            period_df = update(period_df)

        # yield period_df #dfs.append(period_df)
        dfs.append(period_df)
        date = date - period
        if is_first:
            date -= DAY
            is_first = False

    return dfs[::-1]
