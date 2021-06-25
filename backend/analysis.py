from datetime import datetime

from backend.constants import NO_DAY, DAY, YEAR


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
