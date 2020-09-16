"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.sp = 7
    
    
    def ram_read(self,address):
        '''
        Read the information at the index in the RAM
        '''
        return self.ram[address]
    
    
    def ram_write(self,value,address):
        '''
        Writes a value in ram given the specified index
        '''
        self.ram[address] = value    

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print('usage: ls8.py filename')
            sys.exit(1)
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()
                    if n == '':
                        continue
                    try:
                        n = '0b' + n
                        n = int(n,2)
                    except TypeError:
                        print(f'Number not valid {n}')
                        sys.exit(1)

                    self.ram_write(n,address)
                    address += 1
        except FileNotFoundError:
            print('file not found')
            sys.exit(2)                


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
        running = True
        # instructions!
        LDI = 0b10000010 
        PRN = 0b01000111
        MUL = 0b10100010
        HLT = 0b00000001
        PUSH = 0b01000101
        POP = 0b01000110

        
        while running:
            ir = self.ram[self.pc]
            
            
            if ir == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                self.pc +=3
            
            elif ir ==  PRN:
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])
                self.pc += 2
            
            elif ir ==  HLT:
                running = False

            elif ir == MUL:
                r1 = self.ram[self.pc + 1]
                r2 = self.ram[self.pc + 2]
                print(self.reg[r1] * self.reg[r2])
                self.pc += 3

            elif ir == POP:
                reg_num = self.ram[self.pc + 1]
                top_stack = self.reg[self.sp]

                value = self.ram[top_stack]
                self.reg[reg_num] = value
                self.reg[self.sp] += 1
                
                self.pc += 2
            
            elif  ir == PUSH:
                self.reg[self.sp] -= 1
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]


                top_stack = self.reg[self.sp]
                self.ram[top_stack] = value
                self.pc += 2






            
            else:
                print('unknown instruction')
                sys.exit(3)  


    




