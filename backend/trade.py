from dataclasses import dataclass, field
from typing import Dict, List

from backend.account import Account
from backend.asset import Asset, Pair


@dataclass
class Trade:
    origin: Asset
    dest: Asset
    fee: float = 0.0


@dataclass
class TradeDispatcher:
    start_account: Account
    pairs: List[Pair] = field(default_factory=list)
