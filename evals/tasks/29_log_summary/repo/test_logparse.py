from logparse import parse_line
from stats import summarize

LINE = "2026-03-01 12:00:02 ERROR payments Card declined for order 17"


def test_fields():
    entry = parse_line(LINE)
    assert entry["level"] == "ERROR"
    assert entry["service"] == "payments"


def test_message_keeps_every_word():
    assert parse_line(LINE)["message"] == "Card declined for order 17"


def test_summarize_counts_levels():
    lines = [LINE, "2026-03-01 12:00:03 INFO search Query served"]
    assert summarize(lines) == {"ERROR": 1, "INFO": 1}
