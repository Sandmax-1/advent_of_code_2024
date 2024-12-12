from pathlib import Path


def parse_input(file_name: str) -> list[tuple[int, list[int]]]:
    calculations: list[tuple[int, list[int]]] = []
    with open(Path().cwd() / "day_7" / "data" / file_name, "r") as f:
        for line in f.readlines():
            split_line = list(map(str.strip, line.split(":")))
            calculations.append(
                (int(split_line[0]), list(map(int, split_line[1].split(" "))))
            )
    return calculations


def part_1(calculations: list[tuple[int, list[int]]]) -> int:
    total = 0

    for value, operands in calculations:
        residuals: list[int] = [value]

        for operand in reversed(operands):
            new_residuals: list[int] = []
            # print(residuals, operand, value)
            for residual in residuals:
                if residual % operand == 0:
                    new_residuals.append(residual // operand)
                if residual >= operand:
                    new_residuals.append(residual - operand)
            residuals = new_residuals

        # print(residuals, value)
        if 0 in residuals:
            total += value
    return total


def part_2(calculations: list[tuple[int, list[int]]]) -> int:
    total = 0

    for value, operands in calculations:
        operands = list(reversed(operands))

        residuals: list[int] = [value]
        concat_numbers: list[int] = []

        for ind in range(len(operands)):
            residuals, concat_numbers = check_next_number(
                operands, residuals, ind, concat_numbers
            )

        if 0 in residuals:
            total += value
    return total


def check_next_number(
    operands: list[int], residuals: list[int], ind: int, concat_numbers: list[int]
) -> tuple[list[int], list[int]]:
    new_residuals: list[int] = []
    new_concat_numbers: list[int] = []
    operand = operands[ind]

    if ind != len(operands) - 1:
        new_concat_numbers = [int(str(operands[ind + 1]) + str(operand))] + [
            int(str(operands[ind + 1]) + str(num)) for num in concat_numbers
        ]

    for residual in residuals:
        for concat_number in [operand] + concat_numbers:
            if residual % operand == 0:
                new_residuals.append(residual // concat_number)
            if residual >= operand:
                new_residuals.append(residual - concat_number)

    return new_residuals, new_concat_numbers


if __name__ == "__main__":
    inp = parse_input("test_input.txt")

    sol_1 = part_1(inp)
    sol_2 = part_2(inp)

    print(sol_1, sol_2)


# 2501605300634 too low
