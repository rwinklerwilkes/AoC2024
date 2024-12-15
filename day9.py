from aocd import get_data

example_data = '2333133121414131402'
data = get_data(day=9,year=2024)

class Memory:
    def __init__(self, pos, len, id):
        self.pos = pos
        self.len = len
        self.id = id

    def value(self):
        #Derived from formula for triangular numbers, subtracting 1 through pos-1 from 1 through pos + len - 1
        return (self.len*self.len + 2*self.len*self.pos - self.len)//2

    def __repr__(self):
        return f'Pos: {self.pos}, Len: {self.len}, ID: {self.id}'

def parse_data(data):
    used_memory = []
    free_memory = []
    pos = 0
    cur_group = 0
    for i, len in enumerate(data):
        if i%2==1:
            group_to_use = None
            free_memory.append(Memory(pos, int(len), group_to_use))
        else:
            group_to_use = cur_group
            used_memory.append(Memory(pos, int(len), group_to_use))
            cur_group += 1
        pos += int(len)
    return used_memory, free_memory

def print_board(used_memory, free_memory):
    memory = used_memory + free_memory
    max_needed = max(m.pos + m.len for m in memory)
    board = ['.' for i in range(max_needed)]
    for m in memory:
        for i in range(m.pos,m.pos+m.len):
            if m.id is not None:
                board[i] = str(m.id)
            else:
                board[i] = '.'
    return ''.join(board)



for used in used_memory:
    for free in free_memory:
        #Below for part 2
        if used.pos >= free.pos and free.len >= used.len:
            #Shift used position to free position
            used.pos = free.pos
            #Remove any used space from used and add it to free's position
            free.pos += used.len
            #Reduce the amount of available free space
            free.len -= used.len

def shift_memory(used_memory, free_memory):
    new_memory = []
    for used in used_memory[::-1]:
        can_move_left = [i for i, m in enumerate(free_memory) if m.pos < used.pos]
        while can_move_left:
            i = can_move_left[0]
            f = free_memory[i]
            if used.len < f.len:
                # Shorter, use all space
                used.pos = f.pos
                f.pos += used.len
                f.len -= used.len
                can_move_left = []
            elif used.len == f.len:
                # Same size, use all space but delete f from free_memory
                used.pos = f.pos
                free_memory.pop(i)
                can_move_left = []
            elif used.len > f.len:
                # Longer, use all space then figure out what to do next
                f.id = used.id
                used.len -= f.len
                new_memory.append(free_memory.pop(i))
                can_move_left = [i for i, m in enumerate(free_memory) if m.pos < used.pos]

    all_memory = used_memory + free_memory + new_memory
    return all_memory

def part_one(data):
    used_memory, free_memory = parse_data(data)
    all_memory = shift_memory(used_memory, free_memory)
    answer = 0
    for a in all_memory:
        if a.id is not None:
            answer += a.value() * a.id
    return answer

def part_two(data):
    used_memory, free_memory = parse_data(data)
    for used in used_memory[::-1]:
        for free in free_memory:
            # Below for part 2
            if used.pos >= free.pos and free.len >= used.len:
                # Shift used position to free position
                used.pos = free.pos
                # Remove any used space from used and add it to free's position
                free.pos += used.len
                # Reduce the amount of available free space
                free.len -= used.len
    answer = 0
    for a in used_memory:
        if a.id is not None:
            answer += a.value() * a.id
    return answer

part_one_example_answer = part_one(example_data)
assert part_one_example_answer == 1928
part_one_answer = part_one(data)

part_two_example_answer = part_two(example_data)
assert part_two_example_answer == 2858
part_two_answer = part_two(data)
