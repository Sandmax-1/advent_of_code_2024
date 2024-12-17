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


def parse_input(file_name: str) -> list[tuple[Coordinate, ...]]:
    machines: list[tuple[Coordinate, ...]] = []
    with open(Path().cwd() / "day_13" / "data" / file_name, "r") as f:
        out: list[Coordinate] = []
        for line in f.readlines():
            if line == "\n":
                machines.append(tuple(out))
                out = []
                continue

            info = line.strip().split(": ")[1].split(", ")

            button_rule = [i.split("+") for i in info]
            if len(button_rule[0]) == 2:
                button = [int(button[1]) for button in button_rule]

                out.append(Coordinate(button[0], button[1]))

            prize_pos = [i.split("=") for i in info]
            if len(prize_pos[0]) == 2:
                prize = [int(prize[1]) for prize in prize_pos]
                out.append(Coordinate(prize[0], prize[1]))
    machines.append(tuple(out))
    return machines


def get_tickets(machines: list[tuple[Coordinate, ...]]) -> int:
    total_tickets = 0
    cost_for_a = 3
    cost_for_b = 1
    for button_a, button_b, prize in machines:
        num_b_presses = (prize.y * button_a.x - prize.x * button_a.y) / (
            button_a.x * button_b.y - button_a.y * button_b.x
        )
        num_a_presses = (prize.x - button_b.x * num_b_presses) / button_a.x

        if not num_b_presses.is_integer() or not num_a_presses.is_integer():
            continue

        if int(num_a_presses) * button_a + int(num_b_presses) * button_b != prize:
            continue

        total_tickets += (
            int(num_a_presses) * cost_for_a + int(num_b_presses) * cost_for_b
        )
    return total_tickets


def part_1(machines: list[tuple[Coordinate, ...]]) -> int:
    return get_tickets(machines)


def part_2(machines: list[tuple[Coordinate, ...]]) -> int:
    machines = [
        (a, b, Coordinate(c.x + 10000000000000, c.y + 10000000000000))
        for a, b, c in machines
    ]
    return get_tickets(machines)


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")

    sol_1 = part_1(inp)
    sol_2 = part_2(inp)

    print(sol_1, sol_2)
