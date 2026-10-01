def add_item(inv, name, qty):
    inv[name] = qty
    return inv


def remove_item(inv, name, qty):
    inv[name] = inv.get(name, 0) - qty
    return inv
