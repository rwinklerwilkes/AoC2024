from aocd import get_data
from collections import defaultdict
import itertools

data = get_data(day=8,year=2024)
example_data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

def parse_data(data):
    grid = defaultdict(list)
    mxrow= 0
    mxcol = 0
    for irow, row in enumerate(data.split('\n')):
        for icol, val in enumerate(row):
            if val != '.':
                grid[val].append((irow,icol))
            if icol > mxcol:
                mxcol = icol
        if irow > mxrow:
            mxrow = irow
    return grid, mxrow+1, mxcol+1

def find_antinodes(p1, p2, mx, my, part_one = True):
    if p1[0] > p2[0]:
        p1,p2 = p2,p1
    row1, col1 = p1
    row2, col2 = p2
    rowdiff = row2-row1
    coldiff = col2-col1

    left_antinodes = []
    right_antinodes = []

    t = 1 * part_one
    done_left = False
    while not done_left:
        nx1 = row1-t*rowdiff
        ny1 = col1-t*coldiff
        if nx1 < 0 or nx1 >= mx or ny1<0 or ny1 >= my:
            done_left = True
        else:
            left_antinodes.append((nx1, ny1))
        t += 1

    t = 1 * part_one
    done_right = False
    while not done_right:
        nx2 = row2+t*rowdiff
        ny2 = col2+t*coldiff
        if nx2 < 0 or nx2 >= mx or ny2 < 0 or ny2 >= my:
            done_right = True
        else:
            right_antinodes.append((nx2, ny2))
        t += 1

    if part_one:
        left_antinodes = left_antinodes[:1]
        right_antinodes = right_antinodes[:1]
    return left_antinodes, right_antinodes



def both_parts(data, part_one=True):
    parsed_data, mx, my = parse_data(data)
    antinodes = defaultdict(set)
    all_antinodes = set()
    for node_val, points in parsed_data.items():
        for p1, p2 in itertools.combinations(points, 2):
            np1, np2 = find_antinodes(p1, p2, mx, my, part_one=part_one)
            if np1:
                antinodes[node_val] = antinodes[node_val].union(np1)
                all_antinodes = all_antinodes.union(np1)
            if np2:
                antinodes[node_val] = antinodes[node_val].union(np2)
                all_antinodes = all_antinodes.union(np2)
    answer = len(all_antinodes)
    return answer

part_one_example_answer = both_parts(example_data, part_one=True)
assert part_one_example_answer == 14
part_one_answer = both_parts(data, part_one=True)

example_data_part_two = """T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
.........."""
part_two_example_answer = both_parts(example_data_part_two, part_one=False)
assert part_two_example_answer == 9
part_two_example_answer = both_parts(example_data, part_one=False)
assert part_two_example_answer == 34
part_two_answer = both_parts(data, part_one=False)
