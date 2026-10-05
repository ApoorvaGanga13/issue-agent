import pytest

from bill import split_bill, with_tip
from receipt import per_person


def test_shares_always_add_up():
    for total in (0, 1, 99, 1001, 12345):
        for n in (1, 2, 3, 7):
            assert sum(split_bill(total, n)) == total


def test_first_shares_are_larger():
    assert split_bill(10, 4) == [3, 3, 2, 2]


def test_zero_people_is_an_error():
    with pytest.raises(ValueError):
        split_bill(1000, 0)


def test_tip_halves_round_up():
    assert with_tip(1005, 10) == 1106


def test_tip_edge_cases():
    assert with_tip(0, 15) == 0
    assert with_tip(999, 0) == 999


def test_per_person_adds_tip_before_splitting():
    assert per_person(1005, 10, 2) == [553, 553]
