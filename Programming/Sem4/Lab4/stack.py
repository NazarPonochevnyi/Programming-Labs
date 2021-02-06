# Stack implementation using dynamic array and linked list

from linked_list.linked_list import LinkedList


class StackArray:
    def __init__(self, size):
        if size < 2:
            raise Exception("array size for 2 stacks must be >= 2")
        self._stack = [None for _ in range(size)]
        self._length = 0
        self._size = size
        self._top1 = -1
        self._top2 = self._size

    def show1(self):
        if self._top1 <= -1:
            return None
        return self._stack[self._top1]

    def show2(self):
        if self._top2 >= self._size:
            return None
        return self._stack[self._top2]

    def put1(self, item):
        if self.is_full():
            raise Exception("stack overflow")
        self._top1 += 1
        self._stack[self._top1] = item
        self._length += 1

    def put2(self, item):
        if self.is_full():
            raise Exception("stack overflow")
        self._top2 -= 1
        self._stack[self._top2] = item
        self._length += 1

    def pop1(self):
        if self._top1 <= -1:
            raise Exception("stack underflow")
        temp = self._stack[self._top1]
        self._stack[self._top1] = None
        self._top1 -= 1
        self._length -= 1
        return temp

    def pop2(self):
        if self._top2 >= self._size:
            raise Exception("stack underflow")
        temp = self._stack[self._top2]
        self._stack[self._top2] = None
        self._top2 += 1
        self._length -= 1
        return temp

    def is_full(self):
        return self._top1 + 1 == self._top2

    def is_empty(self):
        return self._top1 == -1 and self._top2 == self._size

    @property
    def stack(self):
        return self._stack

    @property
    def length(self):
        return self._length


class StackList:
    def __init__(self):
        self._stack = LinkedList()
        self._length = 0

    def show(self):
        if self.is_empty():
            return None
        return self._stack.tail

    def put(self, item):
        self._stack.append(item)
        self._length += 1

    def pop(self):
        if self.is_empty():
            raise Exception("stack underflow")
        self._length -= 1
        return self._stack.pop()

    def is_empty(self):
        return self._length == 0

    @property
    def stack(self):
        return self._stack

    @property
    def length(self):
        return self._length


def is_float(str):
    try:
        float(str)
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    arr_size = int(input("Input array size for 2 stacks: ").strip())
    s = StackArray(arr_size)
    gr = "\n[s]tack, [l]ength, [put]1/2, " \
        + "[pop]1/2, [show]1/2, [e]mpty, [q]uit: "
    while True:
        command = input(gr).strip().split()
        if len(command) == 0 or \
                (len(command) == 2 and not is_float(command[1])):
            print("Wrong command")
            continue
        if command[0] in ('s', 'stack'):
            print(s.stack)
        elif command[0] in ('l', 'length'):
            print(s.length)
        elif command[0] == 'put1':
            s.put1(float(command[1]))
        elif command[0] == 'put2':
            s.put2(float(command[1]))
        elif command[0] == 'show1':
            print(s.show1())
        elif command[0] == 'show2':
            print(s.show2())
        elif command[0] == 'pop1':
            print(s.pop1(), 'deleted')
        elif command[0] == 'pop2':
            print(s.pop2(), 'deleted')
        elif command[0] in ('e', 'empty'):
            print(s.is_empty())
        elif command[0] in ('q', 'quit', 'exit'):
            break
