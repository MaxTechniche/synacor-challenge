import time
import sys

def main():
    vm = VM()
    vm.read()
    vm.run()

class VM:
    def __init__(self) -> None:
        self.memory = []
        self.register = [0] * 8
        self.stack = []
        self.pos = 0
        self.op = {
            '0': self.op_0,
            '1': self.op_1,
            '2': self.op_2,
            '3': self.op_3,
            '4': self.op_4,
            '5': self.op_5,
            '6': self.op_6,
            '7': self.op_7,
            '8': self.op_8,
            '9': self.op_9,
            '10': self.op_10,
            '11': self.op_11,
            '12': self.op_12,
            '13': self.op_13,
            '14': self.op_14,
            '15': self.op_15,
            '16': self.op_16,
            '17': self.op_17,
            '18': self.op_18,
            '19': self.op_19, 
            '20': self.op_20,
            '21': self.op_21
        }
        
    def read(self, file_path: str=None) -> bool:
        if not file_path:
            file_path = 'challenge.bin'

        # Expand 2 bytes to 1 little-endian pair
        def expand_bytes(low, high):
            low = bin(low)[2:].zfill(8)
            high = bin(high)[2:].zfill(8)
            bin_num = high + low
            num = int(bin_num, 2)
            return num

        # Parse File
        with open(file_path, 'rb') as b:
            while True:
                low = None
                high = None
                for i in b.read(2):
                    if low == None:
                        low = i
                    elif high == None:
                        high = i
                if low == None and high == None:
                    break
                self.memory.append(expand_bytes(low, high))

    def run(self) -> None:
        while True:
            num = self.memory[self.pos]
            
            if str(num) not in self.op:
                print(num)
                break

            self.op[str(num)]()
            
            
    def op_0(self) -> None:
        sys.exit(0)

    def op_1(self) -> None:
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        self.register[a] = b
        self.pos += 3

    def op_2(self) -> None:
        a = self.memory[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        
        self.stack.append(a)
        self.pos += 2

    def op_3(self) -> None:
        a = self.memory[self.pos + 1]
        if a >= 32768:
            self.register[a % 32768] = self.stack.pop()
        else:
            self.memory[a] = self.stack.pop()
        self.pos += 2

    def op_4(self) -> None:
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.memory[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        if b == c:
            self.register[a] = 1
        else:
            self.register[a] = 0
        
        self.pos += 4

    def op_5(self) -> None:
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.memory[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        if b > c:
            self.register[a] = 1
        else:
            self.register[a] = 0
        
        self.pos += 4
   
    def op_6(self) -> None:
        a = self.memory[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        self.pos = a
        
    def op_7(self) -> None:
        # self.pos += 1
        # num = self.memory[self.pos]
        # if num >= 32768:
        #     num %= 32768
        #     if self.register[num] != 0:
        #         self.pos = self.memory[self.pos+1]
        #         return
        # else:
        #     if self.memory[self.pos] != 0:
        #         self.pos = self.memory[self.pos+1]
        #         return
        # self.pos += 2
        
        a = self.memory[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        
        if a != 0:
            self.pos = b
            return
        self.pos += 3
        
    def op_8(self) -> None:
        # self.pos += 1
        # num = self.memory[self.pos]
        # if num >= 32768:
        #     num %= 32768
        #     if self.register[num] == 0:
        #         self.pos = self.memory[self.pos+1]
        #         return
        # else:
        #     if self.memory[self.pos] == 0:
        #         self.pos = self.memory[self.pos+1]
        #         return
            
        # self.pos += 2
        
        a = self.memory[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        
        if a == 0:
            self.pos = b
            return
        self.pos += 3
        
    def op_9(self) -> None:
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.memory[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = (b + c) % 32768
        
        self.pos += 4
        
    def op_10(self) -> None:
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.memory[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = (b * c) % 32768
        
        self.pos += 4
        
    def op_11(self) -> None:
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.memory[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = b % c
        
        self.pos += 4
            
    def op_12(self) -> None:
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.memory[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = b & c
        
        self.pos += 4
        
    def op_13(self) -> None:
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.memory[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = b | c
        
        self.pos += 4
        
    def op_14(self) -> None:
        inverse = {
            '0': '1',
            '1': '0'
        }
        a = self.memory[self.pos + 1] % 32768
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        
        b = bin(b)[2:].zfill(15)
        b = ''.join(inverse[x] for x in b)
        b = int(b, 2)
        self.register[a] = b
        
        self.pos += 3
        
    def op_15(self) -> None:
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        a = self.memory[self.pos + 1]
        if a >= 32768:
            self.register[a % 32768] = self.memory[b]
        else:
            self.memory[a] = self.memory[b]
            
        self.pos += 3
        
    def op_16(self) -> None:
        b = self.memory[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
            
        a = self.memory[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        self.memory[a] = b
            
        self.pos += 3
         
    def op_17(self) -> None:
        self.stack.append(self.pos+2)
        
        a = self.memory[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        self.pos = a
        
    def op_18(self) -> None:
        val = self.stack.pop()
        self.pos = val
    
    def op_19(self) -> None:
        self.pos += 1
        a = self.memory[self.pos]
        if a >= 32768:
            a = self.register[a % 32768]
            char = chr(a)
        else:
            char = chr(self.memory[self.pos])
        print(char, end='')
        self.pos += 1
        
    def op_20(self) -> None:
        a = self.memory[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        self.memory[a] = ord(input())
        self.pos += 2
            
    def op_21(self) -> None:
        self.pos += 1
    
    
if __name__ == '__main__':
    main()