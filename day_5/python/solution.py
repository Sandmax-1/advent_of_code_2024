import os
from pathlib import Path


def parse_input(file_name: str) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    is_page_numbers = False
    orderings: list[tuple[int, ...]] = []
    page_numbers: list[tuple[int, ...]] = []
    with open(Path(os.getcwd()) / f"day_5/data/{file_name}", "r") as f:
        for line in f.readlines():
            if not is_page_numbers:
                if not line.strip():
                    is_page_numbers = True
                else:
                    orderings.append(tuple(map(int, map(str.strip, line.split("|")))))

            else:
                page_numbers.append(tuple(map(int, map(str.strip, line.split(",")))))

    return orderings, page_numbers


def part_1(
    orderings: list[tuple[int, ...]], page_numbers: list[tuple[int, ...]]
) -> int:
    before_map: dict[int, list[int]] = {}

    for ordering in orderings:
        before = before_map.get(ordering[0], [])
        before.append(ordering[1])
        before_map[ordering[0]] = before

    valid_numbers: list[tuple[int, ...]] = []
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


if __name__ == "__main__":
    orderings, page_numbers = parse_input("test_input.txt")

    sol_1 = part_1(orderings, page_numbers)

    print(sol_1)
