import math
from utils import to_bits
from verifier import Verifier

class Prover:
    def __init__(self, g, g_arity):
        self.g_arity = g_arity
        self.random_challenges = []
        self.cached_polynomials = [g]
        self.round = 1
        
        # compute witness H
        sum = 0
        for i in range(2**g_arity):
            args = to_bits(i, g_arity)
            sum += g(*args)
        
        self.H = sum
    
    def compute_and_send_next_polynomial(self, v: Verifier):
        round = self.round
        poly = self.cached_polynomials[-1]
        
        def gJ(*args):
            if len(args) == 0:
                raise ValueError("gJ requires at least one argument")
            
            pad = self.g_arity - round
            sum = 0
            for i in range(2**pad):
                pad_args = to_bits(i, pad)
                j_args = [args[0]] + pad_args
                sum += poly(*j_args)
            return sum
        
        v.recieve_polynomials(gJ)
        self.round += 1
    
    def receive_challenge(self, challenge):
        self.random_challenges.append(challenge)
        self.cache_next(challenge)
        print(f"Received challenge {challenge}, initiating round {self.round}")
    
    def cache_next(self, challenge):
        poly = self.cached_polynomials[-1]
        
        def next_poly(*args):
            return poly(challenge, *args)
        
        self.cached_polynomials.append(next_poly)