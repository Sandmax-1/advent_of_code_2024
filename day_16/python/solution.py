import heapq
from collections import defaultdict
from copy import deepcopy
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

    def __lt__(self, other: "Coordinate") -> bool:
        """just being used for heapq and not really that important"""
        return self.x < other.x


def parse_input(
    file_name: str,
) -> tuple[
    set[Coordinate],
    Coordinate,
    Coordinate,
    Coordinate,
    defaultdict[Coordinate, list[tuple[Coordinate, int, Coordinate]]],
]:
    walls: set[Coordinate] = set()
    empty_space: set[Coordinate] = set()
    start_pos, end_pos, max_x, y = Coordinate(0, 0), Coordinate(0, 0), 0, 0
    with open(Path().cwd() / "day_16" / "data" / file_name, "r") as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            max_x = len(line)
            for x, char in enumerate(line):
                if char == "#":
                    walls.add(Coordinate(x, y))

                elif char == "E":
                    end_pos = Coordinate(x, y)

                elif char == "S":
                    start_pos = Coordinate(x, y)

                elif char == ".":
                    empty_space.add(Coordinate(x, y))

    max_dims = Coordinate(max_x, y)

    vertices: list[Coordinate] = []
    directions = [
        Coordinate(1, 0),
        Coordinate(0, 1),
        Coordinate(-1, 0),
        Coordinate(0, -1),
    ]
    empty_space.update([start_pos, end_pos])
    for space in empty_space:
        empty_dirs: list[Coordinate] = []
        for direction in directions:
            if space + direction in empty_space:
                empty_dirs.append(direction)
        if empty_dirs != [Coordinate(1, 0), Coordinate(-1, 0)] and empty_dirs != [
            Coordinate(0, 1),
            Coordinate(0, -1),
        ]:
            vertices.append(space)

    adjacency_map: defaultdict[
        Coordinate, list[tuple[Coordinate, int, Coordinate]]
    ] = defaultdict(list)

    for ind, vertex in enumerate(vertices):
        for next_vertex in deepcopy(vertices[ind + 1 :]):
            direction = vertex - next_vertex
            if direction.x == 0 or direction.y == 0:
                distance = abs(direction.x + direction.y)
                direction = Coordinate(
                    int(direction.x / distance),
                    int(direction.y / distance),
                )
                if direction not in directions:
                    raise Exception
                cur_pos = vertex - direction

                while cur_pos != next_vertex:
                    if cur_pos in walls:
                        break
                    cur_pos = cur_pos - direction
                if cur_pos == next_vertex:
                    adjacency_map[vertex].append((next_vertex, distance, direction))
                    adjacency_map[next_vertex].append(
                        (vertex, distance, Coordinate(-direction.x, -direction.y))
                    )

    return walls, start_pos, end_pos, max_dims, adjacency_map


def print_grid(
    walls: set[Coordinate],
    start_pos: Coordinate,
    end_pos: Coordinate,
    max_dims: Coordinate,
    verticies: set[Coordinate],
) -> None:
    grid: list[list[str]] = []
    for _ in range(max_dims.y + 1):
        grid.append(list("." * max_dims.x))

    for wall in walls:
        grid[wall.y][wall.x] = "#"

    for vertex in verticies:
        grid[vertex.y][vertex.x] = "O"

    grid[start_pos.y][start_pos.x] = "S"
    grid[end_pos.y][end_pos.x] = "E"

    print("\n")
    for line in grid:
        print("".join(line))


def part_1(
    walls: set[Coordinate],
    start_pos: Coordinate,
    end_pos: Coordinate,
    adjacency_map: dict[Coordinate, list[tuple[Coordinate, int, Coordinate]]],
) -> tuple[int, set[Coordinate]]:
    visited: set[Coordinate] = set()
    inds = {node: ind for ind, node in enumerate(adjacency_map.keys())}
    heap = [(0, start_pos, Coordinate(1, 0), str(inds[start_pos]))]
    heapq.heapify(heap)

    distances = {node: 1e10 for node in adjacency_map.keys()}
    distances[start_pos] = 0

    while heap:
        score, pos, current_direction, path = heapq.heappop(heap)
        if pos == end_pos:
            return score, visited
        if pos in visited:
            continue
        visited.add(pos)

        for vertex, distance, direction in adjacency_map[pos]:
            if vertex not in visited:
                if direction == current_direction:
                    heapq.heappush(
                        heap,
                        (
                            score + distance,
                            vertex,
                            direction,
                            path + f"-{inds[vertex]}",
                        ),
                    )

                else:
                    heapq.heappush(
                        heap,
                        (
                            score + 1000 + distance,
                            vertex,
                            direction,
                            path + f"-{inds[vertex]}",
                        ),
                    )

    return 0, {Coordinate(0, 0)}


