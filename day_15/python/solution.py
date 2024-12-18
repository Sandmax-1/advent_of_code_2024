from collections import deque
from collections.abc import Iterable
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            raise NotImplementedError()
        return self.x == other.x and self.y == other.y


ARROW_MAP = {
    ">": Coordinate(1, 0),
    "v": Coordinate(0, 1),
    "<": Coordinate(-1, 0),
    "^": Coordinate(0, -1),
}


def parse_input(
    file_name: str,
) -> tuple[str, Coordinate, list[Coordinate], Coordinate, set[Coordinate]]:
    box_positions: list[Coordinate] = []
    direction_str = ""
    walls: set[Coordinate] = set()
    with open(Path().cwd() / "day_15" / "data" / file_name, "r") as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            if y == 0:
                max_x = len(line) - 1

            if not line:
                max_y = y - 1
                continue

            if line[0] in ARROW_MAP.keys():
                direction_str += line
                continue

            for x, char in enumerate(line):
                if char == "#":
                    walls.add(Coordinate(x, y))
                elif char == "@":
                    robot_initial_pos = Coordinate(x, y)
                elif char == "O":
                    box_positions.append(Coordinate(x, y))

    max_dims = Coordinate(max_x, max_y)

    return direction_str, robot_initial_pos, box_positions, max_dims, walls


def parse_input_part_2(
    file_name: str,
) -> tuple[
    str,
    Coordinate,
    list[tuple[Coordinate, Coordinate]],
    Coordinate,
    set[tuple[Coordinate, Coordinate]],
]:
    box_positions: list[tuple[Coordinate, Coordinate]] = []
    direction_str = ""
    walls: set[tuple[Coordinate, Coordinate]] = set()
    with open(Path().cwd() / "day_15" / "data" / file_name, "r") as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            if y == 0:
                max_x = 2 * (len(line) - 1)

            if not line:
                max_y = y - 1
                continue

            if line[0] in ARROW_MAP.keys():
                direction_str += line
                continue

            for x, char in enumerate(line):
                if char == "#":
                    walls.add((Coordinate(2 * x, y), Coordinate(2 * x + 1, y)))
                elif char == "@":
                    robot_initial_pos = Coordinate(2 * x, y)
                elif char == "O":
                    box_positions.append(
                        (Coordinate(2 * x, y), Coordinate(2 * x + 1, y))
                    )

    max_dims = Coordinate(max_x, max_y)
    return direction_str, robot_initial_pos, box_positions, max_dims, walls


def in_grid(pos: Coordinate, max_dims: Coordinate) -> bool:
    return 0 < pos.x < max_dims.x and 0 < pos.y < max_dims.y


def part_1(
    directions: str,
    robot_pos: Coordinate,
    boxes: list[Coordinate],
    max_dims: Coordinate,
    walls: set[Coordinate],
) -> int:
    def move_robot(
        robot_pos: Coordinate, direction: Coordinate, boxes: list[Coordinate]
    ) -> tuple[Coordinate, list[Coordinate]]:
        new_robot_pos = robot_pos + direction
        if not in_grid(new_robot_pos, max_dims) or new_robot_pos in walls:
            return robot_pos, boxes

        if new_robot_pos not in boxes:
            return new_robot_pos, boxes

        else:
            indexes: list[int] = []
            indexes.append(boxes.index(new_robot_pos))

            next_box_pos = new_robot_pos + direction

            while next_box_pos in boxes:
                indexes.append(boxes.index(next_box_pos))
                next_box_pos += direction

            if not in_grid(next_box_pos, max_dims) or next_box_pos in walls:
                return robot_pos, boxes

            else:
                for ind in indexes:
                    boxes[ind] = boxes[ind] + direction
                return new_robot_pos, boxes

    for direction in directions:
        robot_pos, boxes = move_robot(robot_pos, ARROW_MAP[direction], boxes)
        # print('\n')
        # print_grid(robot_pos, boxes, walls, max_dims)

    return sum((box.x + box.y * 100 for box in boxes))


