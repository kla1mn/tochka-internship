import json
import heapq


def check_capacity(max_capacity: int, guests: list) -> bool:
    if max_capacity == 0:
        return False
    if len(guests) == 0:
        return True

    guests.sort(key=lambda x: (x['check-out'], x['check-in']))

    queue = []
    for guest in guests:
        if len(queue) != max_capacity:
            heapq.heappush(queue, (guest['check-out'], guest['check-in']))
            continue
        (check_out, _) = heapq.heappop(queue)
        if check_out <= guest['check-in']:
            heapq.heappush(queue, (guest['check-out'], guest['check-in']))
        else:
            return False
    return True


if __name__ == "__main__":
    max_capacity = int(input())
    n = int(input())

    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)

    result = check_capacity(max_capacity, guests)
    print(result)
