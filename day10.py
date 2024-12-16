from aocd import get_data

data = get_data(day=10,year=2024)
example_data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

def parse_data(data):
    parsed_data = {}
    for i, row in enumerate(data.split('\n')):
        for j, val in enumerate(row):
            parsed_data[(i,j)] = int(val)
    return parsed_data

def tadd(t1,t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def find_answer(parsed_data, trailhead, part_two = False):
    s = [trailhead]
    seen = set()
    ans = 0
    while s:
        cur = s.pop()
        if cur not in seen:
            if not part_two:
                seen.add(cur)
            #Found an answer
            if parsed_data[cur] == 9:
                ans += 1
            for n in [(-1,0),(1,0),(0,1),(0,-1)]:
                next = tadd(cur, n)
                if next in parsed_data and parsed_data[next] == parsed_data[cur] + 1:
                    s.append(next)
    return ans

def part_one(data):
    parsed_data = parse_data(data)
    trailheads = [k for k,v in parsed_data.items() if v == 0]
    answer = 0
    for t in trailheads:
        answer += find_answer(parsed_data, t)
    return answer

def part_two(data):
    parsed_data = parse_data(data)
    trailheads = [k for k,v in parsed_data.items() if v == 0]
    answer = 0
    for t in trailheads:
        answer += find_answer(parsed_data, t, part_two=True)
    return answer

part_one_example_answer = part_one(example_data)
assert part_one_example_answer == 36
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
assert part_one_example_answer == 36
part_two_answer = part_two(data)