def part_2(
    directions: str,
    robot_pos: Coordinate,
    boxes: list[tuple[Coordinate, Coordinate]],
    max_dims: Coordinate,
    walls: set[tuple[Coordinate, Coordinate]],
) -> int:
    def check_pos_in_tuples(
        pos: Coordinate, iterator_to_check: Iterable[tuple[Coordinate, Coordinate]]
    ) -> list[int]:
        inds: list[int] = []
        for ind, (coord_1, coord_2) in enumerate(iterator_to_check):
            if pos == coord_1 or pos == coord_2:
                inds.append(ind)

        return inds

    def move_robot(
        robot_pos: Coordinate,
        direction: Coordinate,
        boxes: list[tuple[Coordinate, Coordinate]],
    ) -> tuple[Coordinate, list[tuple[Coordinate, Coordinate]]]:
        new_robot_pos = robot_pos + direction
        if check_pos_in_tuples(new_robot_pos, walls):
            return robot_pos, boxes

        if not (box_indicies := check_pos_in_tuples(new_robot_pos, boxes)):
            return new_robot_pos, boxes

        else:
            indexes: set[int] = set()
            for ind in box_indicies:
                indexes.add(ind)

            next_box_positions: deque[tuple[Coordinate, Coordinate]] = deque(
                [
                    (boxes[box_index][0] + direction, boxes[box_index][1] + direction)
                    for box_index in box_indicies
                ]
            )
            next_box_pos = next_box_positions.popleft()
            inds_1 = check_pos_in_tuples(next_box_pos[0], boxes)
            inds_2 = check_pos_in_tuples(next_box_pos[1], boxes)
            while next_box_positions or inds_1 or inds_2:
                if check_pos_in_tuples(next_box_pos[0], walls) or check_pos_in_tuples(
                    next_box_pos[1], walls
                ):
                    return robot_pos, boxes
                inds = set(inds_1 + inds_2)
                inds = inds.difference(indexes)
                indexes.update(inds)
                next_box_positions.extend(
                    [
                        (boxes[ind][0] + direction, boxes[ind][1] + direction)
                        for ind in inds
                    ]
                )
                if next_box_positions:
                    next_box_pos = next_box_positions.popleft()
                inds_1 = list(
                    set(check_pos_in_tuples(next_box_pos[0], boxes)).difference(indexes)
                )
                inds_2 = list(
                    set(check_pos_in_tuples(next_box_pos[1], boxes)).difference(indexes)
                )

            if check_pos_in_tuples(next_box_pos[0], walls) or check_pos_in_tuples(
                next_box_pos[1], walls
            ):
                return robot_pos, boxes

            else:
                for ind in indexes:
                    boxes[ind] = (boxes[ind][0] + direction, boxes[ind][1] + direction)
                return new_robot_pos, boxes

    for direction in directions:
        robot_pos, boxes = move_robot(robot_pos, ARROW_MAP[direction], boxes)

    return sum(
        (
            min(box_tuple[0].x, box_tuple[1].x) + box_tuple[0].y * 100
            for box_tuple in boxes
        )
    )


def print_grid(
    robot_pos: Coordinate,
    boxes: list[Coordinate],
    walls: set[Coordinate],
    max_dims: Coordinate,
) -> None:
    grid: list[list[str]] = []
    for _ in range(max_dims.y + 1):
        grid.append(list("." * (max_dims.x + 1)))

    for box in boxes:
        grid[box.y][box.x] = "O"
    for wall in walls:
        grid[wall.y][wall.x] = "#"
    grid[robot_pos.y][robot_pos.x] = "@"

    for line in grid:
        print("".join(line))


def print_grid_part_2(
    robot_pos: Coordinate,
    boxes: list[tuple[Coordinate, Coordinate]],
    walls: set[tuple[Coordinate, Coordinate]],
    max_dims: Coordinate,
) -> None:
    grid: list[list[str]] = []
    for _ in range(max_dims.y + 1):
        grid.append(list("." * (max_dims.x + 2)))

    for box in boxes:
        grid[box[0].y][box[0].x] = "["
        grid[box[1].y][box[1].x] = "]"
    for wall in walls:
        grid[wall[0].y][wall[0].x] = "#"
        grid[wall[1].y][wall[1].x] = "#"
    grid[robot_pos.y][robot_pos.x] = "@"

    for line in grid:
        print("".join(line))


if __name__ == "__main__":
    # directions, robot_initial_pos, box_positions, max_dims, walls = parse_input(
    #     "test_input.txt"
    # )

    # print_grid(robot_initial_pos, box_positions, walls, max_dims)

    # sol_1 = part_1(directions, robot_initial_pos, box_positions, max_dims, walls)

    directions, robot_initial_pos, box_positions, max_dims, walls = parse_input_part_2(
        "test_input.txt"
    )

    print_grid_part_2(robot_initial_pos, box_positions, walls, max_dims)

    sol_2 = part_2(directions, robot_initial_pos, box_positions, max_dims, walls)

    print(sol_2)
