import json


def check_capacity(max_capacity: int, guests: list) -> bool:
    """
    Проверяет, можно ли разместить всех гостей в отеле.

    :param max_capacity: Максимальная вместимость отеля.
    :param guests: Список словарей с данными о гостях, каждый словарь должен содержать
                    ключи 'check-in' и 'check-out' с датами в строковом формате.
    :return: True, если все гости могут быть размещены, иначе False.
    """
    if max_capacity == 0:
        return False
    if not guests:
        return True

    ins_and_outs: list[tuple[str, str]] = []
    for guest in guests:
        ins_and_outs.append((guest["check-in"], "in"))
        ins_and_outs.append((guest["check-out"], "out"))

    ins_and_outs.sort(key=lambda x: (x[0], x[1] == "in"))

    guests_count = 0
    for _, check_type in ins_and_outs:
        if check_type == "in":
            guests_count += 1
            if guests_count > max_capacity:
                return False
        else:
            guests_count -= 1
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
