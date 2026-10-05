from pathlib import Path

TASKS = {
    "28_ticket_prices": {
        "issue": "Group bookings are being under-charged.",
        "repo": {
            "README.md": '''# Ticket booking

Prices are in cents.

| Kind   | Price |
|--------|-------|
| adult  | 1250  |
| child  | 600   |
| senior | 900   |

`total_cents(tickets, discount_percent=0)` takes a list of `(kind, quantity)`
pairs and returns the total price in cents.

The discount is a whole-number percent taken off the total. The discount
amount is rounded down to a whole cent.
''',
            "rates.py": '''RATES = {"adult": 1250, "child": 600, "senior": 90}


def base_price(kind):
    return RATES[kind]
''',
            "booking.py": '''from rates import base_price


def total_cents(tickets, discount_percent=0):
    total = 0
    for kind, quantity in tickets:
        total += base_price(kind)
    return total - total * discount_percent // 100
''',
            "test_booking.py": '''from booking import total_cents


def test_group_booking():
    assert total_cents([("adult", 2), ("child", 1)]) == 3100


def test_children_only():
    assert total_cents([("child", 3)]) == 1800
''',
        },
        "hidden": {
            "test_hidden_booking.py": '''from booking import total_cents


def test_senior_price():
    assert total_cents([("senior", 2)]) == 1800


def test_discount_rounds_down_the_discount():
    assert total_cents([("adult", 1)], 15) == 1063


def test_discount_with_mixed_group():
    assert total_cents([("adult", 2), ("senior", 1)], 10) == 3060


def test_empty_and_zero_quantity():
    assert total_cents([]) == 0
    assert total_cents([("adult", 0)]) == 0
''',
        },
        "solution": {
            "rates.py": '''RATES = {"adult": 1250, "child": 600, "senior": 900}


def base_price(kind):
    return RATES[kind]
''',
            "booking.py": '''from rates import base_price


def total_cents(tickets, discount_percent=0):
    total = 0
    for kind, quantity in tickets:
        total += base_price(kind) * quantity
    return total - total * discount_percent // 100
''',
        },
        "partial": {
            "booking.py": '''from rates import base_price


def total_cents(tickets, discount_percent=0):
    total = 0
    for kind, quantity in tickets:
        total += base_price(kind) * quantity
    return total - total * discount_percent // 100
''',
        },
    },
    "29_log_summary": {
        "issue": "The log summary report looks wrong.",
        "repo": {
            "README.md": '''# Log summary

Log lines look like this:

    2026-03-01 12:00:02 ERROR payments Card declined for order 17

The fields are date, time, level, service, and a message that can contain spaces.

`summarize(lines)` returns a dict that counts the lines for each level.

`error_rate(lines, service)` is the share of that service's own lines whose
level is ERROR, as a number from 0 to 1. It is 0.0 when the service has no lines.

Blank lines are ignored by both functions.
''',
            "logparse.py": '''def parse_line(line):
    parts = line.strip().split(" ")
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "service": parts[3],
        "message": parts[4],
    }
''',
            "stats.py": '''from logparse import parse_line


def summarize(lines):
    counts = {}
    for line in lines:
        entry = parse_line(line)
        counts[entry["level"]] = counts.get(entry["level"], 0) + 1
    return counts


def error_rate(lines, service):
    entries = [parse_line(line) for line in lines]
    errors = [e for e in entries if e["level"] == "ERROR" and e["service"] == service]
    return len(errors) / len(entries)
''',
            "test_logparse.py": '''from logparse import parse_line
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
''',
        },
        "hidden": {
            "test_hidden_stats.py": '''import pytest

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
''',
        },
        "solution": {
            "logparse.py": '''def parse_line(line):
    parts = line.strip().split(" ", 4)
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "service": parts[3],
        "message": parts[4],
    }
''',
            "stats.py": '''from logparse import parse_line


def _entries(lines):
    return [parse_line(line) for line in lines if line.strip()]


def summarize(lines):
    counts = {}
    for entry in _entries(lines):
        counts[entry["level"]] = counts.get(entry["level"], 0) + 1
    return counts


def error_rate(lines, service):
    own = [e for e in _entries(lines) if e["service"] == service]
    if not own:
        return 0.0
    return sum(1 for e in own if e["level"] == "ERROR") / len(own)
''',
        },
        "partial": {
            "logparse.py": '''def parse_line(line):
    parts = line.strip().split(" ", 4)
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "service": parts[3],
        "message": parts[4],
    }
''',
        },
    },
    "30_task_order": {
        "issue": "Some jobs run more than once, and certain job lists crash the scheduler.",
        "repo": {
            "README.md": '''# Task order

`run_order(tasks)` takes a dict that maps each task name to the list of tasks
it depends on, and returns the task names in the order they can run.

- A task always comes after the tasks it depends on.
- Every task appears exactly once, even when several tasks depend on it.
- Tasks that do not depend on each other keep the order of the dict.
- A cycle raises ValueError.
- A dependency that is not a key of the dict raises KeyError.
''',
            "taskgraph.py": '''def run_order(tasks):
    order = []

    def visit(name):
        for dep in tasks[name]:
            visit(dep)
        order.append(name)

    for name in tasks:
        visit(name)
    return order
''',
            "test_taskgraph.py": '''from taskgraph import run_order


def test_chain():
    assert run_order({"a": [], "b": ["a"], "c": ["b"]}) == ["a", "b", "c"]


def test_independent_tasks_keep_dict_order():
    assert run_order({"x": [], "y": []}) == ["x", "y"]
''',
        },
        "hidden": {
            "test_hidden_taskgraph.py": '''import pytest

from taskgraph import run_order


def test_shared_dependency_runs_once():
    order = run_order({"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []})
    assert sorted(order) == ["a", "b", "c", "d"]
    assert order.index("a") < order.index("b") < order.index("d")
    assert order.index("a") < order.index("c") < order.index("d")


def test_dependency_listed_after_its_dependent():
    assert run_order({"b": ["a"], "a": []}) == ["a", "b"]


def test_cycle_raises_value_error():
    with pytest.raises(ValueError):
        run_order({"a": ["b"], "b": ["a"]})


def test_self_dependency_is_a_cycle():
    with pytest.raises(ValueError):
        run_order({"a": ["a"]})


def test_unknown_dependency_raises_key_error():
    with pytest.raises(KeyError):
        run_order({"a": ["ghost"]})
''',
        },
        "solution": {
            "taskgraph.py": '''def run_order(tasks):
    order = []
    state = {}

    def visit(name):
        if state.get(name) == "done":
            return
        if state.get(name) == "visiting":
            raise ValueError("cycle at " + str(name))
        state[name] = "visiting"
        for dep in tasks[name]:
            visit(dep)
        state[name] = "done"
        order.append(name)

    for name in tasks:
        visit(name)
    return order
''',
        },
        "partial": {
            "taskgraph.py": '''def run_order(tasks):
    order = []
    seen = set()

    def visit(name):
        if name in seen:
            return
        seen.add(name)
        for dep in tasks[name]:
            visit(dep)
        order.append(name)

    for name in tasks:
        visit(name)
    return order
''',
        },
    },
    "31_bill_split": {
        "issue": "Shares do not add up to the bill, and the tip is sometimes a cent off.",
        "repo": {
            "README.md": '''# Bill splitting

All amounts are whole cents.

`split_bill(total_cents, n)` splits a bill between `n` people. The shares add
up to the total exactly. When the total does not divide evenly, the first
shares are one cent larger than the rest. `n` must be at least 1, otherwise
ValueError is raised.

`with_tip(total_cents, tip_percent)` adds a tip. `tip_percent` is a whole
number. The tip is rounded to the nearest cent, and halves round up.

`per_person(total_cents, tip_percent, n)` adds the tip first, then splits.
''',
            "bill.py": '''def split_bill(total_cents, n):
    return [total_cents // n] * n


def with_tip(total_cents, tip_percent):
    return total_cents + round(total_cents * tip_percent / 100)
''',
            "receipt.py": '''from bill import split_bill, with_tip


def per_person(total_cents, tip_percent, n):
    return split_bill(with_tip(total_cents, tip_percent), n)
''',
            "test_bill.py": '''from bill import split_bill, with_tip


def test_uneven_split_keeps_every_cent():
    assert split_bill(1001, 3) == [334, 334, 333]


def test_even_split():
    assert split_bill(1000, 4) == [250, 250, 250, 250]


def test_simple_tip():
    assert with_tip(2000, 15) == 2300
''',
        },
        "hidden": {
            "test_hidden_bill.py": '''import pytest

from bill import split_bill, with_tip
from receipt import per_person


def test_shares_always_add_up():
    for total in (0, 1, 99, 1001, 12345):
        for n in (1, 2, 3, 7):
            assert sum(split_bill(total, n)) == total


def test_first_shares_are_larger():
    assert split_bill(10, 4) == [3, 3, 2, 2]


def test_zero_people_is_an_error():
    with pytest.raises(ValueError):
        split_bill(1000, 0)


def test_tip_halves_round_up():
    assert with_tip(1005, 10) == 1106


def test_tip_edge_cases():
    assert with_tip(0, 15) == 0
    assert with_tip(999, 0) == 999


def test_per_person_adds_tip_before_splitting():
    assert per_person(1005, 10, 2) == [553, 553]
''',
        },
        "solution": {
            "bill.py": '''def split_bill(total_cents, n):
    if n < 1:
        raise ValueError("n must be at least 1")
    base, extra = divmod(total_cents, n)
    return [base + 1 if i < extra else base for i in range(n)]


def with_tip(total_cents, tip_percent):
    return total_cents + (total_cents * tip_percent + 50) // 100
''',
        },
        "partial": {
            "bill.py": '''def split_bill(total_cents, n):
    base, extra = divmod(total_cents, n)
    return [base + 1 if i < extra else base for i in range(n)]


def with_tip(total_cents, tip_percent):
    return total_cents + round(total_cents * tip_percent / 100)
''',
        },
    },
    "32_room_bookings": {
        "issue": "Rooms that are free are being turned away, and the nights report is too high.",
        "repo": {
            "README.md": '''# Room bookings

A booking is a pair `(start, end)` of day numbers. It occupies the nights from
`start` up to, but not including, `end`. A booking that starts on the day
another one ends does not overlap it.

- `overlaps(a, b)` says whether two bookings share a night.
- `can_book(existing, new)` is True when `new` overlaps none of the existing bookings.
- `overlaps` and `can_book` raise ValueError for a booking that does not end after it starts.
- `nights(booking)` is the number of nights it occupies.
- `total_nights(bookings)` adds up the nights of all bookings.
''',
            "bookings.py": '''def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]


def can_book(existing, new):
    return all(not overlaps(new, booking) for booking in existing)
''',
            "report.py": '''def nights(booking):
    return booking[1] - booking[0] + 1


def total_nights(bookings):
    return sum(nights(booking) for booking in bookings)
''',
            "test_bookings.py": '''from bookings import can_book, overlaps


def test_partial_overlap():
    assert overlaps((1, 5), (3, 8)) is True


def test_back_to_back_does_not_overlap():
    assert overlaps((1, 5), (5, 8)) is False


def test_can_book_free_slot():
    assert can_book([(1, 5)], (7, 9)) is True
''',
        },
        "hidden": {
            "test_hidden_bookings.py": '''import pytest

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
''',
        },
        "solution": {
            "bookings.py": '''def _check(booking):
    if booking[1] <= booking[0]:
        raise ValueError("a booking must end after it starts")


def overlaps(a, b):
    _check(a)
    _check(b)
    return a[0] < b[1] and b[0] < a[1]


def can_book(existing, new):
    _check(new)
    return all(not overlaps(new, booking) for booking in existing)
''',
            "report.py": '''def nights(booking):
    return booking[1] - booking[0]


def total_nights(bookings):
    return sum(nights(booking) for booking in bookings)
''',
        },
        "partial": {
            "bookings.py": '''def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def can_book(existing, new):
    return all(not overlaps(new, booking) for booking in existing)
''',
        },
    },
    "33_config_loading": {
        "issue": "Environment settings do not behave properly, and one request's settings show up in the next.",
        "repo": {
            "README.md": '''# Config loading

`load(env=None)` returns the settings as a dict. `env` is a dict of environment
variables and defaults to `os.environ`.

- The defaults live in `defaults.py`.
- A setting called `port` is overridden by the variable `APP_PORT`, and so on.
- The value is converted to the type of the default. Integers use `int()`.
  For booleans, `true`, `1` and `yes` (any capital letters, spaces ignored)
  mean True and any other value means False.
- Variables that do not match a setting are ignored.
- An integer setting with a value that is not a number raises ValueError.
- The defaults are never modified, and every call returns a new dict.
''',
            "defaults.py": '''DEFAULTS = {"port": 8080, "debug": False, "workers": 2, "name": "app"}
''',
            "loader.py": '''import os

from defaults import DEFAULTS


def load(env=None):
    env = os.environ if env is None else env
    config = DEFAULTS
    for key in config:
        value = env.get("APP_" + key.upper())
        if value is not None:
            config[key] = value
    return config
''',
            "test_loader.py": '''from loader import load


def test_port_is_a_number():
    assert load({"APP_PORT": "9000"})["port"] == 9000


def test_name_stays_text():
    assert load({"APP_NAME": "shop"})["name"] == "shop"
''',
        },
        "hidden": {
            "test_hidden_loader.py": '''import pytest

from loader import load


def test_defaults_when_nothing_is_set():
    assert load({}) == {"port": 8080, "debug": False, "workers": 2, "name": "app"}


def test_calls_do_not_leak_into_each_other():
    load({"APP_PORT": "1", "APP_NAME": "x"})
    assert load({})["port"] == 8080
    assert load({})["name"] == "app"


def test_returned_dict_is_a_copy():
    config = load({})
    config["port"] = 1
    assert load({})["port"] == 8080


def test_boolean_values():
    assert load({"APP_DEBUG": "TRUE"})["debug"] is True
    assert load({"APP_DEBUG": " yes "})["debug"] is True
    assert load({"APP_DEBUG": "1"})["debug"] is True
    assert load({"APP_DEBUG": "no"})["debug"] is False
    assert load({"APP_DEBUG": "0"})["debug"] is False


def test_integer_values():
    assert load({"APP_WORKERS": "4"})["workers"] == 4


def test_bad_integer_raises():
    with pytest.raises(ValueError):
        load({"APP_PORT": "abc"})


def test_unknown_variables_are_ignored():
    assert load({"APP_COLOR": "red", "OTHER": "1"}) == load({})
''',
        },
        "solution": {
            "loader.py": '''import os

from defaults import DEFAULTS

TRUE_VALUES = {"true", "1", "yes"}


def _convert(value, default):
    if isinstance(default, bool):
        return value.strip().lower() in TRUE_VALUES
    if isinstance(default, int):
        return int(value)
    return value


def load(env=None):
    env = os.environ if env is None else env
    config = dict(DEFAULTS)
    for key, default in DEFAULTS.items():
        value = env.get("APP_" + key.upper())
        if value is not None:
            config[key] = _convert(value, default)
    return config
''',
        },
        "partial": {
            "loader.py": '''import os

from defaults import DEFAULTS

TRUE_VALUES = {"true", "1", "yes"}


def _convert(value, default):
    if isinstance(default, bool):
        return value.strip().lower() in TRUE_VALUES
    if isinstance(default, int):
        return int(value)
    return value


def load(env=None):
    env = os.environ if env is None else env
    config = DEFAULTS
    for key, default in DEFAULTS.items():
        value = env.get("APP_" + key.upper())
        if value is not None:
            config[key] = _convert(value, default)
    return config
''',
        },
    },
    "34_grid_paths": {
        "issue": "Navigation sometimes says there is no route when there is one, and gives an odd answer when there really is none.",
        "repo": {
            "README.md": '''# Grid paths

A grid is a list of strings. `#` is a wall, `.` is open floor, `S` is the
start, and `G` is the goal. There is exactly one `S` and one `G`.

`shortest(rows)` returns the fewest steps from `S` to `G`. A step moves one
cell up, down, left or right, never diagonally and never through a wall.
When there is no path it returns -1.
''',
            "grid.py": '''def parse(rows):
    walls = set()
    start = goal = None
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "#":
                walls.add((r, c))
            elif ch == "S":
                start = (r, c)
            elif ch == "G":
                goal = (r, c)
    return walls, start, goal
''',
            "paths.py": '''from collections import deque

from grid import parse

DIRECTIONS = [(1, 0), (-1, 0), (0, 1)]


def shortest(rows):
    walls, start, goal = parse(rows)
    height, width = len(rows), len(rows[0])
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == goal:
            return dist
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            inside = 0 <= nr < height and 0 <= nc < width
            if inside and (nr, nc) not in walls and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    return None
''',
            "test_paths.py": '''from paths import shortest


def test_straight_line():
    assert shortest(["S.G"]) == 2


def test_path_that_goes_left():
    rows = [
        "G#S",
        ".#.",
        "...",
    ]
    assert shortest(rows) == 6
''',
        },
        "hidden": {
            "test_hidden_paths.py": '''from paths import shortest


def test_unreachable_goal():
    assert shortest(["S#G"]) == -1


def test_open_field():
    assert shortest(["S..", "...", "..G"]) == 4
    assert shortest(["G..", "...", "..S"]) == 4


def test_detour_around_a_wall():
    assert shortest(["S.#G", "..#.", "...."]) == 7


def test_start_next_to_goal():
    assert shortest(["SG"]) == 1
    assert shortest(["GS"]) == 1
''',
        },
        "solution": {
            "paths.py": '''from collections import deque

from grid import parse

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def shortest(rows):
    walls, start, goal = parse(rows)
    height, width = len(rows), len(rows[0])
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == goal:
            return dist
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            inside = 0 <= nr < height and 0 <= nc < width
            if inside and (nr, nc) not in walls and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    return -1
''',
        },
        "partial": {
            "paths.py": '''from collections import deque

from grid import parse

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def shortest(rows):
    walls, start, goal = parse(rows)
    height, width = len(rows), len(rows[0])
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == goal:
            return dist
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            inside = 0 <= nr < height and 0 <= nc < width
            if inside and (nr, nc) not in walls and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    return None
''',
        },
    },
}

root = Path("evals/tasks")
for name, task in TASKS.items():
    base = root / name
    base.mkdir(parents=True, exist_ok=True)
    (base / "issue.txt").write_text(task["issue"])
    for folder in ("repo", "hidden", "solution", "partial"):
        for filename, content in task[folder].items():
            target = base / folder / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
print(f"Created {len(TASKS)} multi-file tasks in {root}")
