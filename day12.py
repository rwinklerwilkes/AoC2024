from aocd import get_data
from collections import deque

data = get_data(day=12,year=2024)
example_data = """AAAA
BBCD
BBCC
EEEC"""

example_data_two = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

example_data_three = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


def parse_data(data):
    grid = {}
    for i, row in enumerate(data.split('\n')):
        for j, val in enumerate(row):
            grid[(i,j)] = val
    return grid

def tadd(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def flood_fill(grid, node):
    q = deque([node])
    inside_val = grid[node]
    region = set()
    while q:
        n = q.popleft()
        if grid.get(n,-1) == inside_val and n not in region:
            region.add(n)
            for nbr in [(-1,0),(1,0),(0,-1),(0,1)]:
                q.append(tadd(n,nbr))
    return region

def calculate_perimeter(region):
    perimeter = 0
    for n in region:
        sides_not_touching = 0
        for nbr in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if tadd(n, nbr) not in region:
                sides_not_touching += 1
        perimeter += sides_not_touching
    return perimeter

def count_corners(region):
    #Inside corners
    # UR
    # ##.
    # ###
    # ###
    # UR is different region, UU and RR is same region
    # UL
    # DR
    # DL
    #Outside corners
    # UR
    # ...
    # ##.
    # ##.
    # UR is different region, UU and RR are different region
    # UL
    # DR
    # DL
    pass

def part_one(data):
    parsed_data = parse_data(data)
    remaining_nodes = set(parsed_data.keys())
    answer = 0
    while remaining_nodes:
        cur_node = remaining_nodes.pop()
        rgn = flood_fill(parsed_data, cur_node)
        answer += calculate_perimeter(region=rgn) * len(rgn)
        remaining_nodes = remaining_nodes.difference(rgn)
    return answer

part_one_example_answer_one = part_one(example_data)
assert part_one_example_answer_one == 140

part_one_example_answer_two = part_one(example_data_two)
assert part_one_example_answer_two == 772

part_one_example_answer_three = part_one(example_data_three)
assert part_one_example_answer_three == 1930

part_one_answer = part_one(data)

