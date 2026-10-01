from config import merge


def test_nested_override():
    defaults = {"db": {"host": "localhost", "port": 5432}, "debug": False}
    result = merge(defaults, {"db": {"port": 6543}})
    assert result == {"db": {"host": "localhost", "port": 6543}, "debug": False}
