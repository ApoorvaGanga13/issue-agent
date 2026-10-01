from search import binary_search


def test_single_element():
    assert binary_search([4], 4) == 0


def test_first_element():
    assert binary_search([1, 3, 5, 7, 9], 1) == 0


def test_missing():
    assert binary_search([1, 3, 5, 7, 9], 4) == -1
    assert binary_search([], 1) == -1
