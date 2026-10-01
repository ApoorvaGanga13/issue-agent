from batching import chunk


def test_partial_last_chunk():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_empty():
    assert chunk([], 3) == []


def test_chunk_bigger_than_list():
    assert chunk([1, 2], 5) == [[1, 2]]
