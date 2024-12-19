from aocd import get_data
import numpy as np

data = get_data(day=2, year=2024)
example_data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

def parse_data(data):
    return [[int(i) for i in line.split(' ')] for line in data.split('\n')]

def determine_safe(report):
    diff = [report[i]-report[i-1] for i in range(1,len(report))]
    same_sign = (np.min(np.sign(diff))==np.max(np.sign(diff)))
    abs_diff = np.abs(diff)
    meets_diff = (np.min(abs_diff) >= 1 and np.max(abs_diff) <= 3)
    return same_sign and meets_diff

def part_one(data):
    safe_reports = 0
    parsed_data = parse_data(data)
    for report in parsed_data:
        if determine_safe(report):
            safe_reports += 1
    return safe_reports

def part_two(data):
    safe_reports = 0
    parsed_data = parse_data(data)
    for report in parsed_data:
        if determine_safe(report):
            safe_reports += 1
        else:
            now_safe = False
            for i in range(len(report)):
                now_check = report[:i] + report[i+1:]
                if determine_safe(now_check):
                    now_safe = True
                    break
            safe_reports += 1*now_safe
    return safe_reports

part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
part_two_answer = part_two(data)