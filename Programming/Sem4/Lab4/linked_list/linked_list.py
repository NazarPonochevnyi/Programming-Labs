# Linked List

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return f'Node({self.data})'


class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(elem)
                node = node.next

    def __str__(self):
        nodes = []
        node = self.head
        while node is not None:
            nodes.append(node)
            node = node.next
        nodes.append('None')
        return ' -> '.join(map(str, nodes))

    def __repr__(self):
        nodes = []
        node = self.head
        while node is not None:
            nodes.append(node)
            node = node.next
        return 'LinkedList({})'.format(', '.join(map(str, nodes)))

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __getitem__(self, index):
        if index < 0:
            raise IndexError("list index must be >= 0")
        if not self.head:
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
        if not self.head:
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
        if not self.head:
            raise Exception("list is empty")
        if index == 0:
            self.head = self.head.next
            return
        i, previous_node = 0, self.head
        for current_node in self:
            if i == index:
                previous_node.next = current_node.next
                return
            previous_node = current_node
            i += 1
        raise IndexError("list index out of range")

    def appendleft(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        for current_node in self:
            pass
        current_node.next = new_node

    def insert(self, index, data):
        if not self.head or index <= 0:
            self.appendleft(data)
            return
        new_node, i = Node(data), 1
        for current_node in self:
            if i == index:
                new_node.next = current_node.next
                current_node.next = new_node
                return
            i += 1
        current_node.next = new_node

    def remove(self, data):
        if not self.head:
            raise Exception("list is empty")
        if self.head.data == data:
            self.head = self.head.next
            return
        previous_node = self.head
        for current_node in self:
            if current_node.data == data:
                previous_node.next = current_node.next
                return
            previous_node = current_node
        raise Exception("node with data '%s' not found" % data)

    def pop(self, index):
        if index < 0:
            raise IndexError("list index must be >= 0")
        if not self.head:
            raise Exception("list is empty")
        if index == 0:
            pop_item = self.head.data
            self.head = self.head.next
            return pop_item
        i, previous_node = 0, self.head
        for current_node in self:
            if i == index:
                previous_node.next = current_node.next
                return current_node.data
            previous_node = current_node
            i += 1
        raise IndexError("list index out of range")


def main():
    llist = LinkedList()
    print(llist)
    llist.appendleft(1)
    llist.append(3)
    llist.insert(1, 2)
    print(repr(llist))
    llist = LinkedList([10, 2, 'car', -4.4, 0])
    print(llist)
    llist[4] = 1
    llist.remove(-4.4)
    del llist[0]
    print(' '.join(map(str, llist)))
    return llist


if __name__ == "__main__":
    main()
