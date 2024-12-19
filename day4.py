from aocd import get_data
import numpy as np

data = get_data(day=4,year=2024)
example_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def parse_and_pad(data):
    parsed = [[i for i in row] for row in data.split('\n')]
    padded = np.pad(parsed, pad_width=3, constant_values='.')
    return padded

def part_one(data):
    parsed_data = parse_and_pad(data)
    mx = parsed_data.shape[0]
    my = parsed_data.shape[1]
    already_found = set()
    #Take into account effect of padding
    for i in range(3, mx-3):
        for j in range(3, my-3):
            neighbors = get_neighbors(i,j)
            for n in neighbors:
                #Check if already found
                coord_hash = hash(frozenset(n))
                if coord_hash in already_found:
                    continue
                #Else check the string
                check_string = ''.join([parsed_data[xi, yi] for xi, yi in n])
                if check_string == 'XMAS' or check_string == 'SAMX':
                    already_found.add(coord_hash)
    answer = len(already_found)
    return answer

def get_neighbors(x,y):
    neighbors = []
    for xd in [-1,0,1]:
        for yd in [-1,0,1]:
            if xd == yd and xd == 0:
                continue
            xys = [(x,y)] + [(x + xd*i, y + yd*i) for i in range(1,4)]
            neighbors.append(xys)
    return neighbors

def is_xmas(data, x,y):
    check_diag_left = ''.join([data[x - i,y - i] for i in [-1,0,1]])
    check_diag_right = ''.join([data[x - i, y + i] for i in [-1, 0, 1]])
    return check_diag_left in ['MAS','SAM'] and check_diag_right in ['MAS','SAM']

def part_two(data):
    parsed_data = parse_and_pad(data)
    mx = parsed_data.shape[0]
    my = parsed_data.shape[1]

    already_found = set()
    #Take into account effect of padding
    for i in range(3, mx-3):
        for j in range(3, my-3):
            if parsed_data[i,j] != 'A' or (i,j) in already_found:
                continue
            if is_xmas(parsed_data, i, j):
                already_found.add((i,j))
    answer = len(already_found)
    return answer



part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
part_two_answer = part_two(data)