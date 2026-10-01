from averages import moving_average


def test_window_equals_length():
    assert moving_average([1, 2, 3], 3) == [2.0]


def test_window_larger_than_data():
    assert moving_average([1, 2], 5) == []


def test_window_one():
    assert moving_average([4], 1) == [4.0]
    assert moving_average([1, 2, 3], 1) == [1.0, 2.0, 3.0]
