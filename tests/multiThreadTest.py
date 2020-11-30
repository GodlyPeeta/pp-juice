import ppcalc

import multiprocessing
from os import getpid

def worker(acc, two):
    print(acc)
    return two

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 5)
    print(pool.map(worker, [[90,2],[92,3],[91,1]] ))
