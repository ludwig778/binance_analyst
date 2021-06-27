import numpy as np


def process_simple_rate_of_return(df):
    return df.pct_change(1).mean() * len(df)


def process_compound_rate_of_return(df):
    return (1 + df.pct_change(1).mean()) ** len(df) - 1


def process_log_rate_of_return(df):
    return np.log(df.pct_change(1).mean() + 1) * len(df)


def process_var(df):
    # return df.apply(lambda df: np.var(df, ddof=1) * len(df))
    return df.var() * len(df)


def process_std(df):
    return df.std() * np.sqrt(len(df))
