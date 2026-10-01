from wordfreq import top_words


def test_case_and_punctuation():
    assert top_words("The cat. the dog", 1) == ["the"]


def test_ties_are_alphabetical():
    assert top_words("b a", 2) == ["a", "b"]
