import math
import inspect
from prover import Prover
from verifier import Verifier

class SumcheckProtocol:
    def __init__(self, g):
        self.g_arity = len(inspect.signature(g).parameters)
        if self.g_arity < 1:
            raise ValueError("Function arity must be greater than or equal to 1")
        
        self.p = Prover(g, self.g_arity)
        self.v = Verifier(g, self.g_arity, self.p.H)
        self.round = 1
        self.done = False
        
    def __str__(self):
        return f"Protocol(round: {self.round}, H: {self.p.H}, challenges: {self.p.random_challenges})"
    
    def advance_round(self):
        if self.done:
            raise ValueError("Sumcheck protocol is finished")
        
        self.p.compute_and_send_next_polynomial(self.v)
        self.v.check_latest_polynomial()
        
        if self.round == self.g_arity:
            self.done, _ = self.v.evaluate_and_check_gv()
        else:
            self.v.get_new_random_value_and_send(self.p)
            self.round += 1
    
    def advance_to_end(self, verbose=False):
        while not self.done:
            if verbose:
                print("Advance Output:", str(self))
            
            self.advance_round()