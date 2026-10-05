def nights(booking):
    return booking[1] - booking[0] + 1


def total_nights(bookings):
    return sum(nights(booking) for booking in bookings)
