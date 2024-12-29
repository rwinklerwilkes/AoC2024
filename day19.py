from aocd import get_data

data = get_data(day=19,year=2024)
example_data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

def parse_data(data):
    atw, pat = data.split('\n\n')
    available_towels = atw.split(', ')
    desired_patterns = pat.split('\n')
    return available_towels, desired_patterns

def can_make(already_seen:dict, available_towels:list, target:str):
    if target in already_seen:
        return already_seen, already_seen[target]

    ways = 0
    if len(target) == 0:
        ways = 1

    for towel in available_towels:
        if target.startswith(towel):
            ns, way = can_make(already_seen, available_towels, target[len(towel):])
            for k,v in ns.items():
                already_seen[k] = v
            ways += way
    already_seen[target] = ways
    return already_seen, ways

#Read through code at https://github.com/jonathanpaulson/AdventOfCode/blob/master/2024/19.py to understand
def get_answer(data):
    available_towels, desired_patterns = parse_data(data)
    answer = 0
    answer_part_two = 0
    for pattern in desired_patterns:
        s, num = can_make({}, available_towels, pattern)
        if num > 0:
            answer += 1
            answer_part_two += num
    return answer, answer_part_two

part_one_example_answer = part_one(example_data)
part_one_answer, part_two_answer = get_answer(data)