from pathlib import Path

TASKS = {
    "07_stack_acts_like_queue": {
        "issue": "Stack in stack.py behaves like a queue. pop() should return the most recently pushed item, and popping an empty stack should raise IndexError.",
        "files": {
            "stack.py": '''class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop(0) if self.items else None
''',
            "test_stack.py": '''import pytest
from stack import Stack

def test_lifo_order():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2

def test_pop_empty_raises():
    with pytest.raises(IndexError):
        Stack().pop()
''',
        },
    },
    "08_leap_year_rules": {
        "issue": "days_in_month() in calendar_utils.py returns wrong values for some years.",
        "files": {
            "calendar_utils.py": '''def days_in_month(year, month):
    if month == 2:
        return 29 if year % 4 == 0 else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31
''',
            "test_calendar_utils.py": '''from calendar_utils import days_in_month

def test_leap_years():
    assert days_in_month(2024, 2) == 29
    assert days_in_month(2000, 2) == 29

def test_century_not_leap():
    assert days_in_month(1900, 2) == 28

def test_other_months():
    assert days_in_month(2023, 2) == 28
    assert days_in_month(2023, 4) == 30
    assert days_in_month(2023, 1) == 31
''',
        },
    },
    "09_inventory_multiple_bugs": {
        "issue": "Inventory quantities are wrong in inventory.py: adding the same item twice doesn't accumulate, and stock removal has other problems. Check the tests for the expected behaviour.",
        "files": {
            "inventory.py": '''def add_item(inv, name, qty):
    inv[name] = qty
    return inv


def remove_item(inv, name, qty):
    inv[name] = inv.get(name, 0) - qty
    return inv
''',
            "test_inventory.py": '''import pytest
from inventory import add_item, remove_item

def test_add_accumulates():
    inv = {}
    add_item(inv, "apple", 2)
    add_item(inv, "apple", 3)
    assert inv["apple"] == 5

def test_remove_to_zero_deletes_item():
    inv = {"apple": 2}
    remove_item(inv, "apple", 2)
    assert "apple" not in inv

def test_remove_too_many_raises():
    inv = {"apple": 1}
    with pytest.raises(ValueError):
        remove_item(inv, "apple", 5)
''',
        },
    },
    "10_flatten_deep_nesting": {
        "issue": "flatten() in flat.py doesn't fully flatten deeply nested lists.",
        "files": {
            "flat.py": '''def flatten(items):
    out = []
    for item in items:
        if isinstance(item, list):
            out.extend(item)
        else:
            out.append(item)
    return out
''',
            "test_flat.py": '''from flat import flatten

def test_one_level():
    assert flatten([[1, 2], [3]]) == [1, 2, 3]

def test_deep():
    assert flatten([1, [2, [3, [4]]]]) == [1, 2, 3, 4]

def test_strings_untouched():
    assert flatten(["ab", ["cd"]]) == ["ab", "cd"]

def test_empty():
    assert flatten([]) == []
''',
        },
    },
    "11_rate_limiter_window": {
        "issue": "RateLimiter in limiter.py never lets requests through again after the first `limit` calls, even after the time window has passed.",
        "files": {
            "limiter.py": '''class RateLimiter:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.calls = []

    def allow(self, now):
        if len(self.calls) < self.limit:
            self.calls.append(now)
            return True
        return False
''',
            "test_limiter.py": '''from limiter import RateLimiter

def test_sliding_window():
    rl = RateLimiter(limit=2, window=10)
    assert rl.allow(0) is True
    assert rl.allow(1) is True
    assert rl.allow(2) is False
    assert rl.allow(10) is True
    assert rl.allow(11) is True
    assert rl.allow(11.5) is False
''',
        },
    },
    "12_csv_quoted_commas": {
        "issue": "parse_line() in csvline.py breaks on quoted fields that contain commas.",
        "files": {
            "csvline.py": '''def parse_line(line):
    return line.split(",")
''',
            "test_csvline.py": '''from csvline import parse_line

def test_simple():
    assert parse_line("a,b,c") == ["a", "b", "c"]

def test_empty_fields():
    assert parse_line("x,,z") == ["x", "", "z"]

def test_quoted_comma():
    assert parse_line('a,"b,c",d') == ["a", "b,c", "d"]
''',
        },
    },
}

root = Path("evals/tasks")
for name, task in TASKS.items():
    repo = root / name / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    (root / name / "issue.txt").write_text(task["issue"])
    for filename, content in task["files"].items():
        (repo / filename).write_text(content)
print(f"Created {len(TASKS)} harder tasks in {root}")
