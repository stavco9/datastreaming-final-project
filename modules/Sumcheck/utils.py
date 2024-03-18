import math
import numbers
import inspect

def to_bits(n, padToLen):
    binStr = bin(n)[2:]
    
    if len(binStr) > padToLen:
        padToLen = len(binStr)
    
    v = [int(ch) for ch in binStr]
    diff = padToLen - len(v)
    
    paddedV = [0] * diff
    return paddedV + v

def deg_j(g, j):
    exp = 1
    while True:
        args = [1] * len(inspect.signature(g).parameters)
        args[j] = 100
        out1 = g(*args)
        
        args[j] = 1000
        out2 = g(*args)
        
        scaling = 1000 ** exp / 100 ** exp
        if abs(out1 / scaling - out2) < 1:
            return exp
        elif exp > 10:
            raise ValueError("exp grew larger than 10")
        else:
            exp += 1

def arity(f):
    arity = 0
    if isinstance(f, numbers.FunctionType):
        arity = f.__code__.co_argcount
    elif isinstance(f, numbers.MethodType):
        arity = f.__func__.__code__.co_argcount - 1
    elif isinstance(f, numbers.LambdaType):
        arity = f.__code__.co_argcount
        
    return arity
