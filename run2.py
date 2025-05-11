import sys
from collections import deque

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]
directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def get_robots_keys_coords(n: int, m: int, maze: list[list[str]]) -> (list, list):
    robots, keys = list(), list()
    for x in range(n):
        for y in range(m):
            if maze[x][y] == '@':
                robots.append((x, y))
            elif maze[x][y] in keys_char:
                keys.append((x, y))

    return robots, keys


def calculate_distances_and_needed_keys(robots: list[tuple[int, int]], keys: list[tuple[int, int]],
                                        n: int, m: int, maze: list[list[str]]):
    all_nodes = robots + keys
    l = len(all_nodes)
    node_to_id = dict(zip(all_nodes, range(l)))

    distances = [[float('inf')] * l for _ in range(l)]
    necessary_keys = [[float('inf')] * l for _ in range(l)]

    for i in range(l):
        node = all_nodes[i]
        queue = deque([(node[0], node[1], 0, 0)])
        visited = set()
        while queue:
            x, y, distance, doors = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) in all_nodes and (x, y) != node:
                j = node_to_id[(x, y)]
                distances[i][j] = distance
                necessary_keys[i][j] = doors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] != '#':
                    temp = doors
                    if maze[nx][ny] in doors_char:
                        shift = 1 << (ord(maze[nx][ny].lower()) - ord('a'))
                        temp |= shift
                    queue.append((nx, ny, distance + 1, temp))

    return distances, necessary_keys


def solve(maze):
    n, m = len(maze), len(maze[0])
    robots, keys = get_robots_keys_coords(n, m, maze)
    distances_between_nodes, necessary_keys = calculate_distances_and_needed_keys(robots, keys, n, m, maze)



def main():
    maze = get_input()
    result = solve(maze)
    print(result)


if __name__ == '__main__':
    main()
