from paths import shortest


def test_straight_line():
    assert shortest(["S.G"]) == 2


def test_path_that_goes_left():
    rows = [
        "G#S",
        ".#.",
        "...",
    ]
    assert shortest(rows) == 6
