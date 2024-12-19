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

example_data_four = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

example_data_five = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

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

def all_neighbors(grid, node):
    neighbor_dict = {'up':(-1,0),
                     'left':(0,-1),
                     'down':(1,0),
                     'right':(0,1),
                     'ur':(-1,1),
                     'ul':(-1,-1),
                     'dr':(1,1),
                     'dl':(1,-1)}
    neighbors = {k:grid.get(tadd(node,v)) for k,v in neighbor_dict.items()}
    return neighbors

def count_corners(grid:dict, region:set):
    rgn = region.copy()
    corners = 0
    while rgn:
        node = rgn.pop()
        nv = grid[node]
        neighbors = all_neighbors(grid, node)
        #Inside corners
        # UR
        # ##.
        # ###
        # ###
        # UR is different region, UU and RR is same region
        if nv == neighbors['up'] and nv == neighbors['right'] and (nv != neighbors['ur']):
            corners += 1
        # UL
        if nv == neighbors['up'] and nv == neighbors['left'] and (nv != neighbors['ul']):
            corners += 1
        # DR
        if nv == neighbors['down'] and nv == neighbors['right'] and (nv != neighbors['dr']):
            corners += 1
        # DL
        if nv == neighbors['down'] and nv == neighbors['left'] and (nv != neighbors['dl']):
            corners += 1
        #Outside corners
        # UR
        # ...
        # ##.
        # ##.
        # UR is different region, UU and RR are different region
        if nv != neighbors['up'] and nv != neighbors['right'] and (nv != neighbors['ur']):
            corners += 1
        # UL
        if nv != neighbors['up'] and nv != neighbors['left'] and (nv != neighbors['ul']):
            corners += 1
        # DR
        if nv != neighbors['down'] and nv != neighbors['right'] and (nv != neighbors['dr']):
            corners += 1
        # DL
        if nv != neighbors['down'] and nv != neighbors['left'] and (nv != neighbors['dl']):
            corners += 1
    return corners

def get_answer(data, part_two = False):
    parsed_data = parse_data(data)
    remaining_nodes = set(parsed_data.keys())
    answer = 0
    while remaining_nodes:
        cur_node = remaining_nodes.pop()
        rgn = flood_fill(parsed_data, cur_node)
        if part_two:
            score = count_corners(parsed_data, rgn)
        else:
            score = calculate_perimeter(region=rgn)
        answer += score * len(rgn)
        remaining_nodes = remaining_nodes.difference(rgn)
    return answer

part_one_example_answer_one = get_answer(example_data)
assert part_one_example_answer_one == 140

part_one_example_answer_two = get_answer(example_data_two)
assert part_one_example_answer_two == 772

part_one_example_answer_three = get_answer(example_data_three)
assert part_one_example_answer_three == 1930

part_one_answer = get_answer(data)

part_two_example_answer = get_answer(example_data, part_two=True)
assert part_two_example_answer == 80

part_two_example_answer_two = get_answer(example_data_two, part_two=True)
assert part_two_example_answer_two == 436

part_two_example_answer_three = get_answer(example_data_three, part_two=True)
assert part_two_example_answer_three == 1206

part_two_example_answer_four = get_answer(example_data_four, part_two=True)
assert part_two_example_answer_four == 236

part_two_example_answer_five = get_answer(example_data_five, part_two=True)
assert part_two_example_answer_five == 368

part_two_answer = get_answer(data, part_two=True)

parsed_data = parse_data(example_data_five)
remaining_nodes = set(parsed_data.keys())
cur_node = remaining_nodes.pop()
rgn = flood_fill(parsed_data, cur_node)
remaining_nodes = remaining_nodes.difference(rgn)

cur_node = remaining_nodes.pop()
rgn = flood_fill(parsed_data, cur_node)
count_corners(parsed_data, rgn)