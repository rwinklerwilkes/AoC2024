from aocd import get_data

data = get_data(day=22, year=2024)
example_data = """1
10
100
2024"""

example_data_part_two = """1
2
3
2024"""

def parse_data(data):
    return [int(i) for i in data.split('\n')]

def mix(secret, mixin):
    return secret ^ mixin

def prune(secret):
    return secret % 16777216

def get_next(secret):
    mixin = secret * 64
    secret = mix(secret, mixin)
    secret = prune(secret)
    mixin = secret // 32
    secret = mix(secret, mixin)
    secret = prune(secret)
    mixin = secret * 2048
    secret = mix(secret, mixin)
    secret = prune(secret)
    return secret

def part_one(data):
    answer = 0

    parsed_data = parse_data(data)
    for buyer in parsed_data:
        current = buyer
        for i in range(2000):
            current = get_next(current)
        answer += current
    return answer

def part_two(data):
    parsed_data = parse_data(data)

    last = []
    all_buyer_dicts = []
    all_sequences = set()
    for buyer in parsed_data:
        current = buyer
        buyer_dict = {}
        for i in range(2000):
            next = get_next(current)
            next_ones = next % 10
            current_ones = current % 10
            last.append(next_ones - current_ones)
            if len(last) >= 4:
                last_four_changes = tuple(last[-4:])
                if last_four_changes not in buyer_dict:
                    buyer_dict[last_four_changes] = next_ones
                all_sequences.add(last_four_changes)
            current = next
        all_buyer_dicts.append(buyer_dict)

    max_sum = 0
    max_seq = None
    for cur_seq in all_sequences:
        sequence_sum = 0
        for b in all_buyer_dicts:
            sequence_sum += b.get(cur_seq, 0)
            if sequence_sum > max_sum:
                max_sum = sequence_sum
                max_seq = cur_seq
    return max_sum

part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data_part_two)
part_two_answer = part_two(data)