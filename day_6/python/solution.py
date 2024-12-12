import os
from copy import deepcopy
from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from typing import Counter


@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def parse_input(file_name: str) -> tuple[list[list[str]], Coordinate]:
    start = Coordinate(0, 0)
    grid: list[list[str]] = []
    with open(Path(os.getcwd()) / f"day_6/data/{file_name}", "r") as f:
        for ind, line in enumerate(f.readlines()):
            grid.append(list(line.strip()))
            if "^" in line:
                start = Coordinate(line.index("^"), ind)

    return grid, start


def part_1(grid: list[list[str]], start: Coordinate) -> list[list[str]]:
    directions = cycle(
        [Coordinate(0, -1), Coordinate(1, 0), Coordinate(0, 1), Coordinate(-1, 0)]
    )
    direction = next(directions)
    in_grid = True
    current_pos = start

    while in_grid:
        new_pos = current_pos + direction

        if not (0 <= new_pos.x <= len(grid[0]) - 1 and 0 <= new_pos.y <= len(grid) - 1):
            in_grid = False
            continue

        elif grid[new_pos.y][new_pos.x] == "#":
            direction = next(directions)

        else:
            grid[new_pos.y][new_pos.x] = "X"
            current_pos = new_pos
    # print_grid(grid)

    return grid


def print_grid(grid: list[list[str]]) -> None:
    for line in grid:
        print("".join(line))


def part_2(grid: list[list[str]], start: Coordinate) -> int:
    count = 0
    for y in range(len(grid)):
        print(y)
        for x in range(len(grid[0])):
            if grid[y][x] != "X":
                continue
            new_grid = deepcopy(grid)
            new_grid[y][x] = "#"
            count += move_guard(new_grid, start)

    return count - 1  # -1 to remove starting pos.


def move_guard(grid: list[list[str]], start: Coordinate) -> int:
    directions = cycle(
        [Coordinate(0, -1), Coordinate(1, 0), Coordinate(0, 1), Coordinate(-1, 0)]
    )
    direction = next(directions)
    in_grid = True
    current_pos = start
    visited: set[tuple[Coordinate, Coordinate]] = set([(start, direction)])

    while in_grid:
        new_pos = current_pos + direction
        if (new_pos, direction) in visited:
            return 1

        elif not (
            0 <= new_pos.x <= len(grid[0]) - 1 and 0 <= new_pos.y <= len(grid) - 1
        ):
            in_grid = False
            return 0

        elif grid[new_pos.y][new_pos.x] == "#":
            visited.add((new_pos, direction))
            direction = next(directions)

        else:
            grid[new_pos.y][new_pos.x] = "X"
            current_pos = new_pos
    return 0


if __name__ == "__main__":
    grid, start = parse_input("actual_input.txt")
    # print(grid, start)

    sol_1 = part_1(grid, start)
    sol_2 = part_2(sol_1, start)

    print(sum([Counter(line).get("X", 0) for line in sol_1]), sol_2)
