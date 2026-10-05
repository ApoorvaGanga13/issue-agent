from booking import total_cents


def test_senior_price():
    assert total_cents([("senior", 2)]) == 1800


def test_discount_rounds_down_the_discount():
    assert total_cents([("adult", 1)], 15) == 1063


def test_discount_with_mixed_group():
    assert total_cents([("adult", 2), ("senior", 1)], 10) == 3060


def test_empty_and_zero_quantity():
    assert total_cents([]) == 0
    assert total_cents([("adult", 0)]) == 0
