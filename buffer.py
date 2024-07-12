class Node:
    """
    Node is a container for data used in FixedLengthBuffer.
    """
    def __init__(self, data, next=None):
        """
        Constructor for a Node object.

        :param data: the data to be stored in the Node
        :param next: [default: None] the next node in the list
        """
        self.data = data
        self.next = next

class FixedLengthBuffer:
    """
    FixedLengthBuffer implements a fixed length singly-linked list,
    with a built in `__iter__` unlike the MicroPython `deque`.
    """
    def __init__(self, maxlen=10):
        """
        Constructor for FixedLengthBuffer.

        :param maxlen: the maximum size of the buffer, old values are tossed out
        """
        self.head = None
        self.tail = None
        self.size = 0
        self.maxlen = maxlen

    def append(self, val):
        """
        Append a value to the buffer.

        :param val: the value to be added
        """
        if self.size + 1 > self.maxlen:
            self.pop()

        if not self.head:
            self.head = Node(val)
            self.tail = self.head
        else:
            self.tail.next = Node(val)
            self.tail = self.tail.next
        
        self.size += 1

    def pop(self):
        """
        Pop from the left of the buffer (oldest value).

        :return: the value of the oldest item in the buffer
        """
        if self.size <= 0:
            raise Exception("Buffer is empty, nothing to pop!")

        val = self.head.data
        self.head = self.head.next
        self.size -= 1
        return val
    
    def clear(self):
        """
        Empty out the buffer.
        """
        self.head = None
        self.tail = None
        self.size = 0
    
    def __len__(self):
        """
        Returns the current size of the buffer.
        """
        return self.size

    def __iter__(self):
        """
        Implements an iterator for the fixed length buffer, makes
        summation much easier.
        """
        current_node = self.head
        while current_node:
            yield current_node.data
            current_node = current_node.next

    def __str__(self):
        """
        Returns a simple string representation of the buffer contents.
        """
        current_node = self.head
        result = ''
        while current_node:
            result += str(current_node.data) + ' '
            current_node = current_node.next

        return result

