from aocd import get_data
from infix import shift_infix as infix
from operator import add, mul
import itertools

data = get_data(day=7,year=2024)
example_data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def parse_data(data):
    parsed_data = []
    for row in data.split('\n'):
        left, right = row.split(': ')
        equal_to = int(left)
        values = [int(i) for i in right.split(' ')]
        parsed_data.append((equal_to,values))
    return parsed_data


def reduce_test_equation(test):
    assert len(test) >= 3
    assert len(test)%2==1
    if len(test) == 3:
        return eval(''.join(test))
    else:
        first = eval(''.join(test[:3]))
        rest = test[3:]
        return reduce_test_equation([str(first)] + rest)

def test_equation(equal_to, values):
    passes = False
    n = len(values) - 1
    for p in itertools.product(['+','*'], repeat=n):
        full_test = [str(x) for y in itertools.zip_longest(values, p, fillvalue=None) for x in y if x]
        if equal_to == reduce_test_equation(full_test):
            passes = True
            break
    if passes:
        return equal_to
    else:
        return 0

def part_one(data):
    parsed_data = parse_data(data)
    total_pass = 0
    for equal_to, values in parsed_data:
        total_pass += test_equation(equal_to, values)
    return total_pass

@infix
def cat(a, b): return int(f"{a}{b}")

def test_equation_part_two(equal_to, values):
    start, *rest = values
    full_set = [start]
    for right in rest:
        full_set = [op(left, right) for left in full_set for op in (add, mul, cat)]
    if equal_to in full_set:
        return equal_to
    else:
        return 0

def part_two(data):
    parsed_data = parse_data(data)
    total_pass = 0
    for equal_to, values in parsed_data:
        total_pass += test_equation_part_two(equal_to, values)
    return total_pass



part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
part_two_answer = part_two(data)