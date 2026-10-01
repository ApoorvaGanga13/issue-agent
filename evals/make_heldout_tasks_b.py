from pathlib import Path

TASKS = {
    "23_roman_numerals": {
        "issue": "Converting numbers to Roman numerals gives wrong results for some numbers.",
        "files": {
            "roman.py": '''def to_roman(n):
    table = [(1000, "M"), (500, "D"), (100, "C"), (50, "L"), (10, "X"), (5, "V"), (1, "I")]
    out = ""
    for value, symbol in table:
        while n >= value:
            out += symbol
            n -= value
    return out
''',
            "test_roman.py": '''from roman import to_roman


def test_basic():
    assert to_roman(3) == "III"
    assert to_roman(58) == "LVIII"


def test_four():
    assert to_roman(4) == "IV"
''',
        },
        "hidden": {
            "test_hidden_roman.py": '''from roman import to_roman


def test_nine_and_forty():
    assert to_roman(9) == "IX"
    assert to_roman(40) == "XL"


def test_ninety_four_hundred_nine_hundred():
    assert to_roman(90) == "XC"
    assert to_roman(400) == "CD"
    assert to_roman(900) == "CM"


def test_big_numbers():
    assert to_roman(1994) == "MCMXCIV"
    assert to_roman(2024) == "MMXXIV"
''',
        },
    },
    "24_moving_average": {
        "issue": "The moving average report is missing its last value.",
        "files": {
            "averages.py": '''def moving_average(values, window):
    out = []
    for i in range(len(values) - window):
        out.append(sum(values[i:i + window]) / window)
    return out
''',
            "test_averages.py": '''from averages import moving_average


def test_window_two():
    assert moving_average([1, 2, 3, 4, 5], 2) == [1.5, 2.5, 3.5, 4.5]


def test_window_three():
    assert moving_average([2, 4, 6, 8], 3) == [4.0, 6.0]
''',
        },
        "hidden": {
            "test_hidden_averages.py": '''from averages import moving_average


def test_window_equals_length():
    assert moving_average([1, 2, 3], 3) == [2.0]


def test_window_larger_than_data():
    assert moving_average([1, 2], 5) == []


def test_window_one():
    assert moving_average([4], 1) == [4.0]
    assert moving_average([1, 2, 3], 1) == [1.0, 2.0, 3.0]
''',
        },
    },
    "25_top_words": {
        "issue": "The most common words report is wrong when the text has capital letters or punctuation.",
        "files": {
            "wordfreq.py": '''from collections import Counter


def top_words(text, n):
    counts = Counter(text.split())
    return [w for w, _ in counts.most_common(n)]
''',
            "test_wordfreq.py": '''from wordfreq import top_words


def test_case_and_punctuation():
    assert top_words("The cat. the dog", 1) == ["the"]


def test_ties_are_alphabetical():
    assert top_words("b a", 2) == ["a", "b"]
''',
        },
        "hidden": {
            "test_hidden_wordfreq.py": '''from wordfreq import top_words


def test_mixed_case_and_marks():
    assert top_words("Hello, hello! HELLO? world", 1) == ["hello"]


def test_ties_with_more_words():
    assert top_words("a a b b c", 2) == ["a", "b"]


def test_n_larger_than_distinct():
    assert top_words("x y", 10) == ["x", "y"]


def test_empty_text():
    assert top_words("", 3) == []
''',
        },
    },
    "26_pagination": {
        "issue": "Pagination shows the wrong items, and the page count looks off too.",
        "files": {
            "paging.py": '''def paginate(items, page, per_page):
    start = page * per_page
    return items[start:start + per_page]


def total_pages(count, per_page):
    return count // per_page
''',
            "test_paging.py": '''from paging import paginate


def test_first_page():
    assert paginate(list(range(10)), 1, 3) == [0, 1, 2]


def test_second_page():
    assert paginate(list(range(10)), 2, 3) == [3, 4, 5]
''',
        },
        "hidden": {
            "test_hidden_paging.py": '''from paging import paginate, total_pages


def test_last_partial_page():
    assert paginate(list(range(10)), 4, 3) == [9]


def test_page_past_the_end():
    assert paginate(list(range(10)), 5, 3) == []


def test_total_pages_rounds_up():
    assert total_pages(10, 3) == 4
    assert total_pages(9, 3) == 3


def test_total_pages_empty():
    assert total_pages(0, 3) == 0
''',
        },
    },
    "27_median": {
        "issue": "median() gives wrong answers for some lists.",
        "files": {
            "medians.py": '''def median(values):
    values.sort()
    mid = len(values) // 2
    return values[mid]
''',
            "test_medians.py": '''from medians import median


def test_odd_length():
    assert median([3, 1, 2]) == 2


def test_even_length():
    assert median([1, 2, 3, 4]) == 2.5
''',
        },
        "hidden": {
            "test_hidden_medians.py": '''from medians import median


def test_unsorted_even():
    assert median([4, 1, 3, 2]) == 2.5


def test_two_items():
    assert median([1, 2]) == 1.5


def test_single_item():
    assert median([7]) == 7


def test_does_not_modify_input():
    data = [3, 1, 2]
    median(data)
    assert data == [3, 1, 2]
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
print(f"Created {len(TASKS)} more held-out tasks in {root}")
