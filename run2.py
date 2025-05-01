import sys
import collections
import heapq

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]
directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def get_keys_doors_robots_coord(n: int, m: int, maze: list[list[str]]) -> (list, list):
    keys, robots = list(), set()
    for x in range(n):
        for y in range(m):
            if maze[x][y] in keys_char:
                keys.append((maze[x][y], (x, y)))
            elif maze[x][y] == "@":
                robots.add((x, y))

    return keys, robots


def heuristic(x1, y1, x2, y2):
    return max(abs(x1 - x2), abs(y1 - y2))


def find_best_way_len_from_a_to_b(a: (int, int), b: (int, int), n: int, m: int,
                                  maze: list[list[str]], allowed_keys: list[str], allowed_doors: list[str]) -> int:
    visited = set()
    queue = []
    heapq.heappush(queue, (0, 0, a))
    while queue:
        priority, length, (curr_x, curr_y) = heapq.heappop(queue)
        if (curr_x, curr_y) in visited:
            continue
        visited.add((curr_x, curr_y))
        if (curr_x, curr_y) == b:
            return length
        for dx, dy in directions:
            x, y = curr_x + dx, curr_y + dy
            if (0 <= x < n and 0 <= y < m and (x, y) not in visited and
                    (maze[x][y] == "." or maze[x][y] in allowed_doors or maze[x][y] in allowed_keys)):
                h = heuristic(x, y, b[0], b[1])
                p = length + 1 + h
                heapq.heappush(queue, (p, length + 1, (x, y)))
    return -1


def solve(maze):
    n, m = len(maze), len(maze[0])
    keys, robots = get_keys_doors_robots_coord(n, m, maze)
    keys.sort()
    allowed_keys = []
    allowed_doors = []
    sum = 0
    for key, (x, y) in keys:
        allowed_keys.append(key)
        min_len = float('inf')
        for robot in robots:
            l = find_best_way_len_from_a_to_b(robot, (x, y), n, m, maze, allowed_keys, allowed_doors)
            print(f"from {robot} to {(x, y), key} len {l}")
            if l != -1:
                min_len = min(min_len, l)
        sum += min_len
        allowed_doors.append(key.upper())
    return sum


def main():
    maze = get_input()
    result = solve(maze)
    print(result)


if __name__ == '__main__':
    main()
