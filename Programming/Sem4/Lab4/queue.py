# Stack implementation using dynamic array and linked list

from linked_list.linked_list import LinkedList


class CircularQueue:
    def __init__(self, size):
        if size < 1:
            raise Exception("circular queue size lower than 1")
        self._queue = [None for _ in range(size)]
        self._head = self._tail = -1
        self._size = size

    def is_empty(self):
        return self._head == -1

    @property
    def queue(self):
        if self.is_empty():
            return None
        return self._queue

    @property
    def head(self):
        if self.is_empty():
            return None
        return self._queue[self._head]

    @property
    def tail(self):
        if self.is_empty():
            return None
        return self._queue[self._tail]

    def put(self, item):
        possible_tail = (self._tail + 1) % self._size
        if self.is_empty():
            self._head = self._tail = possible_tail
            self._queue[self._tail] = item
        elif possible_tail == self._head:
            raise Exception("circular queue is full")
        self._tail = possible_tail
        self._queue[self._tail] = item

    def pop_left(self):
        if self.is_empty():
            return None
        temp = self._queue[self._head]
        if self._head == self._tail:
            self._head = self._tail = -1
        else:
            self._head = (self._head + 1) % self._size
        return temp

    def display(self):
        if self.is_empty():
            print("Circular queue is empty")
        elif self._tail >= self._head:
            print("Circular queue:",
                  end=" ")
            for i in range(self._head, self._tail + 1):
                print(self._queue[i], end=" ")
            print()
        else:
            print("Circular queue:",
                  end=" ")
            for i in range(self._head, self._size):
                print(self._queue[i], end=" ")
            for i in range(self._tail + 1):
                print(self._queue[i], end=" ")
            print()
        if ((self._tail + 1) % self._size == self._head):
            print("Circular queue is full")


class QueueList:
    def __init__(self):
        self._queue = LinkedList()
        self._length = 0

    def is_empty(self):
        return self._length == 0

    @property
    def queue(self):
        if self.is_empty():
            return None
        return self._queue

    @property
    def head(self):
        if self.is_empty():
            return None
        return self._queue[0]

    def put(self, item):
        self._queue.append(item)
        self._length += 1

    def pop_left(self):
        self._length -= 1
        return self._queue.pop(0)

    def display(self):
        if self.is_empty():
            print("Circular queue is empty")
        else:
            print("Circular queue:", self._queue)


def main():
    q = QueueList()
    print(q.queue)
    q.put(1)
    q.put(2)
    q.put('+')
    print(q.queue)
    print(q.head)
    print(q.is_empty())
    q.pop_left()
    print(q.head)
    q.pop_left()
    q.pop_left()
    print(q.is_empty())


if __name__ == "__main__":
    main()
