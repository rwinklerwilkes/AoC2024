from aocd import get_data
from collections import defaultdict
import heapq as hq
import numpy as np

data = get_data(day=16,year=2024)
example_data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

example_data_two = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

def tadd(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def parse_data(data):
    grid = {}
    mxh = len(data.split('\n'))
    mxw = len(data.split('\n')[0])
    start_pos = None
    end_pos = None
    for i, row in enumerate(data.split('\n')):
        for j,val in enumerate(row):
            if val == 'S':
                start_pos = (i,j)
            elif val == 'E':
                end_pos = (i,j)
            grid[(i,j)] = val
    return grid, start_pos, end_pos, mxh, mxw

def get_neighbors(grid, pos):
    neighbor_dict = {'up': (-1, 0),
                     'left': (0, -1),
                     'down': (1, 0),
                     'right': (0, 1)}
    neighbors = {cdir: tadd(pos, v) for cdir, v in neighbor_dict.items()}
    neighbors = {cdir: n for cdir,n in neighbors.items() if grid[n] != '#'}
    return neighbors

def rotate(cur_dir, want_dir):
    all_directions = ['left','up','right','down','left']
    one_way = abs(all_directions.index(cur_dir)-all_directions.index(want_dir))
    other_way = abs(all_directions[::-1].index(cur_dir)-all_directions[::-1].index(want_dir))
    return min(one_way, other_way)

def dijkstra(grid, pos):
    dist = {}
    for k,_ in grid.items():
        dist[k] = np.inf
    prev = defaultdict(tuple)
    q = []
    hq.heappush(q, (0,pos,'right'))
    dist[pos] = 0

    while q:
        cnode = hq.heappop(q)
        p, u, current_direction = cnode
        all_neighbors = get_neighbors(grid, u)
        for ndir, n in all_neighbors.items():
            alt = dist[u] + rotate(current_direction, ndir) * 1000 + 1
            if alt < dist[n]:
                prev[n] = u
                dist[n] = alt
                hq.heappush(q, (alt, n, ndir))
    return dist, prev

def part_one(data):
    grid, start_pos, end_pos, mxh, mxw = parse_data(data)
    dist, prev = dijkstra(grid, start_pos)
    answer = dist[end_pos]
    return answer

part_one_example_answer = part_one(example_data)
assert part_one_example_answer == 7036
part_one_example_answer_two = part_one(example_data_two)
assert part_one_example_answer_two == 11048

part_one_answer = part_one(data)