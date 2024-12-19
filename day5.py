from aocd import get_data
from collections import defaultdict

data = get_data(day=5,year=2024)
example_data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def parse_data(data):
    rules = defaultdict(list)
    relationships, lists = data.split('\n\n')
    for r in relationships.split('\n'):
        prior, next = [int(i) for i in r.split('|')]
        rules[prior].append(next)
    return rules, lists
def determine_rules_pass(rules, rule_order):
    passes = True
    for i, r in enumerate(rule_order):
        next_items = rules[r]
        priors = rule_order[:i]
        bad_rules = [i for i in priors if i in next_items]
        if bad_rules:
            passes=False
            break
    return passes

def part_one(data):
    rules, lists = parse_data(data)
    answer = 0
    for rule_str in lists.split('\n'):
        rule_order = [int(i) for i in rule_str.split(',')]
        passes = determine_rules_pass(rules, rule_order)
        if passes:
            answer += rule_order[len(rule_order) // 2]
    return answer

def part_two(data):
    rules, lists = parse_data(data)
    answer = 0
    for rule_str in lists.split('\n'):
        rule_order = [int(i) for i in rule_str.split(',')]
        passes = determine_rules_pass(rules, rule_order)
        if not passes:
            # print(rule_str)
            rule_order = sorted(rule_order, key=lambda rule: -len([after for after in rules[rule] if after in rule_order]))
            answer += rule_order[len(rule_order) // 2]
    return answer


part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
part_two_answer = part_two(data)