from bill import split_bill, with_tip


def per_person(total_cents, tip_percent, n):
    return split_bill(with_tip(total_cents, tip_percent), n)
