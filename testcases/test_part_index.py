from qcalc import *
import unittest
from unittest.mock import patch

class TestPart2IndexAInner(unittest.TestCase):
    
    def test_case_1(self):
        lam = [3,2,1]
        k = 2
        n = 5
        expected = 'S[0,2,4]'
        self.assertEqual(part2indexA_inner(lam, k, n), expected)
        
    def test_case_2(self):
        lam = [6,5,4]
        k = 3
        n = 7
        expected = 'S[-2,0,2,7]'
        self.assertEqual(part2indexA_inner(lam, k, n), expected)
        
    def test_case_3(self):
        lam = [4,3,2]
        k = 1
        n = 6
        expected = 'S[-2,0,2,5,6]'
        self.assertEqual(part2indexA_inner(lam, k, n), expected)
        
    def test_case_4(self):
        lam = [1, 1, 1]
        k = 0
        n = 3
        expected = 'S[0,1,2]'
        self.assertEqual(part2indexA_inner(lam, k, n), expected)
        
    def test_case_5(self):
        lam = [0, 0, 0]
        k = 2
        n = 4
        expected = 'S[3,4]'
        self.assertEqual(part2indexA_inner(lam, k, n), expected)    


class TestPart2IndexBInner(unittest.TestCase):
    
    def test_case_1(self):
        lam = [3,2,1]
        k = 2
        n = 5
        expected = 'S[5,8,10]'
        self.assertEqual(part2indexB_inner(lam, k, n), expected)
        
    def test_case_2(self):
        lam = [6,5,4]
        k = 3
        n = 7
        expected = 'S[5,6,7,15]'
        self.assertEqual(part2indexB_inner(lam, k, n), expected)
        
    def test_case_3(self):
        lam = [4,3,2]
        k = 1
        n = 6
        expected = 'S[4,5,6,12,13]'
        self.assertEqual(part2indexB_inner(lam, k, n), expected)
        
    def test_case_4(self):
        lam = [1, 1, 1]
        k = 0
        n = 3
        expected = 'S[3,3,3]'
        self.assertEqual(part2indexB_inner(lam, k, n), expected)
        
    def test_case_5(self):
        lam = [0, 0, 0]
        k = 2
        n = 4
        expected = 'S[8,9]'
        self.assertEqual(part2indexB_inner(lam, k, n), expected)        


class TestPart2IndexCInner(unittest.TestCase):    
    def test_case_1(self):
        lam = [3,2,1]
        k = 2
        n = 5
        expected = 'S[5,7,9]'
        self.assertEqual(part2indexC_inner(lam, k, n), expected)
        
    def test_case_2(self):
        lam = [6,5,4]
        k = 3
        n = 7
        expected = 'S[5,6,7,14]'
        self.assertEqual(part2indexC_inner(lam, k, n), expected)
        
    def test_case_3(self):
        lam = [4,3,2]
        k = 1
        n = 6
        expected = 'S[4,5,6,11,12]'
        self.assertEqual(part2indexC_inner(lam, k, n), expected)
        
    def test_case_4(self):
        lam = [1, 1, 1]
        k = 0
        n = 3
        expected = 'S[3,3,4]'
        self.assertEqual(part2indexC_inner(lam, k, n), expected)
        
    def test_case_5(self):
        lam = [0, 0, 0]
        k = 2
        n = 4
        expected = 'S[7,8]'
        self.assertEqual(part2indexC_inner(lam, k, n), expected)    




if __name__ == '__main__':
    unittest.main()
