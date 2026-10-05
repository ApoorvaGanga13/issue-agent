import pytest

from bookings import can_book, overlaps
from report import nights, total_nights


def test_back_to_back_can_be_booked():
    assert can_book([(1, 5)], (5, 8)) is True


def test_nested_booking_overlaps():
    assert overlaps((1, 10), (3, 4)) is True


def test_nights_counts_nights_not_days():
    assert nights((1, 5)) == 4
    assert nights((3, 4)) == 1


def test_total_nights():
    assert total_nights([(1, 5), (5, 8)]) == 7
    assert total_nights([]) == 0


def test_booking_must_end_after_it_starts():
    with pytest.raises(ValueError):
        overlaps((5, 5), (1, 9))
    with pytest.raises(ValueError):
        can_book([], (3, 3))
    with pytest.raises(ValueError):
        can_book([(1, 5)], (8, 6))
