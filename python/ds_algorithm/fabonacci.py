# -*- coding: utf-8 -*-

def fabonacci(size):
    fabonacci_ary = [1, 1]
    if size <= 0:
        return []
    elif size == 1:
        return [1]
    elif size == 2:
        return fabonacci_ary
    for i in range(2, size):
        fabonacci_ary.append(fabonacci_ary[i - 1] + fabonacci_ary[i - 2])

    fabonacci_ary.reverse()        
    return fabonacci_ary

if __name__ == "__main__":
    print(', '.join([str(num) for num in fabonacci(130)]))