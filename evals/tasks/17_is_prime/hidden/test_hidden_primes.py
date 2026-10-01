from primes import is_prime


def test_small_numbers():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True


def test_perfect_squares():
    assert is_prime(25) is False
    assert is_prime(49) is False


def test_larger():
    assert is_prime(97) is True
    assert is_prime(91) is False
