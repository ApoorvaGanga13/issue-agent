from medians import median


def test_unsorted_even():
    assert median([4, 1, 3, 2]) == 2.5


def test_two_items():
    assert median([1, 2]) == 1.5


def test_single_item():
    assert median([7]) == 7


def test_does_not_modify_input():
    data = [3, 1, 2]
    median(data)
    assert data == [3, 1, 2]
