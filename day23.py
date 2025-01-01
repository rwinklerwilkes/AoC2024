from aocd import get_data
import networkx as nx

data = get_data(day=23, year=2024)
example_data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

def parse_data(data):
    g = nx.Graph()
    for row in data.split('\n'):
        left, right = row.split('-')
        g.add_edge(left, right)
    return g

def part_one(data):
    parsed_data = parse_data(data)
    cliques = nx.enumerate_all_cliques(parsed_data)
    answer = 0
    for clq in cliques:
        if len(clq) == 3 and any([s.startswith('t') for s in clq]):
            answer += 1
    return answer

def part_two(data):
    parsed_data = parse_data(data)
    cliques = list(nx.enumerate_all_cliques(parsed_data))
    max_clique = cliques[-1]
    answer = ','.join(sorted(max_clique))
    return answer


part_one_example_answer = part_one(example_data)
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
part_two_answer = part_two(data)