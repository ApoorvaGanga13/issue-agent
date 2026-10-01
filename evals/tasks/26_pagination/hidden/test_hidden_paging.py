from paging import paginate, total_pages


def test_last_partial_page():
    assert paginate(list(range(10)), 4, 3) == [9]


def test_page_past_the_end():
    assert paginate(list(range(10)), 5, 3) == []


def test_total_pages_rounds_up():
    assert total_pages(10, 3) == 4
    assert total_pages(9, 3) == 3


def test_total_pages_empty():
    assert total_pages(0, 3) == 0
