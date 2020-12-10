"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
PUSH = 0b01000101
POP = 0b01000110
SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256;        
        self.reg = [0] * 8;
        self.reg[7] = 0xF4                   #Random Access Memory
        self.pc = 0;                                    #Progress Counter
        self.ir = 0;                                    #Instruction Register
        self.mar = 0;                                   #Memory Address Register
        self.mdr = 0;                                   #Memory Data Register
        self.fr = 0;                                    #Flag Register
        self.isRunning = True;

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr



    def load(self):
        """Load a program into memory."""
        # print(sys.argv)
        # sys.exit(0)

        # # get file name from command line argument

        address = 0;
        
        if len(sys.argv) != 2:
            print("Usage: example_cpu.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    split = line.split('#')
                    value = split[0].strip()
                    print(value)

                    if value == '':
                        continue

                    val = int(value, 2)
                    self.ram_write(address, val)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
    
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB":
        #     self.reg[reg_a] -= self.reg[reg_b]
            
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "POP":
            
        # elif op == "PUSH":
        #     pass
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # op === operation

        while self.isRunning:
            instruction = self.ram_read(self.pc)
            op_1 = self.ram_read(self.pc + 1)
            op_2 = self.ram_read(self.pc + 2)

            if instruction == HLT:
                self.isRunning = False;
                self.pc += 1

            elif instruction == LDI:
                self.reg[op_1] = op_2
                self.pc += 3

            elif instruction == PRN:
                op_1 = self.ram_read(self.pc + 1)
                print(self.reg[op_1])
                self.pc += 2

            elif instruction == ADD:
                self.reg[op_1] += self.reg[op_2]

            elif instruction == SUB:
                self.reg[op_1] -= self.reg[op_2]
                
            elif instruction == MUL:
                self.reg[op_1] *= self.reg[op_2]
                self.pc += 3
            
            elif instruction == PUSH:
                self.reg[SP] -= 1
                reg_val = self.reg[op_1]
                top_val = self.reg[SP]
                self.ram[top_val] = reg_val;
                self.pc += 2

            elif instruction == POP:
                top_val = self.ram_read(self.reg[SP])
                self.reg[op_1] = top_val
                self.reg[SP] += 1
                self.pc += 2
                
                
            