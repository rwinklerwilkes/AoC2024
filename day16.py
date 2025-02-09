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

def dijkstra(grid, pos, start_dir='right'):
    dist = {}
    prev = defaultdict(tuple)
    q = []
    hq.heappush(q, (0, pos, start_dir))
    dist[(*pos,start_dir)] = 0

    while q:
        cnode = hq.heappop(q)
        p, u, current_direction = cnode
        all_neighbors = get_neighbors(grid, u)
        current_dist = dist[(*u,current_direction)]
        for ndir, n in all_neighbors.items():
            alt = current_dist + rotate(current_direction, ndir) * 1000 + 1
            if (*n,ndir) not in dist or alt < dist[(*n,ndir)]:
                prev[n] = u
                dist[(*n,ndir)] = alt
                hq.heappush(q, (alt, n, ndir))
    return dist, prev

def dijkstra_part_two(grid, starts):
    dist = {}
    prev = defaultdict(tuple)
    q = []
    for sr, sc, sd in starts:
        hq.heappush(q, (0, (sr, sc), sd))
        dist[(*(sr, sc),sd)] = 0

    while q:
        cnode = hq.heappop(q)
        p, u, current_direction = cnode
        all_neighbors = get_neighbors(grid, u)
        current_dist = dist[(*u,current_direction)]
        for ndir, n in all_neighbors.items():
            alt = current_dist + rotate(current_direction, ndir) * 1000 + 1
            if (*n,ndir) not in dist or alt < dist[(*n,ndir)]:
                prev[n] = u
                dist[(*n,ndir)] = alt
                hq.heappush(q, (alt, n, ndir))
    return dist, prev


def part_one(data):
    grid, start_pos, end_pos, mxh, mxw = parse_data(data)
    dist, prev = dijkstra(grid, start_pos)
    answer = np.inf
    for end_dir in ('left','right','down','up'):
        answer = min(answer,dist.get((*end_pos,end_dir),np.inf))
    return answer, dist, prev

part_one_example_answer, d, p = part_one(example_data)
assert part_one_example_answer == 7036
part_one_example_answer_two, _, _ = part_one(example_data_two)
assert part_one_example_answer_two == 11048

part_one_answer = part_one(data)

grid, start_pos, end_pos, mxh, mxw = parse_data(example_data_two)
dist, prev = dijkstra(grid, start_pos)

eds, eds_prev = dijkstra_part_two(grid, [(*end_pos, d) for d in ['right','left','up','down']])
res = set()
for row in range(mxh):
    for col in range(mxw):
        for ed in eds:
            flip = {'up':'down','right':'left','left':'right','down':'up'}
            for dir in ['up','down','left','right']:
                if (row,col,dir) in dist and (row,col,flip[dir]) in ed:
                    start_len = dist[(row, col, dir)]
                    end_len = ed[(row, col, flip[dir])]
                    if start_len + end_len == part_one_example_answer_two:
                        res.add((row,col))
print(len(res))