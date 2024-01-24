import unittest
from qcalc import index2partA_inner

class TestIndex2PartAInner(unittest.TestCase):
    
    def test_case_1(self):
        idx = [1, 2, 3]
        k = 2
        n = 5
        expected = [2, 3, 4]
        self.assertEqual(index2partA_inner(idx, k, n), expected)
        
    def test_case_2(self):
        idx = [0, 1, 2]
        k = 1
        n = 4
        expected = [2, 3, 4]
        self.assertEqual(index2partA_inner(idx, k, n), expected)
        
    def test_case_3(self):
        idx = [3, 2, 1]
        k = 0
        n = 3
        expected = [1, 2, 3]
        self.assertEqual(index2partA_inner(idx, k, n), expected)
        
    def test_case_4(self):
        idx = [5, 4, 3]
        k = 3
        n = 6
        expected = [4, 5, 6]
        self.assertEqual(index2partA_inner(idx, k, n), expected)
        
    def test_case_5(self):
        idx = [2, 1, 0]
        k = 2
        n = 4
        expected = [3, 4, 5]
        self.assertEqual(index2partA_inner(idx, k, n), expected)    

if __name__ == '__main__':
    unittest.main()