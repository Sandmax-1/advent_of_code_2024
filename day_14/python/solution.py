from dataclasses import dataclass
from functools import reduce
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            raise NotImplementedError()
        return self.x == other.x and self.y == other.y


def parse_input(file_name: str) -> list[tuple[Coordinate, Coordinate]]:
    robots: list[tuple[Coordinate, Coordinate]] = []
    with open(Path().cwd() / "day_14" / "data" / file_name, "r") as f:
        for line in f.readlines():
            position_str, velocity_str = line.strip().split(" ")
            position, velocity = Coordinate(
                *map(int, position_str.split("=")[1].split(","))
            ), Coordinate(*map(int, velocity_str.split("=")[1].split(",")))
            robots.append((position, velocity))
    return robots


def part_1(robots: list[tuple[Coordinate, Coordinate]]) -> int:
    elapsed_time = 100
    room_width = 101
    room_height = 103

    quadrants = [0, 0, 0, 0]

    for position, velocity in robots:
        robots_new_position = Coordinate(
            (position.x + (velocity.x * elapsed_time)) % room_width,
            (position.y + (velocity.y * elapsed_time)) % room_height,
        )

        if (
            robots_new_position.x == (room_width - 1) / 2
            or robots_new_position.y == (room_height - 1) / 2  # noqa: W503
        ):
            continue
        elif robots_new_position.x > (room_width - 1) / 2:
            if robots_new_position.y > (room_height - 1) / 2:
                quadrants[0] += 1
            else:
                quadrants[1] += 1
        else:
            if robots_new_position.y > (room_height - 1) / 2:
                quadrants[2] += 1
            else:
                quadrants[3] += 1

    return reduce(lambda x, y: x * y, quadrants)


def part_2(robots: list[tuple[Coordinate, Coordinate]]) -> int:
    room_width = 101
    room_height = 103
    elapsed_time = 1

    while elapsed_time < 101 * 103:
        robots_new_positions: set[Coordinate] = set()
        for position, velocity in robots:
            robots_new_positions.add(
                Coordinate(
                    (position.x + (velocity.x * elapsed_time)) % room_width,
                    (position.y + (velocity.y * elapsed_time)) % room_height,
                )
            )

        if len(robots_new_positions) == len(robots):
            break

        elapsed_time += 1

    return elapsed_time


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")

    sol_1 = part_1(inp)
    sol_2 = part_2(inp)

    print(sol_1, sol_2)
