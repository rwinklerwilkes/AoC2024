from aocd import get_data
from collections import defaultdict, Counter
import heapq as hq
import numpy as np

data = get_data(day=20,year=2024)
example_data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

def parse_data(data):
    grid = {}
    start = None
    end = None
    for ri, row in enumerate(data.split('\n')):
        for cj, val in enumerate(row):
            grid[(ri, cj)] = val
            if val == 'S':
                start = (ri,cj)
            elif val == 'E':
                end = (ri,cj)
    return grid, start, end

def tadd(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def get_neighbors(grid, pos, cheat=False):
    possible_neighbors = [(-1, 0),(0, -1), (1, 0), (0, 1)]
    neighbors = [tadd(pos, v) for v in possible_neighbors]
    if not cheat:
        neighbors = [n for n in neighbors if grid.get(n, '#') != '#']
    else:
        neighbors = [n for n in neighbors if grid.get(n, '#') == '#']
    return neighbors

def dijkstra(grid, start, end):
    dist = defaultdict(int)
    for k,_ in grid.items():
        dist[(k[0],k[1])] = np.inf
    prev = defaultdict(tuple)
    q = []
    hq.heappush(q, (0,start))
    dist[start] = 0

    while q:
        cnode = hq.heappop(q)
        p, u = cnode
        all_neighbors = get_neighbors(grid, u)
        for n in all_neighbors:
            alt = dist[u] + 1
            if alt < dist[n]:
                prev[n] = u
                dist[n] = alt
                hq.heappush(q, (alt, n))
    answer = dist[end]

    return dist, prev, answer

def cheat_spaces(grid, node):
    cheat_neighbors = get_neighbors(grid, node, cheat=True)
    ways_back = []
    for cn in cheat_neighbors:
        normal = get_neighbors(grid, cn, cheat=False)
        for n in normal:
            if n != node:
                ways_back.append(n)
    return ways_back

def manhattan(t1, t2):
    return abs(t1[0]-t2[0]) + abs(t1[1]-t2[1])

def part_one(data):
    grid, start, end = parse_data(data)
    start_dist, start_prev, total_length = dijkstra(grid, start, end)
    end_dist, end_prev,_ = dijkstra(grid, end, start)
    full_path = []
    cn = end
    while cn != start:
        full_path.append(start_prev[cn])
        cn = start_prev[cn]

    time_saved = {}
    for current_node in full_path:
        cheats = cheat_spaces(grid, current_node)
        for cheat_node in cheats:
            elapsed_dist = start_dist[current_node]
            remaining_dist = end_dist[cheat_node]
            cheat_dist = manhattan(current_node, cheat_node)
            time_saved[(current_node,cheat_node)] = total_length - (elapsed_dist + remaining_dist + cheat_dist)
    good_cheats = {k:v for k,v in time_saved.items() if v > 0}
    ctr = Counter(good_cheats.values())
    meets_saved_threshold = [v for k,v in ctr.items() if k >= 100]
    answer = sum(meets_saved_threshold)
    return answer

part_one_answer = part_one(data)