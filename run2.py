import sys
import heapq
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
                keys.append((x, y, maze[x][y]))

    return robots, keys


def bfs_from_node_to_other(all_nodes, distances, i, m, maze, n, necessary_keys, node_to_id):
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
            if distances[i][j] > distance:
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


def calculate_distances_and_needed_keys(
        robots: list[tuple[int, int]],
        keys_coords: list[tuple[int, int]],
        n: int, m: int, maze: list[list[str]]):
    all_nodes = robots + keys_coords
    l = len(all_nodes)
    node_to_id = {coord: idx for idx, coord in enumerate(all_nodes)}
    distances = [[float('inf')] * l for _ in range(l)]
    necessary_keys = [[0] * l for _ in range(l)]

    for i in range(l):
        bfs_from_node_to_other(all_nodes, distances, i, m, maze, n, necessary_keys, node_to_id)

    return distances, necessary_keys


def dijkstra(distances, necessary_keys, keys_count, key_symbols):
    robots_count = 4  # в условии написано, что всегда 4 робота

    target_mask = 0
    for symbol in key_symbols:
        target_mask |= (1 << (ord(symbol) - ord('a')))

    start_positions = (0, 1, 2, 3)
    start_mask = 0
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_positions, start_mask))

    visited = {}
    visited_key = (start_positions, start_mask)
    visited[visited_key] = 0

    while priority_queue:
        cur_steps, cur_positions, cur_mask = heapq.heappop(priority_queue)

        if cur_mask == target_mask:
            return cur_steps

        if visited.get((cur_positions, cur_mask), float('inf')) < cur_steps:
            continue

        for robot in range(robots_count):
            current_node = cur_positions[robot]

            for key_node in range(robots_count, robots_count + keys_count):
                symbol = key_symbols[key_node - robots_count]
                bit = ord(symbol) - ord('a')
                if cur_mask & (1 << bit):
                    continue
                required_doors = necessary_keys[current_node][key_node]
                if (required_doors & cur_mask) != required_doors:
                    continue

                new_steps = cur_steps + distances[current_node][key_node]
                new_mask = cur_mask | (1 << bit)
                new_positions = list(cur_positions)
                new_positions[robot] = key_node
                new_positions = tuple(new_positions)
                if new_steps < visited.get((new_positions, new_mask), float('inf')):
                    visited[(new_positions, new_mask)] = new_steps
                    heapq.heappush(priority_queue, (new_steps, new_positions, new_mask))


def solve(maze):
    n, m = len(maze), len(maze[0])
    robots, keys_with_symbol = get_robots_keys_coords(n, m, maze)
    keys_coords = [(x, y) for x, y, _ in keys_with_symbol]
    key_symbols = [symbol for _, _, symbol in keys_with_symbol]
    keys_count = len(keys_coords)
    distances, necessary_keys = calculate_distances_and_needed_keys(robots, keys_coords, n, m, maze)
    shortest_distance = dijkstra(distances, necessary_keys, keys_count, key_symbols)
    return shortest_distance


def main():
    maze = get_input()
    result = solve(maze)
    print(result)


if __name__ == '__main__':
    main()
