#!/usr/bin/env python
# -*- coding: utf-8 -*-

def fibonacci(n):
    if (n <= 2):
      return 1
    else:
      prev1 = 1
      prev2 = 1
      for i in range(1, n - 2):
        tmp = prev2
        prev2 = prev1 + prev2
        prev1 = tmp
      
      return prev2


if __name__ == '__main__':
    for i in range(1, 60):
        print(i, fibonacci(i))