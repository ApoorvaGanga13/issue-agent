def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def can_book(existing, new):
    return all(not overlaps(new, booking) for booking in existing)
