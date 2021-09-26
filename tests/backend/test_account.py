from backend.account import Account
from backend.asset import Asset


def test_account():
    account = Account(
        {
            "BTC": Asset("BTC", 1),
            "ETH": Asset("ETH", 0.1),
        }
    )

    assert account.convert_to("BTC") == Asset("BTC", 1.0060274804)
    assert account.convert_to("USDT") == Asset("USDT", 36136.50141019579)
