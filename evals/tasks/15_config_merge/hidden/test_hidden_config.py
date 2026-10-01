from config import merge


def test_defaults_not_mutated():
    defaults = {"a": {"x": 1}}
    merge(defaults, {"a": {"x": 2}})
    assert defaults == {"a": {"x": 1}}


def test_three_levels():
    d = {"a": {"b": {"c": 1, "d": 2}}}
    assert merge(d, {"a": {"b": {"c": 9}}}) == {"a": {"b": {"c": 9, "d": 2}}}


def test_new_keys():
    assert merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
