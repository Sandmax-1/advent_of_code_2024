from pathlib import Path


def parse_input(file_name: str) -> list[list[int]]:
    grid: list[list[int]] = []
    with open(Path().cwd() / "day_10" / "data" / file_name, "r") as f:
        for line in f.readlines():
            grid.append(list(map(int, list(line.strip()))))
    return grid


def in_grid(x: int, y: int, max_x: int, max_y: int) -> bool:
    return 0 <= x <= max_x - 1 and 0 <= y <= max_y - 1


def get_trails(grid: list[list[int]], is_part_1: bool) -> int:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    max_x, max_y = len(grid[0]), len(grid)
    total_hiking_trails = 0

    def find_paths(x: int, y: int) -> list[tuple[int, int]]:
        total_hiking_trails: list[tuple[int, int]] = []

        if grid[y][x] != 0:
            return []

        path_list: list[tuple[int, int, int]] = [(grid[y][x], x, y)]

        while path_list:
            current_path_height, x, y = path_list.pop()
            if current_path_height == 9:
                total_hiking_trails.append((x, y))

            else:
                for direction in directions:
                    new_x, new_y = x + direction[0], y + direction[1]

                    if (
                        in_grid(new_x, new_y, max_x, max_y)
                        and grid[new_y][new_x] - current_path_height == 1  # noqa: W503
                    ):
                        path_list.append((current_path_height + 1, new_x, new_y))
        return total_hiking_trails

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            new_trail_heads = find_paths(x, y)
            if is_part_1:
                total_hiking_trails += len(set(new_trail_heads))
            else:
                total_hiking_trails += len(new_trail_heads)
    return total_hiking_trails


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")
    # print(inp)

    sol_1 = get_trails(inp, is_part_1=True)
    sol_2 = get_trails(inp, is_part_1=False)

    print(sol_1, sol_2)
