from dataclasses import dataclass
from functools import lru_cache
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


def parse_input(
    file_name: str,
) -> list[str]:
    with open(Path().cwd() / "day_21" / "data" / file_name, "r") as f:
        return list(map(str.strip, f.readlines()))


NUMERICAL_KEYPAD_MAP = {
    "A": Coordinate(2, 3),
    "0": Coordinate(1, 3),
    "3": Coordinate(2, 2),
    "2": Coordinate(1, 2),
    "1": Coordinate(0, 2),
    "6": Coordinate(2, 1),
    "5": Coordinate(1, 1),
    "4": Coordinate(0, 1),
    "9": Coordinate(2, 0),
    "8": Coordinate(1, 0),
    "7": Coordinate(0, 0),
}

DIRECTIONAL_KEYPAD_MAP = {
    ">": Coordinate(2, 1),
    "v": Coordinate(1, 1),
    "<": Coordinate(0, 1),
    "A": Coordinate(2, 0),
    "^": Coordinate(1, 0),
}


def part_one(codes: list[str]) -> int:
    return enter_sequences(codes, 2)


def part_two(codes: list[str]) -> int:
    return enter_sequences(codes, 12)


def enter_sequences(codes: list[str], num_directional_pads: int) -> int:
    complexities: list[tuple[int, int]] = []
    for code in codes:
        keyseq = enter_sequence(code, is_numeric_pad=True)
        for _ in range(num_directional_pads):
            keyseq = enter_sequence(keyseq, is_numeric_pad=False)
        complexities.append((len(keyseq), int(code[0:-1])))
    print(complexities)
    return sum([c[0] * c[1] for c in complexities])


def enter_sequence(code: str, is_numeric_pad: bool) -> str:
    keyseq = ""
    if is_numeric_pad:
        keypad = NUMERICAL_KEYPAD_MAP
        current_pos = Coordinate(2, 3)
    else:
        keypad = DIRECTIONAL_KEYPAD_MAP
        current_pos = Coordinate(2, 0)

    for char in code:
        destination = keypad[char]
        added_seq, current_pos = new_func(is_numeric_pad, destination, current_pos)
        keyseq += added_seq
    return keyseq


@lru_cache(maxsize=None)
def new_func(
    is_numeric_pad: bool, destination: Coordinate, current_pos: Coordinate
) -> tuple[str, Coordinate]:
    print(f"CACHE INFO: {new_func.cache_info()}")
    added_seq = ""

    diff = current_pos - destination
    diff, bump = bump_to_avoid_empty(destination, current_pos, diff, is_numeric_pad)
    added_seq += bump
    added_seq += move_to_destination(diff) + "A"
    current_pos = destination
    return added_seq, current_pos


def bump_to_avoid_empty(
    destination: Coordinate,
    current_pos: Coordinate,
    diff: Coordinate,
    is_numeric_pad: bool,
) -> tuple[Coordinate, str]:
    if is_numeric_pad:
        empty_space = Coordinate(0, 3)
    else:
        empty_space = Coordinate(0, 0)
    bump = ""
    if destination.x == empty_space.x and current_pos.y == empty_space.y:
        if is_numeric_pad:
            bump += "^" * abs(diff.y)
            diff += Coordinate(0, -abs(diff.y))
        else:
            bump += "v" * abs(diff.y)
            diff += Coordinate(0, abs(diff.y))
    if destination.y == empty_space.y and current_pos.x == empty_space.x:
        bump += ">" * abs(diff.x)
        diff += Coordinate(abs(diff.x), 0)

    return diff, bump


def move_to_destination(diff: Coordinate) -> str:
    keyseq = ""
    while diff != Coordinate(0, 0):
        if diff.x != 0 and diff.x > 0:
            keyseq += "<" * diff.x
            diff += Coordinate(-1 * diff.x, 0)

        elif diff.y != 0:
            if diff.y < 0:
                keyseq += "v" * abs(diff.y)
                diff += Coordinate(0, 1 * abs(diff.y))
            else:
                keyseq += "^" * diff.y
                diff += Coordinate(0, -1 * diff.y)

        elif diff.x != 0 and diff.x < 0:
            keyseq += ">" * abs(diff.x)
            diff += Coordinate(1 * abs(diff.x), 0)

    return keyseq


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")
    sol_1 = part_one(inp)
    print(f"CACHE INFO: {new_func.cache_info()}")
    sol_2 = part_two(inp)
    print(f"CACHE INFO: {new_func.cache_info()}")

    print(sol_1, sol_2)
