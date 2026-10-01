import pytest
from account import Account, transfer


def test_transfer_moves_money():
    a, b = Account(100), Account(0)
    transfer(a, b, 40)
    assert (a.balance, b.balance) == (60, 40)


def test_transfer_insufficient_funds():
    a, b = Account(10), Account(0)
    with pytest.raises(ValueError):
        transfer(a, b, 500)
