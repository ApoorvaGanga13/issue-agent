def split_bill(total_cents, n):
    if n < 1:
        raise ValueError("n must be at least 1")
    base, extra = divmod(total_cents, n)
    return [base + 1 if i < extra else base for i in range(n)]


def with_tip(total_cents, tip_percent):
    return total_cents + (total_cents * tip_percent + 50) // 100
