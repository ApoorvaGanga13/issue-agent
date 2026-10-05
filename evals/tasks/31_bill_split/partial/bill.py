def split_bill(total_cents, n):
    base, extra = divmod(total_cents, n)
    return [base + 1 if i < extra else base for i in range(n)]


def with_tip(total_cents, tip_percent):
    return total_cents + round(total_cents * tip_percent / 100)
