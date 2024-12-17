from pathlib import Path

# flake8: noqa: W503


def parse_input(file_name: str) -> list[str]:
    grid: list[str] = []
    with open(Path().cwd() / "day_12" / "data" / file_name, "r") as f:
        for line in f.readlines():
            grid.append(line.strip())
    return grid


def in_grid(x: int, y: int, max_x: int, max_y: int) -> bool:
    return 0 <= x <= max_x - 1 and 0 <= y <= max_y - 1


def part_1(grid: list[str]) -> int:
    visited: set[tuple[int, int]] = set()
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0))
    max_x, max_y = len(grid[0]), len(grid)

    def find_region(x: int, y: int) -> int:
        possible_region: list[tuple[int, int]] = [(x, y)]
        val = grid[y][x]
        area, perimeter = 0, 0

        while possible_region:
            x, y = possible_region.pop()
            if (x, y) in visited:
                continue
            area += 1
            visited.add((x, y))

            connected_of_same_type_count = 0
            for direction in directions:
                new_x, new_y = x + direction[0], y + direction[1]

                if in_grid(new_x, new_y, max_x, max_y):
                    if grid[new_y][new_x] == val:
                        possible_region.append((new_x, new_y))
                        connected_of_same_type_count += 1
            perimeter += 4 - connected_of_same_type_count

        return area * perimeter

    total_score = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            total_score += find_region(x, y)

    return total_score


def part_2(grid: list[str]) -> int:
    visited: set[tuple[int, int]] = set()
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    max_x, max_y = len(grid[0]), len(grid)

    def check_corner_and_edge_of_grid(
        connected: list[tuple[int, int]],
        diagonal: tuple[int, int],
        x: int,
        y: int,
        val: str,
    ) -> int:
        """
        Count the corners of each region. These will correspond to th enumber of sides
        """
        corners = 0
        # Corner where we are inside the grid
        if (
            (x + diagonal[0], y) in connected
            and (x, y + diagonal[1]) in connected
            and in_grid(x + diagonal[0], y + diagonal[1], max_x, max_y)
            and grid[y + diagonal[1]][x + diagonal[0]] != val
        ):
            corners += 1

        # Corner where we are on the edge of the grid
        elif not in_grid(x + diagonal[0], y, max_x, max_y) and not in_grid(
            x, y + diagonal[1], max_x, max_y
        ):
            corners += 1

        # Corner where we are on the edge of the grid
        elif (
            not in_grid(x + diagonal[0], y, max_x, max_y)
            and grid[y + diagonal[1]][x] != val
        ):
            corners += 1

        # Corner where we are on the edge of the grid
        elif (
            not in_grid(x, y + diagonal[1], max_x, max_y)
            and grid[y][x + diagonal[0]] != val
        ):
            corners += 1

        # Corner where we are inside the grid
        elif (
            len(connected) == 2
            and in_grid(x + diagonal[0], y, max_x, max_y)
            and in_grid(x, y + diagonal[1], max_x, max_y)
            and grid[y][x + diagonal[0]] != val
            and grid[y + diagonal[1]][x] != val
        ):
            corners += 1
        return corners

    def find_region(x: int, y: int) -> int:
        possible_region: list[tuple[int, int]] = [(x, y)]
        val = grid[y][x]
        area, num_sides = 0, 0

        while possible_region:
            x, y = possible_region.pop()
            if (x, y) in visited:
                continue
            area += 1
            visited.add((x, y))

            connected: list[tuple[int, int]] = []
            for direction in directions:
                new_x, new_y = x + direction[0], y + direction[1]

                if in_grid(new_x, new_y, max_x, max_y):
                    if grid[new_y][new_x] == val:
                        connected.append((new_x, new_y))
                        possible_region.append((new_x, new_y))

            if len(connected) == 1:
                num_sides += 2

            elif len(connected) == 0:
                num_sides += 4

            else:
                num_sides += check_corner_and_edge_of_grid(connected, (1, 1), x, y, val)
                num_sides += check_corner_and_edge_of_grid(
                    connected, (1, -1), x, y, val
                )
                num_sides += check_corner_and_edge_of_grid(
                    connected, (-1, 1), x, y, val
                )
                num_sides += check_corner_and_edge_of_grid(
                    connected, (-1, -1), x, y, val
                )

        return area * num_sides

    total_score = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            total_score += find_region(x, y)

    return total_score


if __name__ == "__main__":
    inp = parse_input("test_input.txt")

    sol_1 = part_1(inp)
    sol_2 = part_2(inp)

    print(sol_1, sol_2)
