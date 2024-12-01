from aocd import get_data
from collections import Counter

data = get_data(day=1,year=2024)
example_data ="""3   4
4   3
2   5
1   3
3   9
3   3"""

def parse_data(data):
    left = []
    right = []
    for line in data.split('\n'):
        left_int, right_int = [int(i) for i in line.split('   ')]
        left.append(left_int)
        right.append(right_int)
    left = sorted(left)
    right = sorted(right)
    return left, right

def difference(sorted_list_left, sorted_list_right):
    diff = [abs(sorted_list_left[i]-sorted_list_right[i]) for i in range(len(sorted_list_left))]
    diff = sum(diff)
    return diff

def sum_product(left, right):
    c = Counter(right)
    total = 0
    for i, num in enumerate(left):
        total += num * c[num]
    return total

def part_one(data):
    left, right = parse_data(data)
    return difference(left, right)

def part_two(data):
    left, right = parse_data(data)
    return sum_product(left, right)

part_one_example_answer = part_one(example_data)
assert part_one_example_answer == 11
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
assert part_two_example_answer == 31
part_two_answer = part_two(data)