from primes import is_prime


def test_composites():
    assert is_prime(9) is False
    assert is_prime(4) is False


def test_primes():
    assert is_prime(7) is True
    assert is_prime(13) is True
