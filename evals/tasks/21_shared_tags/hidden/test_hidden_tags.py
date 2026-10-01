from tags import add_tag


def test_many_fresh_calls():
    for i in range(3):
        assert add_tag(i) == [i]


def test_explicit_list_is_extended():
    mine = ["x"]
    result = add_tag("y", mine)
    assert result == ["x", "y"]
    assert mine == ["x", "y"]
