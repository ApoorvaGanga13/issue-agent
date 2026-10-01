from scheduler import merge_intervals


def test_overlap():
    assert merge_intervals([[1, 3], [2, 6]]) == [[1, 6]]


def test_nested():
    assert merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]
