import pytest
from inventory import add_item, remove_item

def test_add_accumulates():
    inv = {}
    add_item(inv, "apple", 2)
    add_item(inv, "apple", 3)
    assert inv["apple"] == 5

def test_remove_to_zero_deletes_item():
    inv = {"apple": 2}
    remove_item(inv, "apple", 2)
    assert "apple" not in inv

def test_remove_too_many_raises():
    inv = {"apple": 1}
    with pytest.raises(ValueError):
        remove_item(inv, "apple", 5)
