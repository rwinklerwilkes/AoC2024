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

part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)