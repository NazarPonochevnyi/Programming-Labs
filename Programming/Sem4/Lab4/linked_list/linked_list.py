# Linked List

class Node:
    def __init__(self, data):
        self.prev = None
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return f'Node({self.data})'


class LinkedList:
    def __init__(self, nodes=None):
        self._head = None
        self._tail = None
        self._length = 0
        if nodes is not None:
            self._length = len(nodes)
            node = Node(nodes.pop(0))
            self._head = node
            prev_node = node
            for elem in nodes:
                node.next = Node(elem)
                prev_node = node
                node = node.next
                node.prev = prev_node
            self._tail = node

    def __str__(self):
        nodes = []
        node = self._head
        while node is not None:
            nodes.append(node)
            node = node.next
        nodes.append('None')
        return ' -> '.join(map(str, nodes))

    def __repr__(self):
        nodes = []
        node = self._head
        while node is not None:
            nodes.append(node)
            node = node.next
        return 'LinkedList({})'.format(', '.join(map(str, nodes)))

    def __iter__(self):
        node = self._head
        while node is not None:
            yield node
            node = node.next

    def __getitem__(self, index):
        if index < 0:
            raise IndexError("list index must be >= 0")
        if not self._head:
            raise Exception("list is empty")
        i = 0
        for current_node in self:
            if i == index:
                return current_node.data
            i += 1
        raise IndexError("list index out of range")

    def __setitem__(self, index, value):
        if index < 0:
            raise IndexError("list index must be >= 0")
        if not self._head:
            raise Exception("list is empty")
        i = 0
        for current_node in self:
            if i == index:
                current_node.data = value
                return
            i += 1
        raise IndexError("list index out of range")

    def __delitem__(self, index):
        if index < 0:
            raise IndexError("list index must be >= 0")
        if not self._head:
            raise Exception("list is empty")
        if index == 0:
            self._head = self._head.next
            self._head.prev = None
            self._length -= 1
            return
        if index == self._length - 1:
            print(self._tail.prev, self._tail, self._tail.next)
            self._tail = self._tail.prev
            self._tail.next = None
            self._length -= 1
            return
        i, previous_node = 0, self._head
        for current_node in self:
            if i == index:
                previous_node.next = current_node.next
                current_node.next.prev = previous_node
                self._length -= 1
                return
            previous_node = current_node
            i += 1
        raise IndexError("list index out of range")

    def appendleft(self, data):
        new_node = Node(data)
        if not self._head:
            self._head = new_node
            self._tail = new_node
            self._length += 1
            return
        new_node.next = self._head
        self._head.prev = new_node
        self._head = new_node
        self._length += 1

    def append(self, data):
        new_node = Node(data)
        if not self._head:
            self._head = new_node
            self._tail = new_node
            self._length += 1
            return
        self._tail.next = new_node
        new_node.prev = self._tail
        self._tail = new_node
        self._length += 1

    def insert(self, index, data):
        if not self._head or index <= 0:
            self.appendleft(data)
            return
        if index > self._length - 1:
            self.append(data)
            return
        new_node, i = Node(data), 1
        for current_node in self:
            if i == index:
                new_node.next = current_node.next
                new_node.prev = current_node
                current_node.next.prev = new_node
                current_node.next = new_node
                self._length += 1
                return
            i += 1

    def remove(self, data):
        if not self._head:
            raise Exception("list is empty")
        if self._head.data == data:
            del self[0]
            return
        if self._tail.data == data:
            del self[self._length - 1]
            return
        previous_node = self._head
        for current_node in self:
            if current_node.data == data:
                previous_node.next = current_node.next
                current_node.next.prev = previous_node
                self._length -= 1
                return
            previous_node = current_node
        raise Exception("node with data '%s' not found" % data)

    def pop(self, index=None):
        if index is None or index == self._length - 1:
            pop_item = self._tail.data
            del self[self._length - 1]
            return pop_item
        if index < 0:
            raise IndexError("list index must be >= 0")
        if not self._head:
            raise Exception("list is empty")
        if index == 0:
            pop_item = self._head.data
            del self[0]
            return pop_item
        i, previous_node = 0, self._head
        for current_node in self:
            if i == index:
                previous_node.next = current_node.next
                current_node.next.prev = previous_node
                self._length -= 1
                return current_node.data
            previous_node = current_node
            i += 1
        raise IndexError("list index out of range")

    @property
    def head(self):
        if not self._head:
            return None
        return self._head.data

    @property
    def tail(self):
        if not self._tail:
            return None
        return self._tail.data

    @property
    def length(self):
        return self._length


def main():
    llist = LinkedList()
    print(llist)
    llist.appendleft(1)
    llist.append(3)
    llist.insert(1, 2)
    print(repr(llist))
    print(llist.head)
    llist = LinkedList([10, 2, 'car', -4.4, 0])
    print(llist)
    print(llist.length)
    llist[4] = 1
    llist.remove(-4.4)
    del llist[0]
    print(' '.join(map(str, llist)))
    print(llist.tail)
    print(llist.length)
    return llist


if __name__ == "__main__":
    main()
