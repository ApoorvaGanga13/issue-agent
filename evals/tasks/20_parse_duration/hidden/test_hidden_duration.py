from duration import parse_duration


def test_minutes_and_seconds():
    assert parse_duration("2m10s") == 130


def test_all_three():
    assert parse_duration("1h0m5s") == 3605


def test_hour_only():
    assert parse_duration("1h") == 3600


def test_empty():
    assert parse_duration("") == 0
