from roman import to_roman


def test_nine_and_forty():
    assert to_roman(9) == "IX"
    assert to_roman(40) == "XL"


def test_ninety_four_hundred_nine_hundred():
    assert to_roman(90) == "XC"
    assert to_roman(400) == "CD"
    assert to_roman(900) == "CM"


def test_big_numbers():
    assert to_roman(1994) == "MCMXCIV"
    assert to_roman(2024) == "MMXXIV"
