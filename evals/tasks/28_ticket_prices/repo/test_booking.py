from booking import total_cents


def test_group_booking():
    assert total_cents([("adult", 2), ("child", 1)]) == 3100


def test_children_only():
    assert total_cents([("child", 3)]) == 1800
