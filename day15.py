from aocd import get_data

data = get_data(day=15,year=2024)
example_data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

def tadd(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def tminus(t1, t2):
    return (t1[0]-t2[0], t1[1]-t2[1])

def tmult(t1, i):
    return (t1[0]*i, t1[1]*i)

def parse_data(data):
    map_to_use, directions = data.split('\n\n')
    directions = [c for c in directions if c!='\n']
    grid = {}
    mxh = len(map_to_use.split('\n'))
    mxw = len(map_to_use.split('\n')[0])
    start_pos = None
    for i, row in enumerate(map_to_use.split('\n')):
        for j,val in enumerate(row):
            if val == '@':
                start_pos = (i,j)
            grid[(i,j)] = val
    return grid, start_pos, mxh, mxw, directions

def expand_map(grid, mxh, mxw):
    new_grid = {}
    for i in range(mxh):
        for j in range(mxw):
            new_j = j*2
            if grid[(i,j)] == '#':
                new_grid[(i,new_j)] = '#'
                new_grid[(i,new_j+1)] = '#'
            elif grid[(i,j)] == 'O':
                new_grid[(i,new_j)] = '['
                new_grid[(i,new_j+1)] = ']'
            elif grid[(i,j)] == '.':
                new_grid[(i,new_j)] = '.'
                new_grid[(i,new_j+1)] = '.'
            elif grid[(i,j)] == '@':
                new_grid[(i,new_j)] = '@'
                new_start_pos = (i,new_j)
                new_grid[(i,new_j+1)] = '.'
    return new_grid, new_start_pos

def print_grid(grid, mxh, mxw):
    b = [['_' for v in range(mxw)] for h in range(mxh)]
    for k,v in grid.items():
        b[k[0]][k[1]] = v
    output_board = '\n'.join(''.join(row) for row in b)
    print(output_board)

def move(grid, pos, dir):
    new_grid = grid.copy()
    dir_map = {'<':(0,-1),'^':(-1,0),'>':(0,1),'v':(1,0)}
    step_to_use = dir_map[dir]
    done = False
    moves = [(pos, pos)]
    cur_pos = pos
    while not done:
        step = tadd(cur_pos, step_to_use)
        next_pos = grid[step]
        if next_pos == '.':
            moves = [(p, tadd(i, step_to_use)) for p,i in moves]
            done = True
        elif next_pos == 'O':
            moves.append((step,step))
        elif next_pos == '#':
            #stop
            done = True
        cur_pos = step

    new_locations = [m[1] for m in moves]
    for orig, new in moves:
        orig_val = grid[orig]
        new_grid[new] = orig_val
        if orig not in new_locations:
            new_grid[orig] = '.'
    new_pos = moves[0][1]
    return new_grid, new_pos

def move_second_part(grid, pos, dir):
    new_grid = grid.copy()
    dir_map = {'<':(0,-1),'^':(-1,0),'>':(0,1),'v':(1,0)}
    step_to_use = dir_map[dir]
    swap = []
    stack = [pos]
    new_pos = pos
    dont_swap = False
    while stack:
        t = stack.pop()
        if grid[t] == '#':
            dont_swap = True
            break
        elif grid[t] == '.':
            continue
        t = tadd(t, step_to_use)
        swap.append(t)
        stack.append(t)
        if step_to_use[0] and grid[t] == '[':
            stack.append((t[0],t[1]+1))
        if step_to_use[0] and grid[t] == ']':
            stack.append((t[0],t[1]-1))
    done = set()
    if not dont_swap:
        for new_pos in swap[::-1]:
            if new_pos in done:
                continue
            done.add(new_pos)
            prev_pos = tminus(new_pos,step_to_use)
            new_grid[new_pos], new_grid[prev_pos] = new_grid[prev_pos], new_grid[new_pos]
    return new_grid, new_pos


def score_grid(grid):
    score = 0
    for pos, val in grid.items():
        if val == 'O':
            score += 100*pos[0] + pos[1]
        elif val == '[':
            score += 100*pos[0] + pos[1]
    return score

def part_one(data):
    grid, start_pos, mxh, mxw, directions = parse_data(data)
    # print_grid(grid, mxh, mxw)

    new_grid, new_pos = grid, start_pos
    for d in directions:
        new_grid, new_pos = move(new_grid, new_pos, d)
        # print_grid(new_grid, mxh, mxw)
    answer = score_grid(new_grid)
    return new_grid, mxh, mxw, answer

# new_grid, mxh, mxw, part_one_example_answer = part_one(example_data)
# _, _, _, part_one_answer = part_one(data)
#

def part_two(data):
    grid, start_pos, mxh, mxw, directions = parse_data(data)
    p2_grid, p2_start_pos = expand_map(grid, mxh, mxw)
    new_grid, new_pos = p2_grid, p2_start_pos
    for d in directions:
        new_grid, new_pos = move_second_part(new_grid, new_pos, d)
    answer = score_grid(new_grid)
    return new_grid, mxh, mxw*2, answer

example_data_part_two = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

new_grid, mxh, mxw, part_two_example_answer = part_two(example_data_part_two)
_, _, _, part_two_answer = part_two(data)