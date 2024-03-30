import math
import random
import numpy as np

class HighOrderCountMinSketch:
    def generate_hash_functions(self, seed=315870964):
        random.seed(seed)  # Ensure deterministic randomness
        salts = [random.randint(0, 2**32 - 1) for _ in range(self.depth)]  # Unique salt for each hash function

        def hash_func_factory(salt):
            def hash_func(x):
                return (hash(x + salt) % self.width)
            return hash_func

        return [hash_func_factory(salt) for salt in salts]

    def __init__(self, delta, epsilon):
        self.width = int(math.ceil(2/epsilon))
        self.depth = int(math.ceil(np.log2(math.ceil(1/delta))))
        self.table = [[[0 for k in range(self.width)] for i in range(self.width)] for j in range(self.depth)]
        self.hash_functions = [self.generate_hash_functions(),self.generate_hash_functions()]

    def add(self, item):
        for func in range(self.depth):
            self.table[func][self.hash_functions[0][func](item[0])][self.hash_functions[1][func](item[1])] += 1


    def estimate(self, item):
        estimates = []
        for func in range(self.depth):
            estimates.append(self.table[func][self.hash_functions[0][func](item[0])][self.hash_functions[1][func](item[1])])
        return min(estimates)