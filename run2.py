import sys
import heapq
from collections import deque

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]
directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}


def get_input() -> list[list[str]]:
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


def bfs_from_node_to_other(all_nodes: list[(int, int)], node_to_id: dict[(int, int), int],
                           i: int, n: int, m: int, maze: list[list[str]],
                           distances: list[list[float | int]], necessary_keys: list[list[int]]) -> None:
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
        n: int, m: int, maze: list[list[str]]) -> (list[list[float | int]], list[list[int]]):
    all_nodes = robots + keys_coords
    nodes_count = len(all_nodes)
    node_to_id = {coord: idx for idx, coord in enumerate(all_nodes)}
    distances = [[float('inf')] * nodes_count for _ in range(nodes_count)]
    necessary_keys = [[0] * nodes_count for _ in range(nodes_count)]

    for i in range(nodes_count):
        bfs_from_node_to_other(all_nodes, node_to_id, i, n, m, maze, distances, necessary_keys)

    return distances, necessary_keys


def dijkstra(distances: list[list[float]], necessary_keys: list[list[int]],
             keys_count: int, key_symbols: list[str]) -> int:
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


def solve(maze) -> int:
    n, m = len(maze), len(maze[0])
    robots, keys_with_symbol = get_robots_keys_coords(n, m, maze)
    keys_coords = [(x, y) for x, y, _ in keys_with_symbol]
    key_symbols = [symbol for _, _, symbol in keys_with_symbol]
    keys_count = len(keys_with_symbol)
    distances, necessary_keys = calculate_distances_and_needed_keys(robots, keys_coords, n, m, maze)
    shortest_distance = dijkstra(distances, necessary_keys, keys_count, key_symbols)
    return shortest_distance


def main():
    maze = get_input()
    result = solve(maze)
    print(result)


if __name__ == '__main__':
    main()
