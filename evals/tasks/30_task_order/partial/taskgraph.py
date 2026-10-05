def run_order(tasks):
    order = []
    seen = set()

    def visit(name):
        if name in seen:
            return
        seen.add(name)
        for dep in tasks[name]:
            visit(dep)
        order.append(name)

    for name in tasks:
        visit(name)
    return order
