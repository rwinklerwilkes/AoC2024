from aocd import get_data

data = get_data(day=24, year=2024)
example_data = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

def and_gate(x,y):
    return x&y

def or_gate(x,y):
    return x|y

def xor_gate(x,y):
    return x^y

def parse_data(data):
    gates = {}
    fns = {'AND':'and_gate', 'OR': 'or_gate', 'XOR': 'xor_gate'}
    starting_values, all_gates = data.split('\n\n')
    for row in starting_values.split('\n'):
        register, val = row.split(': ')
        val = int(val)
        gates[register] = f'lambda: {val}'

    for g in all_gates.split('\n'):
        left, right = g.split(' -> ')
        l, op, r = left.split(' ')
        op = fns[op]
        gates[right] = f'lambda: {op}({l}(),{r}())'
    return gates

def add_gates_to_namespace(gates, num_gates):
    for k,v in gates.items():
        exec(f'{k}={v}',globals())

    output = []
    for i in range(45, -1, -1):
        output.append(str(eval(f'z{i:02}()')))
    answer = int(''.join(output), 2)
    return answer

def part_one(data):
    gates = parse_data(data)
    answer = add_gates_to_namespace(gates, 45)
    return answer

part_one_answer = part_one(data)