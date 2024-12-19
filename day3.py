from aocd import get_data
import re

data = get_data(day=3,year=2024)
example_data = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
part_two_example_data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def mul(x,y):
    return x*y

def extract_regex(instruction):
    mul_re = r'mul\(([0-9]+),([0-9]+)\)'
    all_matches = re.finditer(mul_re, instruction)
    all_matches_iterator = re.finditer(mul_re, instruction)
    return all_matches_iterator, [[int(i) for i in match.groups()] for match in all_matches]

def find_do_dont(instruction):
    do_re = r'do\(\)'
    dont_re = r"don't\(\)"
    do_idx = [dm.span()[0] for dm in re.finditer(do_re, instruction)]
    dont_idx = [dm.span()[0] for dm in re.finditer(dont_re, instruction)]
    all_idx = [(i,True) for i in do_idx] + [(i,False) for i in dont_idx]
    return all_idx

def part_one(data):
    _, parsed_matches = extract_regex(data)
    answer = sum(mul(*a) for a in parsed_matches)
    return answer

def part_two(data):
    all_matches, match_idx = extract_regex(data)
    all_do_dont = find_do_dont(data)

    total = 0
    for i, m in enumerate(all_matches):
        start = m.span()[0]
        do_dont = [i for i in all_do_dont if i[0] < start]
        if do_dont:
            do_dont = sorted(do_dont, key=lambda x: x[0])
            last_do_dont = do_dont[-1]
            include = last_do_dont[1] * 1
        else:
            include = 1
        total += mul(*match_idx[i]) * include
    return total


part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)

part_two_example_answer = part_two(part_two_example_data)
part_two_answer = part_two(data)