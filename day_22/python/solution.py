from pathlib import Path


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


def part_one(secrets: list[int], max_time: int) -> list[int]:
    out: list[int] = []
    for secret in secrets:
        new_secret = secret
        for _ in range(max_time):
            new_secret = evolve(new_secret)
        out.append(new_secret)
    return out


if __name__ == "__main__":
    inp = parse_input("actual_input.txt")
    sol_1 = part_one(inp, 2000)
    print(sum(sol_1))
