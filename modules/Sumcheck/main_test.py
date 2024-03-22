import unittest
from main import SumcheckProtocol

class TestSumcheck(unittest.TestCase):
    def test_sumcheck(self):

        def g(*args):
            a = args[0]
            return a + a + a*a

        protocol = SumcheckProtocol(g)
        print(protocol)
        protocol.advance_to_end(True)

        def f(*args):
            a = args[0]
            return a*a*a + a + a

        protocol = SumcheckProtocol(f)
        protocol.advance_to_end(True)

        def ff(*args):
            a = args[0]
            return a*a*a + a + a + a*a

        protocol = SumcheckProtocol(ff)
        protocol.advance_to_end(True)