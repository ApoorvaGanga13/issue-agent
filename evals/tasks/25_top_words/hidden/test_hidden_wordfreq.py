from wordfreq import top_words


def test_mixed_case_and_marks():
    assert top_words("Hello, hello! HELLO? world", 1) == ["hello"]


def test_ties_with_more_words():
    assert top_words("a a b b c", 2) == ["a", "b"]


def test_n_larger_than_distinct():
    assert top_words("x y", 10) == ["x", "y"]


def test_empty_text():
    assert top_words("", 3) == []
