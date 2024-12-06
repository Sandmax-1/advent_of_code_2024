import os
from pathlib import Path


def parse_input(file_name: str) -> tuple[dict[int, list[int]], list[list[int]]]:
    is_page_numbers = False
    orderings: list[list[int]] = []
    page_numbers: list[list[int]] = []
    with open(Path(os.getcwd()) / f"day_5/data/{file_name}", "r") as f:
        for line in f.readlines():
            if not is_page_numbers:
                if not line.strip():
                    is_page_numbers = True
                else:
                    orderings.append(list(map(int, map(str.strip, line.split("|")))))
            else:
                page_numbers.append(list(map(int, map(str.strip, line.split(",")))))

    before_map: dict[int, list[int]] = {}

    for ordering in orderings:
        before = before_map.get(ordering[0], [])
        before.append(ordering[1])
        before_map[ordering[0]] = before

    return before_map, page_numbers


def part_1(before_map: dict[int, list[int]], page_numbers: list[list[int]]) -> int:
    valid_numbers: list[list[int]] = []
    for page_number in page_numbers:
        is_valid = True
        for ind, num in enumerate(page_number):
            if not is_valid:
                break
            before = before_map.get(num, [])

            for b in before:
                if b in page_number[:ind]:
                    is_valid = False
                    break
        if is_valid:
            valid_numbers.append(page_number)

    return sum([valid_number[len(valid_number) // 2] for valid_number in valid_numbers])


def part_2(before_map: dict[int, list[int]], page_numbers: list[list[int]]) -> int:
    invalid_numbers: list[list[int]] = []
    for page_number in page_numbers:
        is_valid = True
        for ind, num in enumerate(page_number):
            if not is_valid:
                break
            before = before_map.get(num, [])

            for b in before:
                if b in page_number[:ind]:
                    is_valid = False
                    break
        if not is_valid:
            invalid_numbers.append(page_number)

    fixed_numbers: list[list[int]] = []
    for page_number in invalid_numbers:
        is_valid = False
        while not is_valid:
            page_number, is_valid = check_valid(list(page_number), before_map)
        fixed_numbers.append(page_number)

    return sum([valid_number[len(valid_number) // 2] for valid_number in fixed_numbers])


def check_valid(
    numbers: list[int], orderings: dict[int, list[int]]
) -> tuple[list[int], bool]:
    for ind, num in enumerate(numbers):
        before = orderings.get(num, [])

        bad_positions: list[int] = []
        for b in before:
            if b in numbers[:ind]:
                bad_positions.append(numbers.index(b))
        if bad_positions:
            min_bad_pos = min(bad_positions)
            numbers[ind], numbers[min_bad_pos] = numbers[min_bad_pos], numbers[ind]
            return numbers, False
    return numbers, True


if __name__ == "__main__":
    orderings, page_numbers = parse_input("actual_input.txt")

    sol_1 = part_1(orderings, page_numbers)
    sol_2 = part_2(orderings, page_numbers)

    print(sol_1, sol_2)
