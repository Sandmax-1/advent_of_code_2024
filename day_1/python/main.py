import os
from pathlib import Path
from collections import Counter


def parse_input(file_name: str) -> tuple[list[int], list[int]]:
    with open(Path(os.getcwd()) / f'day_1/data/{file_name}', 'r') as f: 
        id_list_1: list[int] = []
        id_list_2: list[int] = []
        for line in f.readlines():
            split_line = line.split('   ')
            id_list_1.append(int(split_line[0]))
            id_list_2.append(int(split_line[1]))
        
    return id_list_1, id_list_2
            

def part_1(id_list_1: list[int], id_list_2: list[int]) -> int:
    id_list_1 = sorted(id_list_1)
    id_list_2 = sorted(id_list_2)
    
    return sum([abs(el_1 - el_2) for el_1, el_2 in zip(id_list_1, id_list_2)])


def part_2(id_list_1: list[int], id_list_2: list[int]) -> int:
    counts_list_2 = Counter(id_list_2)
    total = 0
    for id in id_list_1:
        total += counts_list_2.get(id, 0)*id
    
    return total
        

if __name__ == '__main__':
    id_list_1, id_list_2 = parse_input('actual_input.txt')
    sol_1 = part_1(id_list_1, id_list_2)
    sol_2 = part_2(id_list_1, id_list_2)
    print(sol_2)