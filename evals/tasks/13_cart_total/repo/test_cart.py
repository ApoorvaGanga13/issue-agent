from cart import Cart


def test_discount_applied():
    cart = Cart(discount_percent=10)
    cart.add("pen", 10.0)
    assert cart.total() == 9.0
