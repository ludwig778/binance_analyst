from copy import deepcopy
from dataclasses import replace

from backend.asset import Pair, PairRegistry


def update_pairs_with_series(pairs, pair_series):
    new_pairs = deepcopy(pairs)

    for name, pair in pairs.items():
        price = getattr(pair_series, name, 0.0)
        new_pairs[name] = replace(pair, ask=price, bid=price)

    return new_pairs
