import random
from utils import deg_j
from prover import Prover

class Verifier:
    def __init__(self, g, g_arity, H):
        self.g = g
        self.g_arity = g_arity
        self.H = H
        self.random_challenges = []
        self.round = 1
        self.polynomials = []
    
    def recieve_polynomials(self, polynomial):
        self.polynomials.append(polynomial)
    
    def check_latest_polynomial(self):
        latest_poly = self.polynomials[-1]
        deg_latest = deg_j(latest_poly, 0)
        deg_max = deg_j(self.g, self.round - 1)
        
        if deg_latest > deg_max:
            return ValueError(f"Prover sent polynomial of degree {deg_latest} greater than expected : {deg_max}")
        
        new_sum = latest_poly(0) + latest_poly(1)
        
        if self.round == 1:
            check = self.H
        else:
            check = self.polynomials[-2](self.random_challenges[-1])
        
        if check != new_sum:
            return ValueError(f"Prover sent incorrect polynomials: {new_sum}, expected {check}")
        
        return None
    
    def get_new_random_value_and_send(self, p: Prover):
        self.random_challenges.append(random.randint(0, 1))
        p.receive_challenge(self.random_challenges[-1])
        self.round += 1
    
    def evaluate_and_check_gv(self):
        if len(self.random_challenges) != self.g_arity - 1:
            return False, ValueError("Incorrect number of random challenges")
        
        self.random_challenges.append(random.randint(0, 1))
        g_final = self.g(*self.random_challenges)
        check = self.polynomials[-1](self.random_challenges[-1])
        
        if g_final != check:
            return False, ValueError("Prover sent incorrect final polynomials")
        
        print("VERIFIER ACCEPTS")
        return True, None