def part_2(
    start_pos: Coordinate,
    end_pos: Coordinate,
    adjacency_map: dict[Coordinate, list[tuple[Coordinate, int, Coordinate]]],
) -> tuple[set[str], set[Coordinate]]:
    visited: dict[tuple[Coordinate, Coordinate], int] = {}
    inds = {node: ind for ind, node in enumerate(adjacency_map.keys())}
    heap = [(0, start_pos, Coordinate(1, 0), str(inds[start_pos]))]
    heapq.heapify(heap)

    distances = {node: 1e10 for node in adjacency_map.keys()}
    distances[start_pos] = 0
    paths: list[tuple[int, str]] = []
    highscore = 10000000

    counter = 0
    while heap:
        counter += 1
        if counter % 100000 == 0:
            print(len(heap))
        score, pos, current_direction, path = heapq.heappop(heap)
        if (pos, current_direction) in visited and score > visited[
            (pos, current_direction)
        ]:
            continue
        if score > highscore:
            break

        if pos == end_pos:
            highscore = score
            paths.append((score, path))
        visited[(pos, current_direction)] = score

        for vertex, distance, direction in adjacency_map[pos]:
            if (vertex, direction) not in visited:
                new_path = path + f"-{inds[vertex]}"
                if direction == current_direction:
                    # distances[vertex] = min(distances[vertex], score + distance)
                    heapq.heappush(
                        heap,
                        (
                            score + distance,
                            vertex,
                            direction,
                            new_path,
                        ),
                    )

                else:
                    # distances[vertex] = min(distances[vertex], score + 1000 + distance)
                    heapq.heappush(
                        heap,
                        (
                            score + 1000 + distance,
                            vertex,
                            direction,
                            new_path,
                        ),
                    )

    best_score = min([path[0] for path in paths])
    print(best_score)

    visited_tiles: set[Coordinate] = set()
    reversed_inds = {ind: node for node, ind in inds.items()}
    for score, path in paths:
        # print(path)
        path = [reversed_inds[ind] for ind in list(map(int, path.split("-")))]
        if score != best_score:
            continue

        else:
            directions = [(path[ind] - path[ind + 1]) for ind in range(len(path) - 1)]
            distances = [abs(direction.x + direction.y) for direction in directions]
            normalised_directions = [
                Coordinate(
                    int(directions[ind].x / distances[ind]),
                    int(directions[ind].y / distances[ind]),
                )
                for ind in range(len(directions))
            ]
            visited_2: set[Coordinate] = set()
            for ind in range(len(path) - 1):
                start_vertex = path[ind]
                for multiple in range(distances[ind]):
                    visited_2.add(start_vertex - multiple * normalised_directions[ind])
            visited_tiles.update(visited_2)
    print(len(visited_tiles))

    a: set[str] = set()
    for score, path in paths:
        if score == best_score:
            a.update(path)

    return a, visited_tiles


if __name__ == "__main__":
    walls, start_pos, end_pos, max_dims, adjacency_map = parse_input("actual_input.txt")
    # print_grid(walls, start_pos, end_pos, max_dims, set())
    # print_grid(walls, start_pos, end_pos, max_dims, set(adjacency_map.keys()))
    # start = time()
    # sol_1, visited = part_1(walls, start_pos, end_pos, adjacency_map)
    # end = time()
    # print(end - start)
    # print(sol_1)

    print("input_done")

    # start = time()
    a, paths = part_2(start_pos, end_pos, adjacency_map)
    # end = time()
    # print(end - start)
    # # print(paths)
    # print_grid(walls, start_pos, end_pos, max_dims, paths)
    # print_grid(walls, start_pos, end_pos, max_dims, a)
    # print(sol_2)
