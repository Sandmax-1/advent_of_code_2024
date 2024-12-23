from collections import defaultdict
from pathlib import Path
from typing import Iterable


def parse_input(
    file_name: str,
) -> list[int]:
    with open(Path().cwd() / "day_22" / "data" / file_name, "r") as f:
        return list(map(int, map(str.strip, f.readlines())))


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def mix(given_number: int, secret_number: int) -> int:
    return given_number ^ secret_number


def evolve(secret_number: int) -> int:
    new_secret = prune(mix(secret_number * 64, secret_number))
    new_secret = prune(mix(new_secret // 32, new_secret))
    new_secret = prune(mix(new_secret * 2048, new_secret))
    return new_secret


def get_price(secret_number: int) -> int:
    return secret_number % 10


def part_one(secrets: list[int], max_time: int) -> list[int]:
    new_secrets: Iterable[int] = secrets

    for _ in range(max_time):
        new_secrets = map(evolve, new_secrets)

    return list(new_secrets)


def part_two(secrets: list[int], max_time: int) -> int:
    diffs: list[list[int]] = [[] for _ in secrets]
    prices: defaultdict[int, list[tuple[int, ...]]] = defaultdict(list)

    for ind, secret in enumerate(secrets):
        old_price = get_price(secret)
        new_secret = secret
        seen_sequences: set[tuple[int, ...]] = set()
        for time_step in range(max_time):
            new_secret = evolve(new_secret)
            new_price = get_price(new_secret)
            diff = new_price - old_price
            diffs[ind].append(diff)
            old_price = new_price

            if time_step < 3:
                continue
            elif (new_sequence := tuple(diffs[ind][-4:])) not in seen_sequences:
                seen_sequences.add(new_sequence)
                prices[new_price].append(new_sequence)

    counted: defaultdict[tuple[int, ...], int] = defaultdict(int)

    for num in range(10, 1, -1):
        for seq in prices[num]:
            counted[seq] += num

    return max(counted.values())


if __name__ == "__main__":
    inp = parse_input("test_input.txt")

    sol_1 = part_one(inp, 2000)

    sol_2 = part_two(inp, 2000)
    print(sol_1, sol_2)
