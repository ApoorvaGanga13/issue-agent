from search import binary_search


def test_last_element():
    assert binary_search([1, 3, 5, 7, 9], 9) == 4


def test_middle_element():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2
