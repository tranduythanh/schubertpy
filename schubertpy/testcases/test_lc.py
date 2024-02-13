from ..qcalc import *
from ..schur import *
import unittest

class TestSpec2Num(unittest.TestCase):
    
    def test_single_part(self):
        OG(2, 6)
        sc = Schur([1])
        self.assertEqual(spec2num(sc), 1)
        
    def test_multiple_parts_type_D(self):
        Gr(2, 5)
        sc = Schur([1, 0])
        with self.assertRaises(ValueError):
            spec2num(sc)
            
    def test_multiple_parts_type_not_D(self):
        OG(2, 6)
        sc = Schur([1, 0])
        self.assertEqual(spec2num(sc), -1)
        
    def test_invalid_input(self):
        OG(2, 6)
        sc = "invalid"
        with self.assertRaises(ValueError):
            spec2num(sc)


class Test_LC(unittest.TestCase):
    
    def test_01(self):
        f = lambda arr: Schur([x+1 for x in arr])
        s1 = Schur([1,2])
        s2 = Schur([3,4])
        lc = LinearCombination(f"q*{s1.symbol()} + 7*{s2.symbol()}")
        res = lc.apply(f)
        self.assertEqual(str(res), 'S[2,3]*q + 7*S[4,5]')

        lc = LinearCombination("q*S[1,2] + 7*S[3,4]")
        res = lc.apply(f)
        self.assertEqual(str(res), 'S[2,3]*q + 7*S[4,5]')

    def test_02(self):
        txt = 'S[3,1] + S[2,2]'
        res = LinearCombination(txt).list_schur_oprands()
        self.assertEqual(str(res), '[S[2,2], S[3,1]]')


class Test_apply(unittest.TestCase):
    
    def test_01(self):
        f = lambda arr: Schur([x+1 for x in arr])
        s1 = Schur([1,2])
        s2 = Schur([3,4])
        lc = LinearCombination(f"q*{s1.symbol()} + 7*{s2.symbol()}")
        res = apply_lc(f, lc)
        self.assertEqual(str(res), 'S[2,3]*q + 7*S[4,5]')

        lc = LinearCombination("q*S[1,2] + 7*S[3,4]")
        res = apply_lc(f, lc)
        self.assertEqual(str(res), 'S[2,3]*q + 7*S[4,5]')

    def test_02(self):
        res = apply_lc(lambda p: qpieriB_inner(2, p, 1, 3), '6*S[4,2]')
        txt = '6*S[3,1]*q + 6*S[]*q^2'
        self.assertEqual(str(res), txt)
        

    def test_03(self):
        res = apply_lc(lambda x: part_tilde(x, 3, 4), 'S[1,1,1] + 2*S[2,1]')
        self.assertEqual(str(res), '0')
    
    
    def test_04(self):
        lc_p1 = 'q*S[2] + q*S[1,1] + 2*S[4,2]'
        res = apply_lc(lambda p: qpieriB_inner(1, p, 1, 3), lc_p1)
        txt = '5*S[2,1]*q + S[3]*q + 2*S[4,3]'
        self.assertEqual(str(res), txt)
            
if __name__ == '__main__':
    unittest.main()