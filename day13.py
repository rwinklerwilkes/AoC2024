from aocd import get_data
import re
from sympy.solvers import solve
from sympy import Symbol, Eq
from sympy import Matrix, solve_linear_system
from sympy.abc import x, y
from sympy.core.numbers import Integer as sympint

data = get_data(day=13,year=2024)
example_data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


A = Symbol('A')
B = Symbol('B')
eq1 = Eq(94 * A + 22 * B, 8400)
eq2 = Eq(34 * A + 67 * B, 5400)
output = solve([eq1,eq2],A,B,dict=False)

eq1 = Eq(26 * A + 67 * B, 12748)
eq2 = Eq(66 * A + 21 * B, 12176)
output = solve([eq1,eq2],x,y,dict=True)

def parse_data(data):
    parsed_data = []
    for system in data.split('\n\n'):
        a,b,prize = system.split('\n')
        button_regex = r'Button [AB]: X\+([0-9]+), Y\+([0-9]+)'
        prize_regex = r'Prize: X\=([0-9]+), Y\=([0-9]+)'
        a = [int(i) for i in re.match(button_regex, a).groups()]
        b = [int(i) for i in re.match(button_regex, b).groups()]
        prize = [int(i) for i in re.match(prize_regex, prize).groups()]
        parsed_data.append(list(zip(a,b,prize)))
    return parsed_data

def solve_system(system):
    m = Matrix(system)
    output = solve_linear_system(m,x,y)
    if len(output) == 0:
        return False, None, None
    else:
        fixed_dict = {'A':output[x],'B':output[y]}
        if not isinstance(fixed_dict['A'],sympint) or not isinstance(fixed_dict['B'],sympint) :
            return False, None, None
        else:
            return True, fixed_dict, fixed_dict['A']*3+fixed_dict['B']*1

def get_answer(data, part_two=False):
    parsed_data = parse_data(data)
    total_cost = 0
    for system in parsed_data:
        system_to_use = system
        if part_two:
            system_to_use = [(i[0],i[1],i[2]+10000000000000) for i in system]
        is_solvable, solution, cost = solve_system(system_to_use)
        if is_solvable:
            total_cost += cost
    return total_cost

part_one_example_answer = get_answer(example_data)
assert part_one_example_answer == 480
part_one_answer = get_answer(data)

part_two_example_answer = get_answer(example_data,part_two=True)
part_two_answer = get_answer(data,part_two=True)

