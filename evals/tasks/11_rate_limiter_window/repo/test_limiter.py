from limiter import RateLimiter

def test_sliding_window():
    rl = RateLimiter(limit=2, window=10)
    assert rl.allow(0) is True
    assert rl.allow(1) is True
    assert rl.allow(2) is False
    assert rl.allow(10) is True
    assert rl.allow(11) is True
    assert rl.allow(11.5) is False
