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

def print_grid(grid, t, mxh, mxw):
    b = [['_' for v in range(mxw)] for h in range(mxh)]
    for k,v in grid.items():
        is_valid = k[1] >= 0 and k[1] < mxh and k[2] >= 0 and k[2] < mxw
        if k[0] < t and is_valid:
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

def dijkstra(grid, mxw, mxh, t):
    start = (0,0)
    end = (mxw, mxh)
    dist = defaultdict(int)
    for k,_ in grid.items():
        if k[0] < t:
            dist[(k[1],k[2])] = np.inf
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
    return dist, prev

grid = parse_data(example_data,6,6)
print_grid(grid, 11, 7, 7)

d, p = dijkstra(grid, 7, 7, 11)