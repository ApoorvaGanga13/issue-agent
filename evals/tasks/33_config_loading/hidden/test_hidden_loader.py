import pytest

from loader import load


def test_defaults_when_nothing_is_set():
    assert load({}) == {"port": 8080, "debug": False, "workers": 2, "name": "app"}


def test_calls_do_not_leak_into_each_other():
    load({"APP_PORT": "1", "APP_NAME": "x"})
    assert load({})["port"] == 8080
    assert load({})["name"] == "app"


def test_returned_dict_is_a_copy():
    config = load({})
    config["port"] = 1
    assert load({})["port"] == 8080


def test_boolean_values():
    assert load({"APP_DEBUG": "TRUE"})["debug"] is True
    assert load({"APP_DEBUG": " yes "})["debug"] is True
    assert load({"APP_DEBUG": "1"})["debug"] is True
    assert load({"APP_DEBUG": "no"})["debug"] is False
    assert load({"APP_DEBUG": "0"})["debug"] is False


def test_integer_values():
    assert load({"APP_WORKERS": "4"})["workers"] == 4


def test_bad_integer_raises():
    with pytest.raises(ValueError):
        load({"APP_PORT": "abc"})


def test_unknown_variables_are_ignored():
    assert load({"APP_COLOR": "red", "OTHER": "1"}) == load({})
