from aocd import get_data
import numpy as np

data = get_data(day=6,year=2024)

example_data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def parse_data(data):
    output = []
    start = None
    for x, row in enumerate(data.split('\n')):
        current_row = []
        for y, val in enumerate(row):
            if val == '^':
                start = np.array((x, y))
            current_row.append(val)
        output.append(current_row)
    return np.array(output), start

def move(data: np.ndarray, position: np.ndarray, direction: int):
    direction_map = [(-1,0),(0,1),(1,0),(0,-1)] #up, right, down, left
    direction_map = [np.array(i) for i in direction_map]
    # Check for running into a block
    done = False
    ict = 0
    new_position = position
    while not done and ict < 4:
        # Determine new position and direction
        new_position = position + direction_map[direction]
        new_x = new_position[0]
        new_y = new_position[1]
        if new_x < 0 or new_x >= data.shape[0] or new_y < 0 or new_y >= data.shape[1]:
            done = True
            direction = -1
        elif data[new_x, new_y] != '#':
            done = True
            #No need to update direction - keep going the way we were already going
        else:
            direction += 1
            direction %= len(direction_map)
            ict += 1
    # Check for out of bounds
    if direction == -1:
        return new_position, -1
    else:
        return new_position, direction

def part_one(data):
    parsed_data, start = parse_data(data)

    visited = set()
    pos = start
    dir = 0
    while dir != -1:
        visited.add(tuple(pos))
        pos, dir = move(parsed_data, pos, dir)
    answer = len(visited)
    return answer

def part_two(data):
    parsed_data, start = parse_data(data)

    visited = set()

    pos = start
    dir = 0
    while dir != -1:
        visited.add(tuple(pos))
        pos, dir = move(parsed_data, pos, dir)

    number_of_loops = 0
    for t in visited:
        pos = start
        dir = 0

        prior_states = set()
        new_visited = set()
        is_loop = False
        parsed_data_obstructed = parsed_data.copy()
        parsed_data_obstructed[t[0],t[1]] = '#'
        while dir != -1 and not is_loop:
            cur_pos = tuple(pos)
            cur_state = cur_pos + tuple([dir])
            if cur_state in prior_states:
                is_loop = True
            new_visited.add(cur_pos)
            prior_states.add(cur_state)
            pos, dir = move(parsed_data_obstructed, pos, dir)
        if is_loop:
            number_of_loops += 1

    answer = number_of_loops
    return answer

part_one_example_answer = part_one(example_data)
assert part_one_example_answer == 41
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
assert part_two_example_answer == 6
part_two_answer = part_two(data)