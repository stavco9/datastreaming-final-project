import random

# Class for implementing a count min sketch "single bank" of counters
class CountMinSketch:
    # Get a random triple (p, a, b) where p is prime and a,b are numbers betweeen 2 and p-1
    @staticmethod
    def get_random_hash_function():
        n = random.getrandbits(64)
        if n < 0: 
            n = -n 
        if n % 2 == 0:
            n = n + 1
        while not n % 20 == 0:
            n = n + 1
        a = random.randint(2, n-1)
        b = random.randint(2, n-1)
        return (n, a, b)
    
    # hash function fora number
    @staticmethod
    def hashfun(hfun_rep, num):
        (p, a, b) = hfun_rep
        return (a * num + b) % p

    # hash function for a string.
    @staticmethod
    def hash_string(hfun_rep, hstr):
        n = hash(hstr)
        
        return CountMinSketch.hashfun(hfun_rep, n)  
    
    # Initialize with `num_counters`
    def __init__ (self, num_counters):
        self.m = num_counters
        self.hash_fun_rep = self.get_random_hash_function()
        self.counters = [0]*self.m

    # function: increment 
    # given a word, increment its count in the countmin sketch
    def increment(self, word):
        self.counters[self.hash_string(self.hash_fun_rep, word)%self.m] = self.counters[self.hash_string(self.hash_fun_rep, word)%self.m] +1
        #return None
        
    # function: approximateCount
    # Given a word, get its approximate count
    def approximateCount(self, word):   
        return self.counters[self.hash_string(self.hash_fun_rep, word)%self.m]