from aocd import get_data

data = get_data(day=15,year=2024)
example_data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########"""

def tadd(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def parse_data(data):
    grid = {}
    mxh = len(data.split('\n'))
    mxw = len(data.split('\n')[0])
    start_pos = None
    for i, row in enumerate(data.split('\n')):
        for j,val in enumerate(row):
            if val == '@':
                start_pos = (i,j)
            grid[(i,j)] = val
    return grid, start_pos, mxh, mxw

def print_grid(grid, mxh, mxw):
    b = [['_' for v in range(mxw)] for h in range(mxh)]
    for k,v in grid.items():
        b[k[0]][k[1]] = v
    output_board = '\n'.join(''.join(row) for row in b)
    print(output_board)

def move(grid, pos, dir):
    grid = grid.copy()
    dir_map = {'<':(0,-1),'^':(-1,0),'>':(0,1),'v':(1,0)}
    step_to_use = dir_map[dir]
    done = False
    steps = []
    cur_pos = pos
    while not done:
        step = tadd(cur_pos, step_to_use)
        next_pos = grid[step]
        if next_pos == 'O':
            steps.append(step)
            cur_pos = step
        elif next_pos == '.':
            #move everything in steps
            for s in reversed(steps):
                next_pos = tadd(s, step_to_use)
                grid[next_pos] = grid[s]
            grid[pos] = '.'
        elif next_pos == '#':
            #stop
            done = True
    return grid, next_pos

grid, start_pos, mxh, mxw = parse_data(example_data)
new_grid, new_pos = move(grid, start_pos, '<')
print(print_grid(grid, mxh, mxw))
print(print_grid(new_grid, mxh, mxw))