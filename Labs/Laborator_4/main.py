class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

def stack_exercise():
    print('Stack Exercise: ')
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    print('Size: ', stack.size())
    print('Peek: ', stack.peek())
    print('Pop: ', stack.pop())
    print('Pop: ', stack.pop())
    print('Pop: ', stack.pop())
    print('Pop: ', stack.pop())
    print()

stack_exercise()

class Queue:
    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        else:
            return None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

def queue_exercise():
    print('Queue Exercise: ')
    queue = Queue()
    queue.push(1)
    queue.push(2)
    queue.push(3)

    print('Size: ', queue.size())
    print('Peek: ', queue.peek())
    print('Pop: ', queue.pop())
    print('Pop: ', queue.pop())
    print('Pop: ', queue.pop())
    print('Pop: ', queue.pop())
    print()

queue_exercise()

class Matrix:

    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

    def get(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.cols:
            return self.matrix[i][j]
        else:
            return None

    def set(self, i, j, val):
        if 0 <= i < self.rows and 0 <= j < self.cols:
            self.matrix[i][j] = val
        else:
            return None

    def transpose(self):
        result = []
        for i in range(self.cols):
            result.append([])
            for j in range(self.rows):
                result[i].append(self.matrix[j][i])
        return result

    def multiplication(self, other):

        if self.cols != other.rows:
            return None

        result = []
        for i in range(self.rows):
            result.append([])
            for j in range(other.cols):
                result[i].append(0)
                for k in range(self.cols):
                    result[i][j] += self.matrix[i][k] * other.matrix[k][j]
        return result

    def iterate(self, func):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = func(self.matrix[i][j])
        return self.matrix


def matrix_exercise():
    print('Matrix Exercise: ')
    matrix = Matrix([[1, 2, 3], [4, 5, 6]])
    print('Get: ', matrix.get(1, 2))
    print('Get: ', matrix.get(1, 3))
    matrix.set(1, 2, 10)
    print('Get: ', matrix.get(1, 2))
    print('Transpose: ', matrix.transpose())
    print('Multiplication: ', matrix.multiplication(Matrix([[1, 2], [3, 4], [5, 6]])))
    print('Iterate: ', matrix.iterate(lambda x: x * 2))
    print()


matrix_exercise()