from schubertpy.grassmannian import *
import unittest
from unittest.mock import patch

class Test_grassmannian(unittest.TestCase):
    
    def setUp(self):
        self.gr = Grassmannian(2, 5)

    def test_qpieri_simple(self):
        res = self.gr.qpieri(1, 'S[2,1]')
        txt = 'S[2,2] + S[3,1]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_plus(self):
        res = self.gr.qpieri(1, 'S[2,1] + S[3,2]')
        txt = 'S[1]*q + S[2,2] + S[3,1] + S[3,3]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus(self):
        res = self.gr.qpieri(1, 'S[2,1] - S[3,2]')
        txt = '-S[1]*q + S[2,2] + S[3,1] - S[3,3]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus_and_coef(self):
        res = self.gr.qpieri(1, 'S[2,1] - 7*S[3,2]')
        txt = '-7*S[1]*q + S[2,2] + S[3,1] - 7*S[3,3]'
        self.assertEqual(str(res), txt)
        
    def test_qact(self):
        res = self.gr.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = 'S[1]*q + S[2,1]*q + S[2,2] + S[3]*q + S[3,1] + S[3,2]*q + S[3,3] + S[]*q^2'
        self.assertEqual(str(res), txt)
    
    def test_qgiambelli(self):
        res = self.gr.qgiambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_qmult(self):
        res = self.gr.qmult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = 'S[1]*q + S[2,1]*q + S[3]*q + S[3,3]'
        self.assertEqual(str(res), txt)

    def test_qtoS(self):
        res = self.gr.qtoS('S[2,1]*S[2,1]*S[2,1]')
        txt = 'S[2,2]*q + 2*S[3,1]*q'
        self.assertEqual(str(res), txt)
    
    def test_dualize(self):
        res = self.gr.dualize('S[1]+S[2]')
        txt = 'S[3,1] + S[3,2]'
        self.assertEqual(str(res), txt)
    
    def test_pieri_simple(self):
        res = self.gr.pieri(1, 'S[2,1]')
        txt = 'S[2,2] + S[3,1]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_plus(self):
        res = self.gr.pieri(1, 'S[2,1] + S[3,2]')
        txt = 'S[2,2] + S[3,1] + S[3,3]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus(self):
        res = self.gr.pieri(1, 'S[2,1] - S[3,2]')
        txt = 'S[2,2] + S[3,1] - S[3,3]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus_and_coef(self):
        res = self.gr.pieri(1, 'S[2,1] - 7*S[3,2]')
        txt = 'S[2,2] + S[3,1] - 7*S[3,3]'
        self.assertEqual(str(res), txt)
        
    def test_act(self):
        res = self.gr.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = 'S[2,2] + S[3,1] + S[3,3]'
        self.assertEqual(str(res), txt)
    
    def test_giambelli(self):
        res = self.gr.giambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_mult(self):
        res = self.gr.mult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = 'S[3,3]'
        self.assertEqual(str(res), txt)

    def test_toS(self):
        res = self.gr.toS('S[2,1]*S[2,1]*S[2,1]')
        txt = '0'
        self.assertEqual(str(res), txt)


if __name__ == '__main__':
    unittest.main()


