from pathlib import Path

TASKS = {
    "18_chunk_list": {
        "issue": "Splitting a list into batches sometimes loses items.",
        "files": {
            "batching.py": '''def chunk(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs) - n, n)]
''',
            "test_batching.py": '''from batching import chunk


def test_even_split():
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_three_way():
    assert chunk([1, 2, 3, 4, 5, 6], 3) == [[1, 2, 3], [4, 5, 6]]
''',
        },
        "hidden": {
            "test_hidden_batching.py": '''from batching import chunk


def test_partial_last_chunk():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_empty():
    assert chunk([], 3) == []


def test_chunk_bigger_than_list():
    assert chunk([1, 2], 5) == [[1, 2]]
''',
        },
    },
    "19_binary_search": {
        "issue": "Searching for the last element of a list sometimes says it is missing.",
        "files": {
            "search.py": '''def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
''',
            "test_search.py": '''from search import binary_search


def test_last_element():
    assert binary_search([1, 3, 5, 7, 9], 9) == 4


def test_middle_element():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2
''',
        },
        "hidden": {
            "test_hidden_search.py": '''from search import binary_search


def test_single_element():
    assert binary_search([4], 4) == 0


def test_first_element():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0


def test_missing():
    assert binary_search([1, 3, 5, 7, 9], 4) == -1
    assert binary_search([], 1) == -1
''',
        },
    },
    "20_parse_duration": {
        "issue": "Durations with more than one unit come out too big.",
        "files": {
            "duration.py": '''def parse_duration(s):
    total = 0
    num = ""
    for ch in s:
        if ch.isdigit():
            num += ch
        elif ch == "h":
            total += int(num) * 3600
        elif ch == "m":
            total += int(num) * 60
        elif ch == "s":
            total += int(num)
    return total
''',
            "test_duration.py": '''from duration import parse_duration


def test_single_unit():
    assert parse_duration("90s") == 90


def test_hours_and_minutes():
    assert parse_duration("1h30m") == 5400
''',
        },
        "hidden": {
            "test_hidden_duration.py": '''from duration import parse_duration


def test_minutes_and_seconds():
    assert parse_duration("2m10s") == 130


def test_all_three():
    assert parse_duration("1h0m5s") == 3605


def test_hour_only():
    assert parse_duration("1h") == 3600


def test_empty():
    assert parse_duration("") == 0
''',
        },
    },
    "21_shared_tags": {
        "issue": "Tags from one call show up in later, unrelated calls.",
        "files": {
            "tags.py": '''def add_tag(item, tags=[]):
    tags.append(item)
    return tags
''',
            "test_tags.py": '''from tags import add_tag


def test_independent_calls():
    assert add_tag("a") == ["a"]
    assert add_tag("b") == ["b"]
''',
        },
        "hidden": {
            "test_hidden_tags.py": '''from tags import add_tag


def test_many_fresh_calls():
    for i in range(3):
        assert add_tag(i) == [i]


def test_explicit_list_is_extended():
    mine = ["x"]
    result = add_tag("y", mine)
    assert result == ["x", "y"]
    assert mine == ["x", "y"]
''',
        },
    },
    "22_overdraft": {
        "issue": "Customers can spend money they do not have.",
        "files": {
            "account.py": '''class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


def transfer(src, dst, amount):
    dst.deposit(amount)
    src.withdraw(amount)
''',
            "test_account.py": '''import pytest
from account import Account, transfer


def test_transfer_moves_money():
    a, b = Account(100), Account(0)
    transfer(a, b, 40)
    assert (a.balance, b.balance) == (60, 40)


def test_transfer_insufficient_funds():
    a, b = Account(10), Account(0)
    with pytest.raises(ValueError):
        transfer(a, b, 500)
''',
        },
        "hidden": {
            "test_hidden_account.py": '''import pytest
from account import Account, transfer


def test_failed_transfer_changes_nothing():
    a, b = Account(10), Account(5)
    with pytest.raises(ValueError):
        transfer(a, b, 500)
    assert (a.balance, b.balance) == (10, 5)


def test_withdraw_overdraft_raises():
    with pytest.raises(ValueError):
        Account(10).withdraw(20)


def test_transfer_exact_balance():
    a, b = Account(50), Account(0)
    transfer(a, b, 50)
    assert (a.balance, b.balance) == (0, 50)
''',
        },
    },
}

root = Path("evals/tasks")
for name, task in TASKS.items():
    base = root / name
    (base / "repo").mkdir(parents=True, exist_ok=True)
    (base / "hidden").mkdir(parents=True, exist_ok=True)
    (base / "issue.txt").write_text(task["issue"])
    for filename, content in task["files"].items():
        (base / "repo" / filename).write_text(content)
    for filename, content in task["hidden"].items():
        (base / "hidden" / filename).write_text(content)
print(f"Created {len(TASKS)} held-out tasks in {root}")
