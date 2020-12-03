"""CPU functionality."""

import sys

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

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        while self.isRunning:
            instruction = self.ram_read(self.pc)

            LDI = 0b10000010
            HLT = 0b00000001
            PRN = 0b01000111


            if instruction == LDI:
                # op === operation
                op_1 = self.ram_read(self.pc + 1)
                op_2 = self.ram_read(self.pc + 2)

                self.reg[op_1] = op_2
                self.pc += 3

            if instruction == PRN:
                op_1 = self.ram_read(self.pc + 1)
                print(self.reg[op_1])
                self.pc += 2

            if instruction == HLT:
                self.isRunning = False;
                self.pc += 1;
