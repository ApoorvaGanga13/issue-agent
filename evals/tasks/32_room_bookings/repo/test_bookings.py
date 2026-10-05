from bookings import can_book, overlaps


def test_partial_overlap():
    assert overlaps((1, 5), (3, 8)) is True


def test_back_to_back_does_not_overlap():
    assert overlaps((1, 5), (5, 8)) is False


def test_can_book_free_slot():
    assert can_book([(1, 5)], (7, 9)) is True
