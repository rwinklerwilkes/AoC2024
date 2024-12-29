from aocd import get_data
from collections import defaultdict
import heapq as hq
import numpy as np

data = get_data(day=18,year=2024)
example_data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

def constant_factory(value):
    return lambda: value

def parse_data(data):
    grid = defaultdict(constant_factory('.'))

    for i, row in enumerate(data.split('\n')):
        column, row = [int(i) for i in row.split(',')]
        grid[(i,row,column)] = '#'
    return grid

def get_grid_at_t(grid, t, mxrow, mxcol):
    grid_at_t = {(k[1],k[2]):v for k,v in grid.items() if k[0] < t}
    for r in range(mxrow):
        for c in range(mxcol):
            if (r,c) not in grid_at_t:
                grid_at_t[(r,c)] = '.'

    for r in range(mxrow):
        grid_at_t[(r,-1)] = '#'
        grid_at_t[(r,mxcol)] = '#'

    for c in range(mxcol):
        grid_at_t[(-1,c)] = '#'
        grid_at_t[(mxrow,c)] = '#'

    return grid_at_t

def print_grid(grid, t, mxrow, mxcol):
    b = [['_' for v in range(mxcol)] for h in range(mxrow)]
    for k,v in grid.items():
        is_valid = k[-2] >= 0 and k[-2] < mxrow and k[-1] >= 0 and k[-1] < mxcol
        if len(k) == 2 and is_valid:
            if v == '.':
                new_v = '_'
            else:
                new_v = v
            b[k[0]][k[1]] = new_v
        if len(k) == 3 and k[0] < t and is_valid:
            b[k[1]][k[2]] = v
    output_board = '\n'.join(''.join(row) for row in b)
    print(output_board)

def tadd(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def get_neighbors(grid_at_time, pos):
    possible_neighbors = [(-1, 0),(0, -1), (1, 0), (0, 1)]
    neighbors = [tadd(pos, v) for v in possible_neighbors]
    neighbors = [n for n in neighbors if grid_at_time.get(n,'.') != '#']
    return neighbors

def dijkstra(grid, mxrow, mxcol, t):
    failed = False
    start = (0,0)
    end = (mxrow-1, mxcol-1)
    grid_at_t = get_grid_at_t(grid, t, mxrow, mxcol)
    dist = defaultdict(int)
    for k,_ in grid_at_t.items():
        dist[(k[0],k[1])] = np.inf
    prev = defaultdict(tuple)
    q = []
    hq.heappush(q, (0,start))
    dist[start] = 0

    while q:
        cnode = hq.heappop(q)
        p, u = cnode
        all_neighbors = get_neighbors(grid_at_t, u)
        for n in all_neighbors:
            alt = dist[u] + 1
            if alt < dist[n]:
                prev[n] = u
                dist[n] = alt
                hq.heappush(q, (alt, n))
    answer = dist[end]
    if np.isinf(answer):
        failed = True

    return dist, prev, answer, failed

def part_one(data, mxrow, mxcol, time):
    grid = parse_data(data)
    dist, prev, answer, _ = dijkstra(grid, mxrow+1, mxcol+1, time)
    return dist, prev, answer

def part_two(data, mxrow, mxcol,start_time):
    grid = parse_data(data)
    done = False
    time = start_time
    while not done:
        dist, prev, answer, failed = dijkstra(grid, mxrow + 1, mxcol + 1, time)
        if failed:
            print(f"Couldn't complete at time {time}")
            done = True
        else:
            time += 1
    answer_time = [(k[2],k[1]) for k,v in grid.items() if k[0]==time-1]
    return answer_time[0]

_, _, part_one_example_answer = part_one(example_data, 6, 6, 12)
print(part_one_example_answer)

_, _, part_one_answer = part_one(data, 70, 70, 1024)
print(part_one_answer)

part_two_example_answer = part_two(example_data, 6, 6, 12)
part_two_answer = part_two(data, 70, 70, 1024)