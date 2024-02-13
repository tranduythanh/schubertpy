from isotropic_grassmannian import *
import unittest
from unittest.mock import patch

class Test_isotropic_grassmannian(unittest.TestCase):
    def setUp(self):
        self.ig = IsotropicGrassmannian(2, 6)
    
    def test_qpieri_simple(self):
        res = self.ig.qpieri(1, 'S[2,1]')
        txt = '2*S[3,1] + S[4]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_plus(self):
        res = self.ig.qpieri(1, 'S[2,1] + S[3,2]')
        txt = '2*S[3,1] + S[4] + S[4,2]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus(self):
        res = self.ig.qpieri(1, 'S[2,1] - S[3,2]')
        txt = '2*S[3,1] + S[4] - S[4,2]'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus_and_coef(self):
        res = self.ig.qpieri(1, 'S[2,1] - 7*S[3,2]')
        txt = '2*S[3,1] + S[4] - 7*S[4,2]'
        self.assertEqual(str(res), txt)
        
    def test_qact(self):
        res = self.ig.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = '3*S[2,1]*q + 3*S[3]*q + 2*S[3,1] + S[3,2]*q + S[4] + 2*S[4,1]*q + S[4,2] + S[]*q^2'
        self.assertEqual(str(res), txt)
    
    def test_qgiambelli_1(self):
        res = self.ig.qgiambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_qgiambelli_2(self):
        res = self.ig.qgiambelli('S[2,1]*S[2,1]*S[2,1]')
        txt = 'S[1]^3*S[2]^3 - 3*S[1]^2*S[2]^2*S[3] + 3*S[1]*S[2]*S[3]^2 - S[3]^3'
        self.assertEqual(str(res), txt)

    def test_qmult(self):
        res = self.ig.qmult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = 'S[1]*q + S[3]*q + 2*S[4,2]'
        self.assertEqual(str(res), txt)

    def test_qtoS(self):
        res = self.ig.qtoS('S[2,1]*S[2,1]*S[2,1]')
        txt = '4*S[3,1]*q + 5*S[4]*q'
        self.assertEqual(str(res), txt)
    
    def test_dualize(self):
        res = self.ig.dualize('S[1]+S[2]')
        txt = 'S[4,1] + S[4,2]'
        self.assertEqual(str(res), txt)
    
    def test_pieri_simple(self):
        res = self.ig.pieri(1, 'S[2,1]')
        txt = '2*S[3,1] + S[4]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_plus(self):
        res = self.ig.pieri(1, 'S[2,1] + S[3,2]')
        txt = '2*S[3,1] + S[4] + S[4,2]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus(self):
        res = self.ig.pieri(1, 'S[2,1] - S[3,2]')
        txt = '2*S[3,1] + S[4] - S[4,2]'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus_and_coef(self):
        res = self.ig.pieri(1, 'S[2,1] - 7*S[3,2]')
        txt = '2*S[3,1] + S[4] - 7*S[4,2]'
        self.assertEqual(str(res), txt)
        
    def test_act(self):
        res = self.ig.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = '2*S[3,1] + S[4] + S[4,2]'
        self.assertEqual(str(res), txt)
    
    def test_giambelli(self):
        res = self.ig.giambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_mult(self):
        res = self.ig.mult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = '2*S[4,2]'
        self.assertEqual(str(res), txt)

    def test_toS(self):
        res = self.ig.toS('S[2,1]*S[2,1]*S[2,1]')
        txt = '0'
        self.assertEqual(str(res), txt)


if __name__ == '__main__':
    unittest.main()


