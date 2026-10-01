import pytest
from account import Account, transfer


def test_failed_transfer_changes_nothing():
    a, b = Account(10), Account(5)
    with pytest.raises(ValueError):
        transfer(a, b, 500)
    assert (a.balance, b.balance) == (10, 5)


def test_withdraw_overdraft_raises():
    with pytest.raises(ValueError):
        Account(10).withdraw(20)


def test_transfer_exact_balance():
    a, b = Account(50), Account(0)
    transfer(a, b, 50)
    assert (a.balance, b.balance) == (0, 50)
