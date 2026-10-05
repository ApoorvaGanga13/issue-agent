import pytest

from stats import error_rate, summarize

LINES = [
    "2026-03-01 12:00:01 INFO payments Started batch",
    "2026-03-01 12:00:02 ERROR payments Card declined for order 17",
    "2026-03-01 12:00:03 ERROR search Index timeout",
    "2026-03-01 12:00:04 INFO search Query served",
    "2026-03-01 12:00:05 INFO search Query served again",
]


def test_summarize_all_levels():
    assert summarize(LINES) == {"INFO": 3, "ERROR": 2}


def test_error_rate_uses_the_services_own_lines():
    assert error_rate(LINES, "payments") == 0.5
    assert error_rate(LINES, "search") == pytest.approx(1 / 3)


def test_unknown_service_is_zero():
    assert error_rate(LINES, "billing") == 0.0


def test_blank_lines_are_ignored():
    assert summarize(["", LINES[0], "   "]) == {"INFO": 1}
    assert error_rate(["", LINES[1]], "payments") == 1.0
