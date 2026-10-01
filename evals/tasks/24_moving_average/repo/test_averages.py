from averages import moving_average


def test_window_two():
    assert moving_average([1, 2, 3, 4, 5], 2) == [1.5, 2.5, 3.5, 4.5]


def test_window_three():
    assert moving_average([2, 4, 6, 8], 3) == [4.0, 6.0]
