from functools import lru_cache
from pathlib import Path


def parse_input(file_name: str) -> list[int]:
    with open(Path().cwd() / "day_11" / "data" / file_name, "r") as f:
        stones = list(map(int, f.read().strip().split(" ")))
    return stones


def part_1(stones: list[int]) -> int:
    def blink(stones: list[int]) -> list[int]:
        new_stones: list[int] = []

        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len((stone_str := str(stone))) % 2 == 0:
                stone_len = len(stone_str)
                new_stones.append(int(stone_str[: stone_len // 2]))
                new_stones.append(int(stone_str[stone_len // 2 :]))

            else:
                new_stones.append(stone * 2024)
        return new_stones

    for _ in range(25):
        stones = blink(stones)
        # print(stones)

    return len(stones)


def part_2(stones: list[int]) -> int:
    @lru_cache(maxsize=None)
    def blink_stone(stone: int, remaining_blinks: int) -> int:
        if remaining_blinks == 0:
            return 1

        if stone == 0:
            return blink_stone(1, remaining_blinks - 1)

        elif len((stone_str := str(stone))) % 2 == 0:
            stone_len = len(stone_str)
            return blink_stone(
                int(stone_str[: stone_len // 2]), remaining_blinks - 1
            ) + blink_stone(int(stone_str[stone_len // 2 :]), remaining_blinks - 1)

        else:
            return blink_stone(stone * 2024, remaining_blinks - 1)

    total = 0
    for stone in stones:
        total += blink_stone(stone, 75)

    return total


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")
    print(inp)
    sol_1 = part_1(inp)
    sol_2 = part_2(inp)

    print(sol_1, sol_2)
