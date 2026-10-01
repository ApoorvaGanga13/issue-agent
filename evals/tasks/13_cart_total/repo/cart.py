from pricing import apply_discount


class Cart:
    def __init__(self, discount_percent=0):
        self.items = []
        self.discount_percent = discount_percent

    def add(self, name, price, qty=1):
        self.items.append({"name": name, "price": price, "qty": qty})

    def total(self):
        total = sum(item["price"] for item in self.items)
        return round(apply_discount(total, self.discount_percent), 2)
