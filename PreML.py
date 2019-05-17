# python -m pip install numpy
# python -m pip install scipy
# python -m pip install matplotlib

import time
from datetime import datetime
from datetime import timedelta
from numpy import *
import scipy as sp
import matplotlib.pylab as plt

def test_numpy():
    mat1 = mat([
        [1, 2, 3],
        [4, 5, 6]
    ])
    
    mat2 = mat([
        [1, 2],
        [2, 5],
        [3, 8]
    ])
    
    mat3 = mat1*mat2
    print(mat3)
    print(eye(2))

    t = sp.linspace(0, 1, 100)

    plt.plot(t, t**2)
    # plt.show()


if __name__ == "__main__":
    fmt = '%Y-%m-%d %H:%M:%S'
    start = datetime.now().strftime(fmt)

    test_numpy()
        
    finish = datetime.now().strftime(fmt)

    print(start)
    print(finish)