import pytest
from stack import Stack

def test_lifo_order():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2

def test_pop_empty_raises():
    with pytest.raises(IndexError):
        Stack().pop()
