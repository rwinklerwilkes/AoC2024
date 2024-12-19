from aocd import get_data
from collections import defaultdict

data = get_data(day=11,year=2024)

def blink(stone):
    if stone == 0:
        return 1
    elif len(str(stone))%2 == 0:
        s = str(stone)
        return int(s[:len(s)//2]),int(s[len(s)//2:])
    else:
        return stone*2024

assert blink(0) == 1
assert blink(1000) == (10,0)
assert blink(999) == 2021976

def parse_data(data):
    parsed_data = defaultdict(int)
    for stone in data.split(' '):
        parsed_data[int(stone)] = 1
    return parsed_data

def part_one(data, num_rounds = 25):
    stones = parse_data(data)
    for _ in range(num_rounds):
        for stone, count in stones.copy().items():
            if count > 0:
                new_stone = blink(stone)
                stones[stone] -= count
                if isinstance(new_stone, tuple):
                    stones[new_stone[0]] += count
                    stones[new_stone[1]] += count
                else:
                    stones[new_stone] += count
    total_count = sum(stones.values())
    return stones, total_count


example_data = '125 17'
stones, part_one_example_answer = part_one(example_data,num_rounds=25)
assert part_one_example_answer == 55312

_, part_one_answer = part_one(data,num_rounds=25)
_, part_two_answer = part_one(data,num_rounds=75)