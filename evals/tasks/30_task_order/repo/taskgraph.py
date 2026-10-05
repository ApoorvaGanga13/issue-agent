def run_order(tasks):
    order = []

    def visit(name):
        for dep in tasks[name]:
            visit(dep)
        order.append(name)

    for name in tasks:
        visit(name)
    return order
