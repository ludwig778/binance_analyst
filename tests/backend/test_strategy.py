from pytest import mark

from backend.account import Account
from backend.asset import Asset, Pair, pair_registry
from backend.constants import YEAR
from backend.helpers import get_pairs_column_as_dataframes
from backend.strategies import StrategyTester, NoStrategy, RebalancingStrategy
from backend.trade import Trade, TradeDispatcher
from utils.pair_registry import update_pairs_with_series


def test_rebalancing_strategy_basic_setup():
    pair_registry.set_pairs({
        "BTCUSDT": Pair("BTC", "USDT", 10000, 10000)
    })
    account = Account({"USDT": Asset("USDT", 10000)})
    strategy = RebalancingStrategy({"BTC": 1, "USDT": 1})
    new_account = strategy.process(account)

    assert new_account == Account({
        "BTC": Asset("BTC", 0.5),
        "USDT": Asset("USDT", 5000.0)
    })


def test_rebalancing_strategy_sensibility_triggering():
    pair_registry.set_pairs({
        "BTCUSDT": Pair("BTC", "USDT", 10000, 10000)
    })
    account = Account({"USDT": Asset("USDT", 10000)})
    strategy = RebalancingStrategy({"BTC": 1, "USDT": 99}, 0.02)
    new_account = strategy.process(account)

    assert new_account == Account({
        "BTC": Asset("BTC", 0.0),
        "USDT": Asset("USDT", 10000.0)
    })

    account = new_account
    strategy = RebalancingStrategy({"BTC": 2, "USDT": 98}, 0.01)
    new_account = strategy.process(account)

    assert new_account == Account({
        "BTC": Asset("BTC", 0.02),
        "USDT": Asset("USDT", 9800.0)
    })

    from pprint import pprint
    print()

    pprint(account.assets)
    print()
    pprint(new_account.assets)



@mark.skip
def test_strategy_tester(pairs, pair_dataframes):
    pair_list = list(pairs.values())

    account = Account({"USDT": Asset("USDT", 1000)})
    dispatcher = TradeDispatcher(account, pair_list)

    strategy = RebalancingStrategy({  
        #"BTC": 20, 
        #"USDT": 40,
        #"DOGE": 20,
        "XRP": 50,
        "LTC": 50,
    })
    tester = StrategyTester(dispatcher, strategy, YEAR * 1.5)
    close_df = get_pairs_column_as_dataframes(pair_list, column="close")

    tester.run(close_df, pairs)
