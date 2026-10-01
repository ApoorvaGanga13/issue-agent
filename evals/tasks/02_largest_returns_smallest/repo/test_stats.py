from stats import largest

def test_largest():
    assert largest([3, 9, 2]) == 9

def test_largest_negative():
    assert largest([-5, -2, -9]) == -2
