from scheduler import merge_intervals


def test_unsorted():
    assert merge_intervals([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]]


def test_touching():
    assert merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]


def test_no_input_mutation():
    data = [[1, 4], [2, 5]]
    merge_intervals(data)
    assert data == [[1, 4], [2, 5]]
