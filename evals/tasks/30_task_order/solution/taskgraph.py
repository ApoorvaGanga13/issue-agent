def run_order(tasks):
    order = []
    state = {}

    def visit(name):
        if state.get(name) == "done":
            return
        if state.get(name) == "visiting":
            raise ValueError("cycle at " + str(name))
        state[name] = "visiting"
        for dep in tasks[name]:
            visit(dep)
        state[name] = "done"
        order.append(name)

    for name in tasks:
        visit(name)
    return order
