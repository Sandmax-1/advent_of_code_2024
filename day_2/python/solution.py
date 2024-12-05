import os
from pathlib import Path


def parse_input(file_name: str) -> list[tuple[int, ...]]:
    levels: list[tuple[int, ...]] = []
    with open(Path(os.getcwd()) / f"day_2/data/{file_name}", "r") as f:
        for line in f.readlines():
            levels.append(tuple(map(int, line.split(" "))))

    return levels


def part_1(levels: list[tuple[int, ...]]) -> int:
    total_safe = 0
    for level in levels:
        diffs = [level[ind] - level[ind + 1] for ind in range(len(level) - 1)]

        if (
            len(set([diff >= 0 for diff in diffs])) == 1
            and max([abs(diff) for diff in diffs]) <= 3  # noqa: W503
            and 0 not in diffs  # noqa: W503
        ):
            total_safe += 1
    return total_safe


def is_safe(safe_range: range, level: list[int], can_remove: bool) -> bool:
    out = True

    for ind in range(len(level) - 1):
        diff = level[ind + 1] - level[ind]

        if diff not in safe_range:
            if can_remove:
                if ind != 0:
                    out = is_safe(
                        safe_range, [level[ind - 1]] + level[ind + 1 :], False
                    ) or is_safe(
                        safe_range, level[ind - 1 : ind + 1] + level[ind + 2 :], False
                    )
                else:
                    out = is_safe(safe_range, level[1:], False) or is_safe(
                        safe_range, [level[0]] + level[2:], False
                    )
                break
            else:
                out = False
                break
    return out


def part_2(levels: list[tuple[int, ...]]) -> int:
    total_safe = 0

    for level in levels:
        if is_safe(range(1, 4), list(level), True) or is_safe(
            range(-3, 0), list(level), True
        ):
            total_safe += 1
    return total_safe


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")

    sol_1 = part_1(inp)
    sol_2 = part_2(inp)

    print(sol_1, sol_2)
