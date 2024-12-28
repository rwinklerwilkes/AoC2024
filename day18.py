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

def parse_data(data, mxx, mxy):
    grid = defaultdict(constant_factory('.'))

    for i, row in enumerate(data.split('\n')):
        x,y = [int(i) for i in row.split(',')]
        grid[(i,y,x)] = '#'

    for i in range(mxy):
        grid[(-1, i, -1)] = '#'
        grid[(-1, i, mxx+1)] = '#'
    for i in range(mxx):
        grid[(-1, -1, i)] = '#'
        grid[(-1, mxy+1, i)] = '#'
    return grid

def get_grid_at_t(grid, t, mxx, mxy):
    grid_at_t = {(k[1],k[2]):v for k,v in grid.items() if k[0] < t}
    for x in range(mxx):
        for y in range(mxy):
            if (y,x) not in grid_at_t:
                grid_at_t[(y,x)] = '.'
    return grid_at_t

def print_grid(grid, t, mxh, mxw):
    b = [['_' for v in range(mxw)] for h in range(mxh)]
    for k,v in grid.items():
        is_valid = k[-2] >= 0 and k[-2] < mxh and k[-1] >= 0 and k[-1] < mxw
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

def get_neighbors(grid, pos, t):
    neighbor_dict = {'up': (-1, 0),
                     'left': (0, -1),
                     'down': (1, 0),
                     'right': (0, 1)}
    neighbors = {cdir: tadd(pos, v) for cdir, v in neighbor_dict.items()}
    grid_at_time = {(k[1],k[2]):v for k,v in grid.items() if k[0] < t}
    neighbors = {cdir: n for cdir, n in neighbors.items() if grid_at_time.get(n,'.') != '#'}
    return neighbors

def dijkstra(grid, mxy, mxx, t):
    start = (0,0)
    end = (mxy-1, mxx-1)
    grid_at_t = get_grid_at_t(grid, t, mxy=mxy, mxx=mxx)
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
        all_neighbors = get_neighbors(grid, u, t)
        for ndir, n in all_neighbors.items():
            alt = dist[u] + 1
            if alt < dist[n]:
                prev[n] = u
                dist[n] = alt
                hq.heappush(q, (alt, n))
    answer = dist[end]
    return dist, prev, answer

grid = parse_data(example_data,6,6)
print_grid(grid, 11, 7, 7)
# grid_at_t = get_grid_at_t(grid, 11, 7, 7)
# print_grid(grid_at_t, 11, 7, 7)
dist, prev, answer = dijkstra(grid, 7, 7, 12)

grid = parse_data(data, 70, 70)
dist, prev, part_one_answer = dijkstra(grid, 1024, 71, 71)