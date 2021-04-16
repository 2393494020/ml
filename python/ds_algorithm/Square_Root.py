#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Newton's Method

def square_root(num):
    old_root = num / 2
    for n in range(20):
        old_root = (1 / 2) * (old_root + num / old_root)
    
    return old_root

if __name__ == '__main__':
    print(square_root(81))