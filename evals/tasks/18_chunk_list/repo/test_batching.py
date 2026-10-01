from batching import chunk


def test_even_split():
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_three_way():
    assert chunk([1, 2, 3, 4, 5, 6], 3) == [[1, 2, 3], [4, 5, 6]]
