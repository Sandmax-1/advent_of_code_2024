import os
from pathlib import Path


def parse_input(file_name: str) -> list[str]:
    word_search: list[str] = []
    with open(Path(os.getcwd()) / f"day_4/data/{file_name}", "r") as f:
        for line in f.readlines():
            word_search.append(line.strip())

    return word_search


def part_1(word_search: list[str]) -> int:
    def find_xmas(x: int, y: int) -> int:
        if word_search[y][x] != "X":
            return 0

        count = 0

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        for direction in directions:
            coords = [
                (x + ind * direction[0], y + ind * direction[1]) for ind in range(4)
            ]
            word = ""
            for coord in coords:
                if (
                    0 <= coord[0] <= len(word_search[0]) - 1
                    and 0 <= coord[1] <= len(word_search) - 1  # noqa: W503
                ):
                    word += word_search[coord[1]][coord[0]]
                else:
                    break
            if "XMAS" == "".join(word):
                count += 1

        return count

    count = 0
    for y in range(len(word_search)):
        for x in range(len(word_search[1])):
            add = find_xmas(x, y)
            count += add

    return count


def part_2(word_search: list[str]) -> int:
    def find_xmas(x: int, y: int) -> int:
        count = 0

        if word_search[y][x] != "A":
            return 0

        forward_diag = [(x - 1, y - 1), (x, y), (x + 1, y + 1)]
        back_diag = [(x - 1, y + 1), (x, y), (x + 1, y - 1)]

        for_word = ""
        back_word = ""

        for ind in range(3):
            for_coord = forward_diag[ind]
            back_coord = back_diag[ind]
            if (
                0 <= for_coord[0] <= len(word_search[0]) - 1
                and 0 <= for_coord[1] <= len(word_search) - 1  # noqa: W503
            ):
                for_word += word_search[for_coord[1]][for_coord[0]]

            if (
                0 <= back_coord[0] <= len(word_search[0]) - 1
                and 0 <= back_coord[1] <= len(word_search) - 1  # noqa: W503
            ):
                back_word += word_search[back_coord[1]][back_coord[0]]

        if for_word == "MAS" and back_word == "MAS":
            count += 1
        elif for_word == "SAM" and back_word == "MAS":
            count += 1
        elif for_word == "MAS" and back_word == "SAM":
            count += 1
        elif for_word == "SAM" and back_word == "SAM":
            count += 1

        return count

    count = 0
    for y in range(len(word_search)):
        for x in range(len(word_search[1])):
            add = find_xmas(x, y)
            count += add

    return count


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")

    sol_1 = part_1(inp)
    sol_2 = part_2(inp)

    print(sol_1, sol_2)
