import pytest

from taskgraph import run_order


def test_shared_dependency_runs_once():
    order = run_order({"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []})
    assert sorted(order) == ["a", "b", "c", "d"]
    assert order.index("a") < order.index("b") < order.index("d")
    assert order.index("a") < order.index("c") < order.index("d")


def test_dependency_listed_after_its_dependent():
    assert run_order({"b": ["a"], "a": []}) == ["a", "b"]


def test_cycle_raises_value_error():
    with pytest.raises(ValueError):
        run_order({"a": ["b"], "b": ["a"]})


def test_self_dependency_is_a_cycle():
    with pytest.raises(ValueError):
        run_order({"a": ["a"]})


def test_unknown_dependency_raises_key_error():
    with pytest.raises(KeyError):
        run_order({"a": ["ghost"]})
