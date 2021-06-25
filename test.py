from json import loads
from pprint import pprint as pp

import requests


from app.settings import *
from backend.account import *
from backend.analysis import *
from backend.asset import *
from backend.binance import *
from backend.commands import *
from backend.constants import *
from backend.backtest import *
from backend.helpers import *

df = get_pairs_df()

s = Strategy("test")
b = Backtest(3 * MONTH, 2 * YEAR, strategy=s)
b.process(df)






print("\n" * 1)
