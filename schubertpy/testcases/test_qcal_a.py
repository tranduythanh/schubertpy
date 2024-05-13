from ..qcalc import *
import unittest
from unittest.mock import patch

class Test_qcal_qq(unittest.TestCase):
    
    def test_qpieri_simple(self):
        Gr(2,5)
        res = qpieri(1, 'S[2,1]')
        txt = 'S[2,2] + S[3,1]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_plus(self):
        Gr(2,5)
        res = qpieri(1, 'S[2,1] + S[3,2]')
        txt = 'S[1]*q + S[2,2] + S[3,1] + S[3,3]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus(self):
        Gr(2,5)
        res = qpieri(1, 'S[2,1] - S[3,2]')
        txt = '-S[1]*q + S[2,2] + S[3,1] - S[3,3]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus_and_coef(self):
        Gr(2,5)
        res = qpieri(1, 'S[2,1] - 7*S[3,2]')
        txt = '-7*S[1]*q + S[2,2] + S[3,1] - 7*S[3,3]'
        self.assertEqual(str(res), txt)
        
    def test_qact(self):
        Gr(2,5)
        res = qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = 'S[1]*q + S[2,1]*q + S[2,2] + S[3]*q + S[3,1] + S[3,2]*q + S[3,3] + S[]*q^2'
        self.assertEqual(str(res), txt)
    
    def test_qgiambelli(self):
        Gr(2,5)
        res = qgiambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_qtoS(self):
        Gr(2,5)
        res = qtoS('S[2,1]*S[2,1]*S[2,1]')
        txt = 'S[2,2]*q + 2*S[3,1]*q'
        self.assertEqual(str(res), txt)
    
    def test_dualize(self):
        Gr(2,5)
        res = dualize('S[1]+S[2]')
        txt = 'S[3,1] + S[3,2]'
        self.assertEqual(str(res), txt)


class Test_qcal_(unittest.TestCase):
    
    def test_pieri_simple(self):
        Gr(2,5)
        res = pieri(1, 'S[2,1]')
        txt = 'S[2,2] + S[3,1]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_plus(self):
        Gr(2,5)
        res = pieri(1, 'S[2,1] + S[3,2]')
        txt = 'S[2,2] + S[3,1] + S[3,3]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus(self):
        Gr(2,5)
        res = pieri(1, 'S[2,1] - S[3,2]')
        txt = 'S[2,2] + S[3,1] - S[3,3]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus_and_coef(self):
        Gr(2,5)
        res = pieri(1, 'S[2,1] - 7*S[3,2]')
        txt = 'S[2,2] + S[3,1] - 7*S[3,3]'
        self.assertEqual(str(res), txt)
        
    def test_act(self):
        Gr(2,5)
        res = act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = 'S[2,2] + S[3,1] + S[3,3]'
        self.assertEqual(str(res), txt)
    
    def test_giambelli(self):
        Gr(2,5)
        res = giambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_mult(self):
        Gr(2,5)
        res = mult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = 'S[3,3]'
        self.assertEqual(str(res), txt)

    def test_toS(self):
        Gr(2,5)
        res = toS('S[2,1]*S[2,1]*S[2,1]')
        txt = '0'
        self.assertEqual(str(res), txt)


if __name__ == '__main__':
    unittest.main()


