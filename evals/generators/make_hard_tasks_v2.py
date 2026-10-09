from pathlib import Path

TASKS = {
    "13_cart_total": {
        "issue": "Customers are being charged the wrong amount at checkout.",
        "files": {
            "pricing.py": '''def apply_discount(price, percent):
    return price * percent / 100
''',
            "cart.py": '''from pricing import apply_discount


class Cart:
    def __init__(self, discount_percent=0):
        self.items = []
        self.discount_percent = discount_percent

    def add(self, name, price, qty=1):
        self.items.append({"name": name, "price": price, "qty": qty})

    def total(self):
        total = sum(item["price"] for item in self.items)
        return round(apply_discount(total, self.discount_percent), 2)
''',
            "test_cart.py": '''from cart import Cart


def test_discount_applied():
    cart = Cart(discount_percent=10)
    cart.add("pen", 10.0)
    assert cart.total() == 9.0
''',
        },
        "hidden": {
            "test_hidden_cart.py": '''from cart import Cart


def test_quantities():
    cart = Cart()
    cart.add("a", 10.0, qty=2)
    cart.add("b", 5.0)
    assert cart.total() == 25.0


def test_discount_with_quantities():
    cart = Cart(discount_percent=20)
    cart.add("a", 10.0, qty=3)
    assert cart.total() == 24.0


def test_empty_cart():
    assert Cart().total() == 0
''',
        },
    },
    "14_merge_intervals": {
        "issue": "Overlapping meeting blocks are not being combined correctly in the scheduler.",
        "files": {
            "scheduler.py": '''def merge_intervals(intervals):
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = end
        else:
            merged.append([start, end])
    return merged
''',
            "test_scheduler.py": '''from scheduler import merge_intervals


def test_overlap():
    assert merge_intervals([[1, 3], [2, 6]]) == [[1, 6]]


def test_nested():
    assert merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]
''',
        },
        "hidden": {
            "test_hidden_scheduler.py": '''from scheduler import merge_intervals


def test_unsorted():
    assert merge_intervals([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]]


def test_touching():
    assert merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]


def test_no_input_mutation():
    data = [[1, 4], [2, 5]]
    merge_intervals(data)
    assert data == [[1, 4], [2, 5]]
''',
        },
    },
    "15_config_merge": {
        "issue": "Loading configuration loses some of the default settings when a user overrides one value.",
        "files": {
            "config.py": '''def merge(defaults, overrides):
    result = defaults
    for key, value in overrides.items():
        result[key] = value
    return result
''',
            "test_config.py": '''from config import merge


def test_nested_override():
    defaults = {"db": {"host": "localhost", "port": 5432}, "debug": False}
    result = merge(defaults, {"db": {"port": 6543}})
    assert result == {"db": {"host": "localhost", "port": 6543}, "debug": False}
''',
        },
        "hidden": {
            "test_hidden_config.py": '''from config import merge


def test_defaults_not_mutated():
    defaults = {"a": {"x": 1}}
    merge(defaults, {"a": {"x": 2}})
    assert defaults == {"a": {"x": 1}}


def test_three_levels():
    d = {"a": {"b": {"c": 1, "d": 2}}}
    assert merge(d, {"a": {"b": {"c": 9}}}) == {"a": {"b": {"c": 9, "d": 2}}}


def test_new_keys():
    assert merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
''',
        },
    },
    "16_lru_cache": {
        "issue": "The cache sometimes throws away entries that were just used.",
        "files": {
            "cache.py": '''class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}
        self.order = []

    def get(self, key):
        return self.data.get(key, -1)

    def put(self, key, value):
        if key not in self.data and len(self.data) >= self.capacity:
            oldest = self.order.pop(0)
            del self.data[oldest]
        self.data[key] = value
        self.order.append(key)
''',
            "test_cache.py": '''from cache import LRUCache


def test_get_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)
    assert c.get("b") == -1
    assert c.get("a") == 1
''',
        },
        "hidden": {
            "test_hidden_cache.py": '''from cache import LRUCache


def test_update_existing_refreshes():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)
    assert c.get("a") == 10
    assert c.get("b") == -1


def test_capacity_one():
    c = LRUCache(1)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == -1
    assert c.get("b") == 2


def test_missing_key():
    assert LRUCache(2).get("zzz") == -1
''',
        },
    },
    "17_is_prime": {
        "issue": "Some composite numbers are reported as prime.",
        "files": {
            "primes.py": '''def is_prime(n):
    for i in range(2, int(n ** 0.5)):
        if n % i == 0:
            return False
    return True
''',
            "test_primes.py": '''from primes import is_prime


def test_composites():
    assert is_prime(9) is False
    assert is_prime(4) is False


def test_primes():
    assert is_prime(7) is True
    assert is_prime(13) is True
''',
        },
        "hidden": {
            "test_hidden_primes.py": '''from primes import is_prime


def test_small_numbers():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True


def test_perfect_squares():
    assert is_prime(25) is False
    assert is_prime(49) is False


def test_larger():
    assert is_prime(97) is True
    assert is_prime(91) is False
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
print(f"Created {len(TASKS)} hard tasks with hidden tests in {root}")
