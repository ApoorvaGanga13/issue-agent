from flat import flatten

def test_one_level():
    assert flatten([[1, 2], [3]]) == [1, 2, 3]

def test_deep():
    assert flatten([1, [2, [3, [4]]]]) == [1, 2, 3, 4]

def test_strings_untouched():
    assert flatten(["ab", ["cd"]]) == ["ab", "cd"]

def test_empty():
    assert flatten([]) == []
