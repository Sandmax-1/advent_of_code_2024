from copy import deepcopy
from pathlib import Path


def parse_input(
    file_name: str,
) -> tuple[list[str], list[tuple[int, int]], list[tuple[int, int]]]:
    with open(Path().cwd() / "day_9" / "data" / file_name, "r") as f:
        files = f.read().strip()

    pos = 0
    file_system: list[str] = []
    free_space_map: list[tuple[int, int]] = []
    file_map: list[tuple[int, int]] = []
    free_space_index = 0
    file_index = 0
    while pos <= len(files) - 1:
        file_length = int(files[pos])
        file_map.append((file_index, file_length))
        id = pos // 2
        free_space_index += file_length

        if pos == len(files) - 1:
            file_system += [str(id)] * file_length
            pos += 2
            continue

        free_space = int(files[pos + 1])
        free_space_map.append((free_space_index, free_space))
        free_space_index += free_space
        file_index += free_space + file_length
        pos += 2

        file_system += [str(id)] * file_length + ["."] * free_space

    return file_system, free_space_map, file_map


def part_1(file_system: list[str]) -> int:
    def find_next_free_space(file_system: list[str], free_space_pointer: int) -> int:
        val = file_system[free_space_pointer]
        while val != "." and free_space_pointer != len(file_system):
            free_space_pointer += 1
            val = file_system[free_space_pointer]

        return free_space_pointer

    free_space_pointer = file_system.index(".")

    for ind, val in enumerate(reversed(file_system)):
        if val != ".":
            file_system[free_space_pointer] = val
            file_system[len(file_system) - ind - 1] = "."
            free_space_pointer = find_next_free_space(file_system, free_space_pointer)
            if ind >= len(file_system) - free_space_pointer - 2:
                break

    return sum(
        [ind * int(val) if val != "." else 0 for ind, val in enumerate(file_system)]
    )


def part_2(
    file_system: list[str],
    free_space_map: list[tuple[int, int]],
    file_map: list[tuple[int, int]],
) -> int:
    for file_index, file_length in reversed(file_map):
        for free_space_map_ind, (empty_space_index, empty_space_length) in enumerate(
            free_space_map
        ):
            if empty_space_index >= file_index:
                break
            elif file_length <= empty_space_length:
                val = file_system[file_index]

                for offset in range(file_length):
                    file_system[file_index + offset] = "."
                    file_system[empty_space_index + offset] = val

                free_space_map[free_space_map_ind] = (
                    empty_space_index + file_length,
                    empty_space_length - file_length,
                )
                break

    return sum(
        [ind * int(val) if val != "." else 0 for ind, val in enumerate(file_system)]
    )


if __name__ == "__main__":
    file_system, free_space_map, file_map = parse_input("actual_input.txt")

    sol_1 = part_1(deepcopy(file_system))
    sol_2 = part_2(file_system, free_space_map, file_map)

    print(sol_1, sol_2)
