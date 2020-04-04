#!/usr/bin/env python
# -*- coding: utf-8 -*-


def isAnagram1(s, t):
    dict1, dict2 = {}, {}
    for item in s:
        dict1[item] = dict1.get(item, 0) + 1
    
    for item in t:
        dict2[item] = dict2.get(item, 0) + 1
    
    return dict1 == dict2

def isAnagram2(s, t):
    hashTable1, hashTable2 = [0] * 26, [0] * 26
    for item in s:
        hashTable1[ord(item) - ord('a')] += 1
    
    for item in t:
        hashTable2[ord(item) - ord('a')] += 1
    
    return hashTable1 == hashTable2

def isAnagram3(s, t):
    return sorted(s) == sorted(t)

if __name__ == '__main__':
    print(isAnagram1('cat', 'act'))
    print(isAnagram2('cat', 'act'))
    print(isAnagram3('cat', 'act'))