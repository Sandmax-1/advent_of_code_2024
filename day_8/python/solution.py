from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x - other.x, self.y - other.y)

    def __rmul__(self, scale_factor: int) -> "Coordinate":
        """scalar mult"""
        return Coordinate(scale_factor * self.x, scale_factor * self.y)

    def __abs__(self) -> int:
        """Implement manhattan distance"""
        return self.x + self.y


def parse_input(
    file_name: str,
) -> tuple[int, int, defaultdict[str, list[Coordinate]], list[list[str]]]:
    nodes: defaultdict[str, list[Coordinate]] = defaultdict(list)
    grid: list[list[str]] = []
    with open(Path().cwd() / "day_8" / "data" / file_name, "r") as f:
        max_y = 0
        max_x = 0
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            grid.append(list(line))
            max_y += 1
            max_x = len(line)
            for x, char in enumerate(line):
                if char != ".":
                    nodes[char].append(Coordinate(x, y))

    return max_x, max_y, nodes, grid


def in_grid(node: Coordinate, max_x: int, max_y: int) -> bool:
    return 0 <= node.x <= max_x - 1 and 0 <= node.y <= max_y - 1


def part_1(
    max_x: int, max_y: int, nodes: defaultdict[str, list[Coordinate]]
) -> set[Coordinate]:
    antinodes: set[Coordinate] = set()
    for _, positions in nodes.items():
        for ind, pos in enumerate(positions):
            for other_pos in positions[ind + 1 :]:
                distance = pos - other_pos
                antinode_positions: list[Coordinate] = [
                    pos + distance,
                    pos + Coordinate(-distance.x, -distance.y),
                    other_pos + distance,
                    other_pos + Coordinate(-distance.x, -distance.y),
                ]

                for antinode_position in antinode_positions:
                    if in_grid(
                        antinode_position, max_x, max_y
                    ) and antinode_position not in (pos, other_pos):
                        antinodes.add(antinode_position)

    return antinodes


def part_2(
    max_x: int, max_y: int, nodes: defaultdict[str, list[Coordinate]]
) -> set[Coordinate]:
    def check_along_line(
        pos: Coordinate,
        other_pos: Coordinate,
        direction: Coordinate,
        antinodes: set[Coordinate],
    ) -> set[Coordinate]:
        scale_factor = 0
        while in_grid((antinode := pos + scale_factor * direction), max_x, max_y):
            scale_factor += 1
            antinodes.add(antinode)
        return antinodes

    antinodes: set[Coordinate] = set()
    for _, positions in nodes.items():
        for ind, pos in enumerate(positions):
            for other_pos in positions[ind + 1 :]:
                distance = pos - other_pos
                antinodes = check_along_line(pos, other_pos, distance, antinodes)
                antinodes = check_along_line(
                    pos, other_pos, Coordinate(-distance.x, -distance.y), antinodes
                )
    return antinodes


def print_grid(grid: list[list[str]]) -> None:
    for line in grid:
        print("".join(line))


if __name__ == "__main__":
    max_x, max_y, nodes, grid = parse_input("actual_input.txt")
    print(max_x, max_y, nodes)

    sol_1 = part_1(max_x, max_y, nodes)
    sol_2 = part_2(max_x, max_y, nodes)

    print(sol_2)
    for pos in sol_2:
        grid[pos.y][pos.x] = "#"

    print_grid(grid)

    print(len(sol_1), len(sol_2))
