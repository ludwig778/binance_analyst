from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Generator, List, Union

from backend.asset import Asset
from backend.helpers import get_periods, get_timeframe, update_df


@dataclass
class Config:
    parameter_matrix: Dict[str, Union[str, int, float, Generator[int, None, None]]]


class StrategyTester:
    assets: List[Asset]
    trades: List[Trade]

    period: timedelta
    timeframe: timedelta
    strategy: Strategy
    config: Config

    def setup(self, df):
        df = get_timeframe(df, timeframe=self.timeframe, update=update_df(perc=100))

        for period in get_periods(df, self.period):
            first_day = period.index[0]
            last_day = period.index[-1]
            print(f"{first_day=} - {last_day=}")

            self.strategy.process(period)
