from text import is_palindrome

def test_case():
    assert is_palindrome("Racecar") is True

def test_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True

def test_negative():
    assert is_palindrome("hello") is False
