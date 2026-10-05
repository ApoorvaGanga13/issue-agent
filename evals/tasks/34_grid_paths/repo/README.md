# Grid paths

A grid is a list of strings. `#` is a wall, `.` is open floor, `S` is the
start, and `G` is the goal. There is exactly one `S` and one `G`.

`shortest(rows)` returns the fewest steps from `S` to `G`. A step moves one
cell up, down, left or right, never diagonally and never through a wall.
When there is no path it returns -1.
