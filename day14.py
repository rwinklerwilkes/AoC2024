from aocd import get_data
from collections import defaultdict
import numpy as np
import re

data = get_data(day=14,year=2024)
example_data = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''

class Robot:
    def __init__(self, p, v, w, h):
        self.p = p
        self.v = v
        self.board_size = np.array([w,h])

    def get_quadrant(self, t):
        cur_pos = self.determine_position(t)
        half_x = self.board_size[0]//2
        half_y = self.board_size[1]//2
        if cur_pos[0] == half_x or cur_pos[1] == half_y:
            quadrant = -1
        elif cur_pos[0] < half_x and cur_pos[1] < half_y:
            quadrant = 0
        elif cur_pos[0] > half_x and cur_pos[1] < half_y:
            quadrant = 1
        elif cur_pos[0] < half_x and cur_pos[1] > half_y:
            quadrant = 2
        else:
            quadrant = 3
        return quadrant, tuple(cur_pos)

    def determine_position(self, t):
        return (self.p + t * self.v) % self.board_size

def print_board(robots, t, w, h):
    board = defaultdict(int)
    for r in robots:
        board[tuple(r.determine_position(t))] += 1
    b = [['_' for i in range(w)] for j in range(h)]
    for k, v in board.items():
        b[k[1]][k[0]] = str(v)
    output_board = '\n'.join(''.join(row) for row in b)
    return output_board

def parse_data(data,mw,mh):
    robots = []
    for row in data.split('\n'):
        p,v = row.split(' ')
        rgx = r'[pv]\=(\-{0,1}[0-9]+),(\-{0,1}[0-9]+)'
        p_int = np.array([int(i) for i in re.match(rgx, p).groups()])
        v_int = np.array([int(i) for i in re.match(rgx, v).groups()])
        robots.append(Robot(p_int, v_int, mw, mh))
    return robots

def part_one(data,w,h):
    parsed_data = parse_data(data,w,h)
    quad = defaultdict(int)
    for robot in parsed_data:
        cur_quad, _ = robot.get_quadrant(100)
        quad[cur_quad] += 1
    safety_factor = 1
    # print(quad)
    for k,v in quad.items():
        if k != -1:
            safety_factor *= v
    return safety_factor

def part_two(data, w, h):
    parsed_data = parse_data(data,w,h)
    quad = defaultdict(int)
    done = False
    t = 0
    while not done:
        all_pos = set()
        all_unique = True
        for robot in parsed_data:
            cur_quad, cur_pos = robot.get_quadrant(t)
            if cur_pos in all_pos:
                all_unique = False
                break
            else:
                all_pos.add(cur_pos)
            quad[robot.get_quadrant(t)] += 1
        if all_unique:
            unique_time = t
            done = True
        t += 1
    answer = unique_time
    return answer

part_one_example_answer = part_one(example_data, 11, 7)
assert part_one_example_answer == 12
part_one_answer = part_one(data, 101, 103)

part_two_answer = part_two(data, 101, 103)