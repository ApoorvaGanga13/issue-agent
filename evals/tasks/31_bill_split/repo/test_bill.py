from bill import split_bill, with_tip


def test_uneven_split_keeps_every_cent():
    assert split_bill(1001, 3) == [334, 334, 333]


def test_even_split():
    assert split_bill(1000, 4) == [250, 250, 250, 250]


def test_simple_tip():
    assert with_tip(2000, 15) == 2300
