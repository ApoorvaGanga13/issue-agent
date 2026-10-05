def split_bill(total_cents, n):
    return [total_cents // n] * n


def with_tip(total_cents, tip_percent):
    return total_cents + round(total_cents * tip_percent / 100)
