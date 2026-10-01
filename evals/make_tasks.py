from pathlib import Path

TASKS = {
    "01_average_off_by_one": {
        "issue": "average() in calculator.py returns wrong values. average([2, 4, 6]) should be 4.",
        "files": {
            "calculator.py": '''def average(numbers):
    return sum(numbers) / (len(numbers) + 1)
''',
            "test_calculator.py": '''from calculator import average

def test_average():
    assert average([2, 4, 6]) == 4

def test_average_single():
    assert average([10]) == 10
''',
        },
    },
    "02_largest_returns_smallest": {
        "issue": "largest() in stats.py returns the smallest number instead of the largest.",
        "files": {
            "stats.py": '''def largest(nums):
    best = nums[0]
    for n in nums:
        if n < best:
            best = n
    return best
''',
            "test_stats.py": '''from stats import largest

def test_largest():
    assert largest([3, 9, 2]) == 9

def test_largest_negative():
    assert largest([-5, -2, -9]) == -2
''',
        },
    },
    "03_palindrome_case_and_spaces": {
        "issue": "is_palindrome() in text.py should ignore letter case and spaces. 'Racecar' and 'A man a plan a canal Panama' should both return True.",
        "files": {
            "text.py": '''def is_palindrome(s):
    return s == s[::-1]
''',
            "test_text.py": '''from text import is_palindrome

def test_case():
    assert is_palindrome("Racecar") is True

def test_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True

def test_negative():
    assert is_palindrome("hello") is False
''',
        },
    },
    "04_fizzbuzz_wrong_order": {
        "issue": "fizzbuzz(15) returns 'Fizz' but should return 'FizzBuzz'.",
        "files": {
            "fizz.py": '''def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    elif n % 15 == 0:
        return "FizzBuzz"
    return str(n)
''',
            "test_fizz.py": '''from fizz import fizzbuzz

def test_fizzbuzz():
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(7) == "7"
''',
        },
    },
    "05_word_count_extra_spaces": {
        "issue": "count_words() in words.py gives wrong counts when the text has multiple spaces or is empty.",
        "files": {
            "words.py": '''def count_words(text):
    return len(text.split(" "))
''',
            "test_words.py": '''from words import count_words

def test_multiple_spaces():
    assert count_words("hello   world") == 2

def test_empty():
    assert count_words("") == 0

def test_simple():
    assert count_words("a b c") == 3
''',
        },
    },
    "06_clamp_bug_in_other_file": {
        "issue": "normalize_score(150) should return 100 and normalize_score(-5) should return 0, but scores come out wrong.",
        "files": {
            "utils.py": '''def clamp(x, lo, hi):
    return min(lo, max(x, hi))
''',
            "scale.py": '''from utils import clamp

def normalize_score(score):
    return clamp(score, 0, 100)
''',
            "test_scale.py": '''from scale import normalize_score

def test_high():
    assert normalize_score(150) == 100

def test_low():
    assert normalize_score(-5) == 0

def test_middle():
    assert normalize_score(50) == 50
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
print(f"Created {len(TASKS)} tasks in {root}")
