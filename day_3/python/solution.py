import os
import re
from functools import reduce
from pathlib import Path


def parse_input(file_name: str) -> str:
    with open(Path(os.getcwd()) / f"day_3/data/{file_name}", "r") as f:
        data = f.read()

    return data


def part_1(data: str) -> int:
    mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"

    mults = "".join(re.findall(mul_pattern, data))

    nums_pattern = r"\d{1,3},\d{1,3}"

    nums = re.findall(nums_pattern, mults)

    nums = [pair.split(",") for pair in nums]
    out = sum([reduce(lambda a, b: a * b, map(int, pair)) for pair in nums])

    return out


def part_2(data: str) -> int:
    mul_pattern = r"(do\(\)|mul\(\d{1,3},\d{1,3}\)|don\'t\(\))"

    ops = re.findall(mul_pattern, data)

    enabled = True
    mults: list[str] = []

    for op in ops:
        if op == "do()":
            enabled = True
        elif op == "don't()":
            enabled = False
        elif enabled:
            mults.append(op)

    nums_pattern = r"\d{1,3},\d{1,3}"

    mult_str = "".join(mults)

    nums = re.findall(nums_pattern, mult_str)

    nums = [pair.split(",") for pair in nums]
    out = sum([reduce(lambda a, b: a * b, map(int, pair)) for pair in nums])

    return out


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")

    sol_1 = part_1(inp)
    sol_2 = part_2(inp)

    print(sol_1, sol_2)
