from scale import normalize_score

def test_high():
    assert normalize_score(150) == 100

def test_low():
    assert normalize_score(-5) == 0

def test_middle():
    assert normalize_score(50) == 50
