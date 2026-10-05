from paths import shortest


def test_unreachable_goal():
    assert shortest(["S#G"]) == -1


def test_open_field():
    assert shortest(["S..", "...", "..G"]) == 4
    assert shortest(["G..", "...", "..S"]) == 4


def test_detour_around_a_wall():
    assert shortest(["S.#G", "..#.", "...."]) == 7


def test_start_next_to_goal():
    assert shortest(["SG"]) == 1
    assert shortest(["GS"]) == 1
