from cart import Cart


def test_quantities():
    cart = Cart()
    cart.add("a", 10.0, qty=2)
    cart.add("b", 5.0)
    assert cart.total() == 25.0


def test_discount_with_quantities():
    cart = Cart(discount_percent=20)
    cart.add("a", 10.0, qty=3)
    assert cart.total() == 24.0


def test_empty_cart():
    assert Cart().total() == 0
