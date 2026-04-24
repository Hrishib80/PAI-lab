import heapq

def water_jug_astar(capacity_x, capacity_y, target):
    # Heuristic function
    def heuristic(x, y):
        return min(abs(x - target), abs(y - target))

    # A* search
    visited = set()
    pq = []

    # (f, g, x, y, path)
    heapq.heappush(pq, (heuristic(0, 0), 0, 0, 0, []))

    while pq:
        f, g, x, y, path = heapq.heappop(pq)

        if (x, y) in visited:
            continue

        visited.add((x, y))
        path = path + [(x, y)]

        # Goal condition
        if x == target or y == target:
            return path

        # Possible operations
        next_states = []

        # Fill X
        next_states.append((capacity_x, y))

        # Fill Y
        next_states.append((x, capacity_y))

        # Empty X
        next_states.append((0, y))

        # Empty Y
        next_states.append((x, 0))

        # Pour X -> Y
        transfer = min(x, capacity_y - y)
        next_states.append((x - transfer, y + transfer))

        # Pour Y -> X
        transfer = min(y, capacity_x - x)
        next_states.append((x + transfer, y - transfer))

        for nx, ny in next_states:
            if (nx, ny) not in visited:
                new_g = g + 1
                new_f = new_g + heuristic(nx, ny)
                heapq.heappush(pq, (new_f, new_g, nx, ny, path))

    return None


# Example usage
capacity_x = 4
capacity_y = 3
target = 2

solution = water_jug_astar(capacity_x, capacity_y, target)

if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution possible.")
