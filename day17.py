from aocd import get_data

data = get_data(day=17,year=2024)

class Program:
    def __init__(self, a, b, c):
        self.registers = {
            'A':a,
            'B':b,
            'C':c
        }
        self.instruction_pointer = 0
        self.output = []

    def combo_operand(self, val):
        return_value = None
        if val in [0,1,2,3]:
            return_value = val
        elif val in [4,5,6]:
            return_value = [self.registers[ch] for ch in ['A','B','C']][val-4]
        elif val == 7:
            raise AssertionError('Combo operand 7 is not valid')
        return return_value

    def dv(self, operand, register):
        numerator = self.registers['A']
        denominator = 2**self.combo_operand(operand)
        self.registers[register] = numerator//denominator
        increment = True
        return increment

    def adv(self, operand):
        return self.dv(operand, 'A')

    def bxl(self, operand):
        new_b = self.registers['B'] ^ operand
        self.registers['B'] = new_b
        increment = True
        return increment

    def bst(self, operand):
        combo_operand = self.combo_operand(operand)
        self.registers['B'] = combo_operand % 8
        increment = True
        return increment

    def jnz(self, operand):
        increment = True
        if self.registers['A'] != 0:
            self.instruction_pointer = operand
            increment = False
        return increment

    def bxc(self, operand):
        increment = True
        bxc = self.registers['B'] ^ self.registers['C']
        self.registers['B'] = bxc
        return increment

    def out(self, operand):
        increment = True
        combo_operand = self.combo_operand(operand)
        self.output.append(combo_operand % 8)
        return increment

    def bdv(self, operand):
        return self.dv(operand, 'B')

    def cdv(self, operand):
        return self.dv(operand, 'C')

    def run_program(self, instructions):
        valid_inst = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]
        done = False
        while not done:
            inst = instructions[self.instruction_pointer]
            inst_fn = valid_inst[inst]
            op = instructions[self.instruction_pointer + 1]
            increment = inst_fn(op)
            if increment:
                self.instruction_pointer += 2
            if self.instruction_pointer >= len(instructions):
                done = True
        out_str = [str(i) for i in self.output]
        print(','.join(out_str))

p = Program(729,0,0)
p.run_program([0,1,5,4,3,0])

#Part one answer
p = Program(30118712,0,0)
p.run_program([2,4,1,3,7,5,4,2,0,3,1,5,5,5,3,0])

#Part two
p = Program(117440,0,0)
p.run_program([0,3,5,4,3,0])