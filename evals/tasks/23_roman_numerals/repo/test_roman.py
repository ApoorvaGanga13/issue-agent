from roman import to_roman


def test_basic():
    assert to_roman(3) == "III"
    assert to_roman(58) == "LVIII"


def test_four():
    assert to_roman(4) == "IV"
