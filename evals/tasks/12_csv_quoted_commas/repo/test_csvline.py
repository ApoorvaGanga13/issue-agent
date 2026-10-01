from csvline import parse_line

def test_simple():
    assert parse_line("a,b,c") == ["a", "b", "c"]

def test_empty_fields():
    assert parse_line("x,,z") == ["x", "", "z"]

def test_quoted_comma():
    assert parse_line('a,"b,c",d') == ["a", "b,c", "d"]
