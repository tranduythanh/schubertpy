from schubertpy.qcalc import *
import unittest
from unittest.mock import patch

class Test_qcal_qq(unittest.TestCase):
    
    def test_qpieri_simple(self):
        IG(2,6)
        res = qpieri(1, 'S[2,1]')
        txt = '2*S[3,1] + S[4]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_plus(self):
        IG(2,6)
        res = qpieri(1, 'S[2,1] + S[3,2]')
        txt = '2*S[3,1] + S[4] + S[4,2]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus(self):
        IG(2,6)
        res = qpieri(1, 'S[2,1] - S[3,2]')
        txt = '2*S[3,1] + S[4] - S[4,2]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus_and_coef(self):
        IG(2,6)
        res = qpieri(1, 'S[2,1] - 7*S[3,2]')
        txt = '2*S[3,1] + S[4] - 7*S[4,2]'
        self.assertEqual(str(res), txt)
        
    def test_qact(self):
        IG(2,6)
        res = qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = '3*S[2,1]*q + 3*S[3]*q + 2*S[3,1] + S[3,2]*q + S[4] + 2*S[4,1]*q + S[4,2] + S[]*q^2'
        self.assertEqual(str(res), txt)
    
    def test_qgiambelli_1(self):
        IG(2,6)
        res = qgiambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_qgiambelli_2(self):
        IG(2,6)
        res = qgiambelli('S[2,1]*S[2,1]*S[2,1]')
        txt = 'S[1]^3*S[2]^3 - 3*S[1]^2*S[2]^2*S[3] + 3*S[1]*S[2]*S[3]^2 - S[3]^3'
        self.assertEqual(str(res), txt)

    def test_qtoS(self):
        IG(2,6)
        res = qtoS('S[2,1]*S[2,1]*S[2,1]')
        txt = '4*S[3,1]*q + 5*S[4]*q'
        self.assertEqual(str(res), txt)
    
    def test_dualize(self):
        IG(2,6)
        res = dualize('S[1]+S[2]')
        txt = 'S[4,1] + S[4,2]'
        self.assertEqual(str(res), txt)


class Test_qcal_(unittest.TestCase):
    
    def test_pieri_simple(self):
        IG(2,6)
        res = pieri(1, 'S[2,1]')
        txt = '2*S[3,1] + S[4]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_plus(self):
        IG(2,6)
        res = pieri(1, 'S[2,1] + S[3,2]')
        txt = '2*S[3,1] + S[4] + S[4,2]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus(self):
        IG(2,6)
        res = pieri(1, 'S[2,1] - S[3,2]')
        txt = '2*S[3,1] + S[4] - S[4,2]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus_and_coef(self):
        IG(2,6)
        res = pieri(1, 'S[2,1] - 7*S[3,2]')
        txt = '2*S[3,1] + S[4] - 7*S[4,2]'
        self.assertEqual(str(res), txt)
        
    def test_act(self):
        IG(2,6)
        res = act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = '2*S[3,1] + S[4] + S[4,2]'
        self.assertEqual(str(res), txt)
    
    def test_giambelli(self):
        IG(2,6)
        res = giambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_mult(self):
        IG(2,6)
        res = mult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = '2*S[4,2]'
        self.assertEqual(str(res), txt)

    def test_toS(self):
        IG(2,6)
        res = toS('S[2,1]*S[2,1]*S[2,1]')
        txt = '0'
        self.assertEqual(str(res), txt)


if __name__ == '__main__':
    unittest.main()


