from collections import deque

from grid import parse

DIRECTIONS = [(1, 0), (-1, 0), (0, 1)]


def shortest(rows):
    walls, start, goal = parse(rows)
    height, width = len(rows), len(rows[0])
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == goal:
            return dist
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            inside = 0 <= nr < height and 0 <= nc < width
            if inside and (nr, nc) not in walls and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    return None
