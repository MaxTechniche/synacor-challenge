#!/usr/bin/env python3

import sys
import json


MAX_VALUE = 32768
ROOMS = {}


def main():
    vm = VM()
    vm.read()
    vm.run()


class InputBuffer(list):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.address = 0

    def __call__(self, *args: any, **kwds: any) -> any:
        return self.address < len(self)

    def add(self, val: str | int | list):
        if isinstance(val, list) or isinstance(val, str):
            for element in val:
                self.append(ord(element))
        elif isinstance(val, int):
            self.append(val)
        else:
            raise ValueError("Unable to add type " + type(val).__name__)

        self.append(10)
        return self

    def next(self):
        if self():
            self.address += 1
            return self[self.address - 1]
        else:
            raise IndexError

    def to_dict(self):
        d = {}
        d["history"] = self[:]
        d["address"] = 0
        return d


class Room(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self["long_desc"] = ""
        self["short_desc"] = ""
        self["id"] = None
        self["items"] = []
        self["actions"] = []

    def remove_exit(self, e: str) -> None:
        self["actions"].remove(e)

    def set_id(self) -> None:
        if self["id"]:
            return
        try:
            i = ""
            for ch in self["long_desc"]:
                i += bin(ord(ch))[2:].zfill(8)
            i = i[::-1]
            i = int(i, 2)
            self["id"] = i % 2147483647
        except TypeError:
            return


class VM:
    def __init__(self, *args, **kwargs) -> None:
        self.memory = []
        self.register = [0] * 8
        self.stack = []
        self.input_buffer = InputBuffer()
        self.address = 0
        self.current_room = Room()

    def get_register(self):
        s = "-" * 63 + "\n"
        s += "\t".join(["reg " + str(x) + " |" for x in range(8)]) + "\n"
        s += " \t".join([str(x) for x in self.register]) + "\n"
        s += "-" * 63
        return s

    def read(self, file_path: str = None) -> bool:
        if not file_path:
            file_path = "challenge.bin"

        # Expand 2 bytes to 1 little-endian pair
        def expand_bytes(low, high):
            low = bin(low)[2:].zfill(8)
            high = bin(high)[2:].zfill(8)
            bin_num = high + low
            num = int(bin_num, 2)
            return num

        # Parse File
        with open(file_path, "rb") as b:
            while True:
                low = None
                high = None
                for i in b.read(2):
                    if low is None:
                        low = i
                    elif high is None:
                        high = i
                if low is None and high is None:
                    break
                self.memory.append(expand_bytes(low, high))

    def run(self) -> None:
        while True:
            num = self.get_val(0, False)

            try:
                getattr(self, "opcode_" + str(num))()
            except AttributeError:
                print(num)
                raise

    def set_val(self, value, address_value, reg=True, force_reg=False):
        if reg:
            if address_value >= MAX_VALUE:
                self.register[address_value % MAX_VALUE] = value
                return
            if force_reg:
                self.register[address_value] = value
                return
        self.memory[address_value] = value

    def get_val(self, address, reg=True):
        n = self.memory[self.address + address]
        if reg:
            if n >= MAX_VALUE:
                n = self.register[n % MAX_VALUE]

        return n

    def opcode_0(self) -> None:
        sys.exit()

    def opcode_1(self) -> None:
        a = self.memory[self.address + 1] % MAX_VALUE
        b = self.get_val(2)
        self.set_val(b, a, force_reg=True)
        self.register[a] = b
        self.address += 3

    def opcode_2(self) -> None:
        a = self.get_val(1)
        self.stack.append(a)
        self.address += 2

    def opcode_3(self) -> None:
        a = self.get_val(1, False)
        self.set_val(self.stack.pop(), a)
        self.address += 2

    def opcode_4(self) -> None:
        a = self.get_val(1, False)
        b = self.get_val(2)
        c = self.get_val(3)
        self.set_val(1 * (b == c), a)
        self.address += 4

    def opcode_5(self) -> None:
        a = self.get_val(1, False)
        b = self.get_val(2)
        c = self.get_val(3)
        self.set_val(1 * (b > c), a)
        self.address += 4

    def opcode_6(self) -> None:
        self.address = self.get_val(1)

    def opcode_7(self) -> None:
        a = self.get_val(1)
        b = self.get_val(2)

        if a != 0:
            self.address = b
            return
        self.address += 3

    def opcode_8(self) -> None:
        a = self.get_val(1)
        b = self.get_val(2)

        if a == 0:
            self.address = b
            return
        self.address += 3

    def opcode_9(self) -> None:
        a = self.get_val(1, False)
        b = self.get_val(2)
        c = self.get_val(3)
        self.set_val((b + c) % MAX_VALUE, a)

        self.address += 4

    def opcode_10(self) -> None:
        a = self.get_val(1, False)
        b = self.get_val(2)
        c = self.get_val(3)
        self.set_val((b * c) % MAX_VALUE, a)

        self.address += 4

    def opcode_11(self) -> None:
        a = self.get_val(1, False)
        b = self.get_val(2)
        c = self.get_val(3)
        self.set_val(b % c, a)

        self.address += 4

    def opcode_12(self) -> None:
        a = self.get_val(1, False)
        b = self.get_val(2)
        c = self.get_val(3)
        self.set_val(b & c, a)

        self.address += 4

    def opcode_13(self) -> None:
        a = self.get_val(1, False)
        b = self.get_val(2)
        c = self.get_val(3)
        self.set_val(b | c, a)

        self.address += 4

    def opcode_14(self) -> None:
        inverse = {"0": "1", "1": "0"}
        a = self.get_val(1, False)
        b = self.get_val(2)

        b = bin(b)[2:].zfill(15)
        b = "".join(inverse[x] for x in b)
        b = int(b, 2)
        self.set_val(b, a)

        self.address += 3

    def opcode_15(self) -> None:
        a = self.get_val(1, False)
        b = self.memory[self.get_val(2)]
        self.set_val(b, a)

        self.address += 3

    def opcode_16(self) -> None:
        b = self.get_val(2)
        a = self.get_val(1)
        self.set_val(b, a, False)

        self.address += 3

    def opcode_17(self) -> None:
        self.stack.append(self.address + 2)
        self.address = self.get_val(1)

    def opcode_18(self) -> None:
        self.address = self.stack.pop()

    def opcode_19(self) -> None:
        a = self.get_val(1)
        if not self.current_room["id"]:
            self.current_room["long_desc"] += chr(a)
        if not self.input_buffer():
            print(chr(a), end="")

        self.address += 2

    def opcode_20(self) -> None:
        if self.current_room["long_desc"]:
            self.current_room.set_id()
            if self.current_room["id"] not in ROOMS:
                ROOMS[self.current_room["id"]] = self.current_room

        if self.input_buffer():
            n = self.input_buffer.next()
            if n != 10 or n != 13:
                a = self.get_val(1, False)
                self.set_val(n, a)

            self.address += 2
        else:
            i = input().split()
            if i[0] == "save":
                if len(i) > 1:
                    f_name = i[1]
                else:
                    f_name = None
                save(self, f_name)
                return
            elif i[0] == "load":
                if len(i) > 1:
                    f_name = i[1]
                else:
                    f_name = None
                try:
                    self = load(f_name)
                    self.run()
                    return
                except FileNotFoundError:
                    print("file not found. Please try again.")
                    return
            elif i[0] == "exit":
                if len(i) > 1:
                    if i[1] == "save":
                        if len(i) > 2:
                            f_name = i[2]
                        else:
                            f_name = None
                        save(self, f_name)

                sys.exit()
            i = " ".join(i)
            self.input_buffer.add(i)

        self.current_room = Room()

    def opcode_21(self) -> None:
        self.address += 1


def save(vm: VM, file_path: str = None) -> None:
    state = {}
    state["memory"] = vm.memory
    state["register"] = vm.register
    state["input_buffer"] = vm.input_buffer.to_dict()
    state["stack"] = vm.stack
    state["address"] = vm.address
    state["ROOMS"] = ROOMS

    if not file_path:
        file_path = "program-save"
    json.dump(state, open(file_path, "w"))


def load(file_path: str = None) -> VM:
    if not file_path:
        file_path = "program-save"
    state = json.load(open(file_path))
    vm = VM()
    vm.memory = state["memory"]
    vm.address = state["address"]
    vm.stack = state["stack"]
    vm.register = state["register"]
    vm.input_buffer = InputBuffer(state["input_buffer"]["history"])
    vm.input_buffer.address = state["input_buffer"]["address"]
    global ROOMS
    ROOMS = state["ROOMS"]

    return vm


if __name__ == "__main__":
    main()
