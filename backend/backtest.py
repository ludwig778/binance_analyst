from pprint import pprint as pp

from backend.helpers import get_periods, get_timeframe, update_df


class Trade:
    def __init__(self, origin, dest, policy=None):
        self.origin = origin
        self.dest = dest
        self.policy = policy
        self.fee = 0.0

        self.process()

    def show(self):
        pp(self.__dict__)

    def process(self):
        pass


class Strategy:
    def __init__(self, name):
        self.name = name

    def process(self, df):
        res = (df.pct_change(1).mean() * len(df.index) * 100)
        res.sort_values(inplace=True, ascending=True)
        print(res)
        print(df.columns)
        print(df["ETHBTC"].rolling(5).mean())
        return res


class Backtest:
    def __init__(self, period, timeframe, strategy, policy=None):
        self.period = period
        self.timeframe = timeframe
        self.strategy = strategy
        self.policy = policy

        self.setup()
        self.show()

    def setup(self, assets=None):
        self.assets = assets or []
        self.trades = []

    def show(self):
        pp(self.__dict__)

    def process(self, df):
        df = get_timeframe(df, timeframe=self.timeframe, update=update_df(perc=100))

        for period in get_periods(df, self.period):
            first_day = period.index[0]
            last_day = period.index[-1]
            print(f"{first_day=} - {last_day=}")

            self.strategy.process(period)
