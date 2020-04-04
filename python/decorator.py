#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


# 装饰器
def deco(func):
    def wrapper(*args):
        begin = time.time()
        result = func(*args)
        end = time.time()
        print('Total time: {:.3} s'.format( end - begin ))
        return result

    return wrapper

def is_prime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2, num):
            if num % i == 0:
                return False
        return True

@deco
def count_prime_num(maxnum):
    count = 0
    for num in range(2, maxnum):
        if is_prime(num):
            count = count + 1
    
    return(count)

if __name__ == '__main__':
    print(count_prime_num(10000))