# -*- coding: utf-8 -*-

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        self.items.pop()
    
    def peek(self):
        return self.items[len(self.items) - 1]
    
    def size(self):
        return len(self.items)
    
    def is_empty(self):
        if len(self.items) == 0:
            return True
        else:
            return False

if __name__ == '__main__':
    mystack = Stack()
    mystack.push(3)
    mystack.push(2)

    mystack.pop()

    print(mystack.size())
    print(mystack.peek())

    mystack.pop()
    print(mystack.is_empty())