from words import count_words

def test_multiple_spaces():
    assert count_words("hello   world") == 2

def test_empty():
    assert count_words("") == 0

def test_simple():
    assert count_words("a b c") == 3
