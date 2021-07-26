from abc import ABC
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Generator, List, Union

from backend.asset import Asset
from backend.trade import Trade, TradeDispatcher
from backend.trade import Trade, TradeDispatcher
from backend.helpers import trim_dataframe_by_timeframe


@dataclass
class StrategyAbstract(ABC):
    name: str


class NoStrategy(StrategyAbstract):
    pass


class RebalancingStrategy(StrategyAbstract):
    pass


@dataclass
class StrategyTester:
    dispatcher: TradeDispatcher
    strategy: StrategyAbstract
    timeframe: timedelta

    def run(self, df):
        df = trim_dataframe_by_timeframe(df, timeframe=self.timeframe)
        df = filter_dataframe_columns(df, perc=100)

        for period in get_periods(df, self.period):
            first_day = period.index[0]
            last_day = period.index[-1]
            print(f"{first_day=} - {last_day=}")

            self.strategy.process(period)




    #strategy: Strategy
    #config: Config
