import itertools
import functools
from utils import to_bits
from verifier import Verifier

class InefficientProver:
    def __init__(self, g, g_arity):
        self.g = g
        self.g_arity = g_arity
        self.random_challenges = []
        self.polynomials = []
        self.round = 1
        
        sum = 0
        for i in range(1 << g_arity):
            args = to_bits(i, g_arity)
            sum += g(*args)
        self.H = sum
    
    def compute_and_send_next_polynomial(self, v: Verifier):
        round = self.round
        
        def gJ(*args):
            if len(args) == 0:
                raise ValueError("gJ requires at least one argument")
            
            argsInit = self.random_challenges[:round-1] + [args[0]]
            padLen = self.g_arity - len(argsInit)
            
            sum = 0
            for bits in itertools.product([0, 1], repeat=padLen):
                fullArgs = argsInit + list(bits)
                sum += self.g(*fullArgs)
            return sum
        
        self.polynomials.append(gJ)
        v.recieve_polynomials(gJ)
        self.round += 1
        
    def receive_challenge(self, challenge):
        self.random_challenges.append(challenge)
        print(f"Received challenge {challenge}, initiating round {self.round}")