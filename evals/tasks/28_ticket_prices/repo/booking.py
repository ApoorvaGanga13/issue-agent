from rates import base_price


def total_cents(tickets, discount_percent=0):
    total = 0
    for kind, quantity in tickets:
        total += base_price(kind)
    return total - total * discount_percent // 100
