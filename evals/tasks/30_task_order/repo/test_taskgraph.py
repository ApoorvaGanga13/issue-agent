from taskgraph import run_order


def test_chain():
    assert run_order({"a": [], "b": ["a"], "c": ["b"]}) == ["a", "b", "c"]


def test_independent_tasks_keep_dict_order():
    assert run_order({"x": [], "y": []}) == ["x", "y"]
