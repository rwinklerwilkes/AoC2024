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

already_seen = {}
def can_make(available_towels:list, target:str):
    if target in already_seen:
        return already_seen[target]

    ways = 0
    if len(target) == 0:
        ways = 1

    for towel in available_towels:
        if target.startswith(towel):
            ways += can_make(available_towels, target[len(towel):])
    already_seen[target] = ways
    return ways

#Read through code at https://github.com/jonathanpaulson/AdventOfCode/blob/master/2024/19.py to understand
at, dp = parse_data(example_data)
can_make(at, 'brwrr')