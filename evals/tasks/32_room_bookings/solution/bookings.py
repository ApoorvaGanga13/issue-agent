def _check(booking):
    if booking[1] <= booking[0]:
        raise ValueError("a booking must end after it starts")


def overlaps(a, b):
    _check(a)
    _check(b)
    return a[0] < b[1] and b[0] < a[1]


def can_book(existing, new):
    _check(new)
    return all(not overlaps(new, booking) for booking in existing)
