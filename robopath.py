#!/usr/bin/env python3
import heapq
import sys
from typing import List, Tuple, Set, Dict, Optional

Point = Tuple[int, int]


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(pt: Point, width: int, height: int) -> List[Point]:
    x, y = pt
    results = []
    if x > 0:
        results.append((x - 1, y))
    if x < width - 1:
        results.append((x + 1, y))
    if y > 0:
        results.append((x, y - 1))
    if y < height - 1:
        results.append((x, y + 1))
    return results


def astar(start: Point, goal: Point, width: int, height: int, blocked: Set[Point]) -> Optional[List[Point]]:
    open_heap: List[Tuple[int, int, Point]] = []
    heapq.heappush(open_heap, (manhattan(start, goal), 0, start))
    came_from: Dict[Point, Optional[Point]] = {start: None}
    gscore: Dict[Point, int] = {start: 0}

    while open_heap:
        _, current_g, current = heapq.heappop(open_heap)
        if current == goal:
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return path

        for nbr in neighbors(current, width, height):
            if nbr in blocked:
                continue
            tentative_g = gscore[current] + 1
            if nbr not in gscore or tentative_g < gscore[nbr]:
                gscore[nbr] = tentative_g
                priority = tentative_g + manhattan(nbr, goal)
                heapq.heappush(open_heap, (priority, tentative_g, nbr))
                came_from[nbr] = current

    return None


def print_grid(width: int, height: int, blocked: Set[Point], path: Optional[List[Point]], start: Point, goal: Point) -> None:
    path_set = set(path or [])
    for y in range(height):
        row = []
        for x in range(width):
            p = (x, y)
            if p == start:
                row.append("S")
            elif p == goal:
                row.append("G")
            elif p in path_set:
                row.append("*")
            elif p in blocked:
                row.append("#")
            else:
                row.append(".")
        print(" ".join(row))


def main(argv: List[str]):
    width, height = 5, 3
    start: Point = (0, 0)
    goal: Point = (4, 2)
    blocked: Set[Point] = {(1, 0), (1, 1), (3, 1)}

    if len(argv) >= 7:
        try:
            width = int(argv[1])
            height = int(argv[2])
            start = (int(argv[3]), int(argv[4]))
            goal = (int(argv[5]), int(argv[6]))
        except Exception:
            pass

    path = astar(start, goal, width, height, blocked)
    print_grid(width, height, blocked, path, start, goal)
    if path:
        print("Path:", path)
    else:
        print("No path found")


if __name__ == "__main__":
    main(sys.argv
