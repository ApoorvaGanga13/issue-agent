# Task order

`run_order(tasks)` takes a dict that maps each task name to the list of tasks
it depends on, and returns the task names in the order they can run.

- A task always comes after the tasks it depends on.
- Every task appears exactly once, even when several tasks depend on it.
- Tasks that do not depend on each other keep the order of the dict.
- A cycle raises ValueError.
- A dependency that is not a key of the dict raises KeyError.
