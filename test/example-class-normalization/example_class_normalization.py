""" Classes:
    Some weird and corner cases we suspect might choke the
    representer.

    These include:
    - nested classes
    - classes with pass
    - classes with ...
    - classes with unassigned but type-hinted class vars
    -other craziness as we come across it.
"""

from collections import deque
class BufferFullException(BufferError):
    """
    Docstring with only an ellipsis body.
    """
    ...


class BufferEmptyException(BufferError):
    """
    Docstring with only a pass body.
    """
    pass


class BufferEmptyException(BufferError):
    """
    Docstring with a pass method.
    """

    def pass_method(self):
        pass


class BufferEmptyException(BufferError):
    """
    Docstring with a ellipsis method.
    """

    def pass_method(self):
        ...


class CircularBuffer:
    """
    Unassigned but typehinted class vars.
    """

    tracker: int
    instructions: str

    def __init__(self, capacity: int):
        self.buffer = deque([], capacity)
    def read(self):
        if not self.buffer:
            raise BufferEmptyException("Circular buffer is empty")
        return self.buffer.popleft()
    def write(self, data):
        if len(self.buffer) == self.buffer.maxlen:
            raise BufferFullException("Circular buffer is full")
        self.buffer.append(data)
    def overwrite(self, data):
        if len(self.buffer) == self.buffer.maxlen:
            self.read()
        self.write(data)
    def clear(self):
        self.buffer.clear()


class Account:
    """
        A class with an inner class and methods.
    """

    account_number: int
    
    def __init__(self):
        self.bank = self.Bank()
        self.test: str

    class Bank:

        bank_number: int

        def __init__(self):
            self.balance = 100000

        def withdraw(self, amount):
            self.balance -= amount

        def deposit(self, amount):
            self.balance += amount

        def audit(self):
            ...


