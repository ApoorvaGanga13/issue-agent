from duration import parse_duration


def test_single_unit():
    assert parse_duration("90s") == 90


def test_hours_and_minutes():
    assert parse_duration("1h30m") == 5400
