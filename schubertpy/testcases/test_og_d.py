from schubertpy.orthogonal_grassmannian import *
import unittest

class Test_orthogonal_grassmannian_D(unittest.TestCase):
    def setUp(self):
        self.og = OrthogonalGrassmannian(2,6)

    def test_qpieri_simple(self):
        res = self.og.qpieri(1, 'S[2,1]')
        txt = 'S[1,0]*q1'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_plus(self):
        res = self.og.qpieri(1, 'S[2,1] + S[3,2]')
        txt = 'S[1,0]*q1 + S[2,1,0]*q1 + S[]*q1*q2'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus(self):
        res = self.og.qpieri(1, 'S[2,1] - S[3,2]')
        txt = 'S[1,0]*q1 - S[2,1,0]*q1 - S[]*q1*q2'
        self.assertEqual(str(res), txt)

    def test_qpieri_with_minus_and_coef(self):
        res = self.og.qpieri(1, 'S[2,1] - 7*S[3,2]')
        txt = 'S[1,0]*q1 - 7*S[2,1,0]*q1 - 7*S[]*q1*q2'
        self.assertEqual(str(res), txt)
        
    def test_qact(self):
        res = self.og.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = 'S[1,0]*q1 + S[1,1]*q1*q2 + S[2,1,0]*q1 + S[3,1]*q1*q2 + S[3,1,0]*q1*q2 + S[]*q1*q2'
        self.assertEqual(str(res), txt)
    
    def test_qgiambelli_1(self):
        res = self.og.qgiambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_qgiambelli_2(self):
        res = self.og.qgiambelli('S[2,1]*S[2,1]*S[2,1]')
        txt = 'S[1]^3*S[2]^3 - 3*S[1]^2*S[2]^2*S[3] + 3*S[1]*S[2]*S[3]^2 - S[3]^3'
        self.assertEqual(str(res), txt)

    def test_qmult(self):
        res = self.og.qmult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = 'S[1,1]*q1*q2 + S[3]*q1'
        self.assertEqual(str(res), txt)

    def test_qmult_og(self):
        og = OrthogonalGrassmannian(2,8)
        res = og.qmult('S[2,1,0]', 'S[]')
        txt = 'S[2,1,0]'
        self.assertEqual(str(res), txt)

    def test_qtoS(self):
        res = self.og.qtoS('S[2,1]*S[2,1]*S[2,1]')
        txt = 'S[2,1,0]*q1^2'
        self.assertEqual(str(res), txt)
    
    def test_dualize(self):
        res = self.og.dualize('S[1]+S[2]')
        txt = 'S[3] + S[3,1,0]'
        self.assertEqual(str(res), txt)
        
    def test_dualize_2(self):
        res = self.og.dualize('S[3,1]*q1')
        txt = 'S[1,0]*q1'
        self.assertEqual(str(res), txt)
    
    def test_pieri_simple(self):
        res = self.og.pieri(1, 'S[2,1]')
        txt = '0'
        self.assertEqual(str(res), txt)

    def test_pieri_with_plus(self):
        res = self.og.pieri(1, 'S[2,1] + S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus(self):
        res = self.og.pieri(1, 'S[2,1] - S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)

    def test_pieri_with_minus_and_coef(self):
        res = self.og.pieri(1, 'S[2,1] - 7*S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)
        
    def test_act(self):
        res = self.og.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)
    
    def test_giambelli(self):
        res = self.og.giambelli('S[2,1]*S[2,1]')
        txt = 'S[1]^2*S[2]^2 - 2*S[1]*S[2]*S[3] + S[3]^2'
        self.assertEqual(str(res), txt)

    def test_mult(self):
        res = self.og.mult('S[2,1]', 'S[2,1]+S[3,2]')
        txt = '0'
        self.assertEqual(str(res), txt)

    def test_toS(self):
        res = self.og.toS('S[2,1]*S[2,1]*S[2,1]')
        txt = '0'
        self.assertEqual(str(res), txt)

if __name__ == '__main__':
    unittest.main()


