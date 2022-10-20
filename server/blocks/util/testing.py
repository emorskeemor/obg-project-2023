import time
from typing import List

from blocks.core.generate.save import SaveNode


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()

        print("TIME TAKEN :", round(end-start, 2))
        return res
    return wrapper

def reverse_sp(sp:SaveNode):
    items = list(sp.resolve())
    items.reverse()
    return items

def difference(sp1:SaveNode, sp2:SaveNode):
    for node1, node2 in zip(reverse_sp(sp1), reverse_sp(sp2)):
        print("\nnode1")
        print(node1.blocks)
        print(node1.used)
        
        print("node2")
        print(node2.blocks)
        print(node2.used)