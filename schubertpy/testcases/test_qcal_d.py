from ..qcalc import *
import unittest
from unittest.mock import patch

class Test_qcal_qq(unittest.TestCase):
    
    def test_qpieri_simple(self):
        OG(2,6)
        res = qpieri(1, 'S[2,1]')
        txt = 'S[1,0]*q1'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_plus(self):
        OG(2,6)
        res = qpieri(1, 'S[2,1] + S[3,2]')
        txt = 'S[1,0]*q1 + S[2,1,0]*q1 + S[]*q1*q2'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus(self):
        OG(2,6)
        res = qpieri(1, 'S[2,1] - S[3,2]')
        txt = 'S[1,0]*q1 - S[2,1,0]*q1 - S[]*q1*q2'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus_and_coef(self):
        OG(2,6)
        res = qpieri(1, 'S[2,1] - 7*S[3,2]')
        txt = 'S[1,0]*q1 - 7*S[2,1,0]*q1 - 7*S[]*q1*q2'
        self.assertEqual(str(res), txt)
        
    def test_qact(self):
        OG(2,6)
        res = qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = 'S[1,0]*q1 + S[1,1]*q1*q2 + S[2,1,0]*q1 + S[3,1]*q1*q2 + S[3,1,0]*q1*q2 + S[]*q1*q2'
        self.assertEqual(str(res), txt)
    
    def test_qgiambelli_1(self):
        OG(2,6)
        res = qgiambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_qgiambelli_2(self):
        OG(2,6)
        res = qgiambelli('S[2,1]*S[2,1]*S[2,1]')
        txt = 'S[1]^3*S[2]^3 - 3*S[1]^2*S[2]^2*S[3] + 3*S[1]*S[2]*S[3]^2 - S[3]^3'
        self.assertEqual(str(res), txt)

    def test_qtoS(self):
        OG(2,6)
        res = qtoS('S[2,1]*S[2,1]*S[2,1]')
        txt = 'S[2,1,0]*q1^2'
        self.assertEqual(str(res), txt)
    
    def test_dualize(self):
        OG(2,6)
        res = dualize('S[1]+S[2]')
        txt = 'S[3] + S[3,1,0]'
        self.assertEqual(str(res), txt)
        
    def test_dualize_2(self):
        OG(2,6)
        res = dualize('S[3,1]*q1')
        txt = 'S[1,0]*q1'
        self.assertEqual(str(res), txt)


class Test_qcal_(unittest.TestCase):
    
    def test_pieri_simple(self):
        OG(2,6)
        res = pieri(1, 'S[2,1]')
        txt = '0'
        self.assertEqual(str(res), txt)

    def test_pieri_with_plus(self):
        OG(2,6)
        res = pieri(1, 'S[2,1] + S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus(self):
        OG(2,6)
        res = pieri(1, 'S[2,1] - S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus_and_coef(self):
        OG(2,6)
        res = pieri(1, 'S[2,1] - 7*S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)
        
    def test_act(self):
        OG(2,6)
        res = act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)
    
    def test_giambelli(self):
        OG(2,6)
        res = giambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_mult(self):
        OG(2,6)
        res = mult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)

    def test_toS(self):
        OG(2,6)
        res = toS('S[2,1]*S[2,1]*S[2,1]')
        txt = '0'
        self.assertEqual(str(res), txt)


if __name__ == '__main__':
    unittest.main()


