def to_roman(n):
    table = [(1000, "M"), (500, "D"), (100, "C"), (50, "L"), (10, "X"), (5, "V"), (1, "I")]
    out = ""
    for value, symbol in table:
        while n >= value:
            out += symbol
            n -= value
    return out
