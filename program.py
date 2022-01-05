import time
import sys

def main():
    vm = VM()
    vm.read()
    vm.run()

class VM:
    def __init__(self) -> None:
        self.memory = {}
        self.register = [0] * 8
        self.stack = []
        self.pos = 0
        self.input = []
        
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
                self.input.append(expand_bytes(low, high))

    def run(self) -> None:
        while True:
            num = self.input[self.pos]
            
            if num == 0:
                self.op_0()
            elif num == 1:
                self.op_1()
            elif num == 2:
                self.op_2()
            elif num == 3:
                self.op_3()
            elif num == 4:
                self.op_4()
            elif num == 5:
                self.op_5()
            elif num == 6:
                self.op_6()
            elif num == 7:
                self.op_7()
            elif num == 8:
                self.op_8()
            elif num == 9:
                self.op_9()
            elif num == 10:
                self.op_10()
                
            elif num == 12:
                self.op_12()
            elif num == 13:
                self.op_13()
            elif num == 14:
                self.op_14()
                
            elif num == 17:
                self.op_17()
                
            elif num == 19:
                self.op_19()
                
            elif num == 21:
                self.op_21()
        
            else:
                print(num)
                break

    def op_0(self) -> None:
        sys.exit(0)

    def op_1(self) -> None:
        a = self.input[self.pos + 1] % 32768
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        self.register[a] = b
        self.pos += 3

    def op_2(self) -> None:
        a = self.input[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        
        self.stack.append(a)
        self.pos += 2

    def op_3(self) -> None:
        a = self.input[self.pos + 1] % 32768
        self.register[a] = self.stack.pop()
        self.pos += 2

    def op_4(self) -> None:
        a = self.input[self.pos + 1] % 32768
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.input[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        if b == c:
            self.register[a] = 1
        else:
            self.register[a] = 0
        
        self.pos += 4

    def op_5(self) -> None:
        a = self.input[self.pos + 1] % 32768
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.input[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        if b > c:
            self.register[a] = 1
        else:
            self.register[a] = 0
        
        self.pos += 4
   
    def op_6(self) -> None:
        a = self.input[self.pos + 1] % 32768
        if a >= 32768:
            a = self.register[a % 32768]
        self.pos = a
        
    def op_7(self) -> None:
        # self.pos += 1
        # num = self.input[self.pos]
        # if num >= 32768:
        #     num %= 32768
        #     if self.register[num] != 0:
        #         self.pos = self.input[self.pos+1]
        #         return
        # else:
        #     if self.input[self.pos] != 0:
        #         self.pos = self.input[self.pos+1]
        #         return
        # self.pos += 2
        
        a = self.input[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        
        if a != 0:
            self.pos = b
            return
        self.pos += 3
        
    def op_8(self) -> None:
        # self.pos += 1
        # num = self.input[self.pos]
        # if num >= 32768:
        #     num %= 32768
        #     if self.register[num] == 0:
        #         self.pos = self.input[self.pos+1]
        #         return
        # else:
        #     if self.input[self.pos] == 0:
        #         self.pos = self.input[self.pos+1]
        #         return
            
        # self.pos += 2
        
        a = self.input[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        
        if a == 0:
            self.pos = b
            return
        self.pos += 3
        
    def op_9(self) -> None:
        a = self.input[self.pos + 1] % 32768
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.input[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = (b + c) % 32768
        
        self.pos += 4
        
    def op_10(self) -> None:
        a = self.input[self.pos + 1] % 32768
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.input[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = (b * c) % 32768
        
        self.pos += 4
        
        
    def op_12(self) -> None:
        a = self.input[self.pos + 1] % 32768
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.input[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = b & c
        
        self.pos += 4
        
    def op_13(self) -> None:
        a = self.input[self.pos + 1] % 32768
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        c = self.input[self.pos + 3]
        if c >= 32768:
            c = self.register[c % 32768]
        
        self.register[a] = b | c
        
        self.pos += 4
        
    def op_14(self) -> None:
        inverse = {
            '0': '1',
            '1': '0'
        }
        a = self.input[self.pos + 1] % 32768
        b = self.input[self.pos + 2]
        if b >= 32768:
            b = self.register[b % 32768]
        
        b = bin(b)[2:].zfill(15)
        b = ''.join(inverse[x] for x in b)
        b = int(b, 2)
        self.register[a] = b
        
        self.pos += 3
        
    
    def op_17(self) -> None:
        a = self.input[self.pos + 1]
        if a >= 32768:
            a = self.register[a % 32768]
        
        b = self.pos + 2
        # if b >= 32768:
        #     b = self.register[b % 32768]
        self.stack.append(b)
        
        self.pos = a
        
    
    
    
    def op_19(self) -> None:
        self.pos += 1
        num = self.input[self.pos]
        if num >= 32768:
            num %= 32768
            char = chr(num)
        else:
            char = chr(self.input[self.pos])
        print(char, end='')
        self.pos += 1
        
    def op_21(self) -> None:
        self.pos += 1
    
    
if __name__ == '__main__':
    main()