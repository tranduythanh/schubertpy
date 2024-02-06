from qcalc import *
import unittest
from unittest.mock import patch

class TestPart2IndexAInner(unittest.TestCase):
    
    def test_case_1(self):
        lam = [3,2,1]
        k = 2
        n = 5
        expected = 'S[0,2,4]'
        self.assertEqual(str(part2indexA_inner(lam, k, n)), expected)
        
    def test_case_2(self):
        lam = [6,5,4]
        k = 3
        n = 7
        expected = 'S[-2,0,2,7]'
        self.assertEqual(str(part2indexA_inner(lam, k, n)), expected)
        
    def test_case_3(self):
        lam = [4,3,2]
        k = 1
        n = 6
        expected = 'S[-2,0,2,5,6]'
        self.assertEqual(str(part2indexA_inner(lam, k, n)), expected)
        
    def test_case_4(self):
        lam = [1, 1, 1]
        k = 0
        n = 3
        expected = 'S[0,1,2]'
        self.assertEqual(str(part2indexA_inner(lam, k, n)), expected)
        
    def test_case_5(self):
        lam = [0, 0, 0]
        k = 2
        n = 4
        expected = 'S[3,4]'
        self.assertEqual(str(part2indexA_inner(lam, k, n)), expected)    


class TestPart2IndexBInner(unittest.TestCase):
    
    def test_case_1(self):
        lam = [3,2,1]
        k = 2
        n = 5
        expected = 'S[5,8,10]'
        self.assertEqual(str(part2indexB_inner(lam, k, n)), expected)
        
    def test_case_2(self):
        lam = [6,5,4]
        k = 3
        n = 7
        expected = 'S[5,6,7,15]'
        self.assertEqual(str(part2indexB_inner(lam, k, n)), expected)
        
    def test_case_3(self):
        lam = [4,3,2]
        k = 1
        n = 6
        expected = 'S[4,5,6,12,13]'
        self.assertEqual(str(part2indexB_inner(lam, k, n)), expected)
        
    def test_case_4(self):
        lam = [1, 1, 1]
        k = 0
        n = 3
        expected = 'S[3,3,3]'
        self.assertEqual(str(part2indexB_inner(lam, k, n)), expected)
        
    def test_case_5(self):
        lam = [0, 0, 0]
        k = 2
        n = 4
        expected = 'S[8,9]'
        self.assertEqual(str(part2indexB_inner(lam, k, n)), expected)        


class TestPart2IndexCInner(unittest.TestCase):    
    def test_case_1(self):
        lam = [3,2,1]
        k = 2
        n = 5
        expected = 'S[5,7,9]'
        self.assertEqual(str(part2indexC_inner(lam, k, n)), expected)
        
    def test_case_2(self):
        lam = [6,5,4]
        k = 3
        n = 7
        expected = 'S[5,6,7,14]'
        self.assertEqual(str(part2indexC_inner(lam, k, n)), expected)
        
    def test_case_3(self):
        lam = [4,3,2]
        k = 1
        n = 6
        expected = 'S[4,5,6,11,12]'
        self.assertEqual(str(part2indexC_inner(lam, k, n)), expected)
        
    def test_case_4(self):
        lam = [1, 1, 1]
        k = 0
        n = 3
        expected = 'S[3,3,4]'
        self.assertEqual(str(part2indexC_inner(lam, k, n)), expected)
        
    def test_case_5(self):
        lam = [0, 0, 0]
        k = 2
        n = 4
        expected = 'S[7,8]'
        self.assertEqual(str(part2indexC_inner(lam, k, n)), expected)    


class TestPart2IndexDInner(unittest.TestCase):
    def test_case1(self):
        lam = [2, 1, 0, 0, 0]
        k = 0
        n = 1
        expected = 'S[0,1]'
        self.assertEqual(str(part2indexD_inner(lam, k, n)), expected)

    def test_case2(self):
        lam = [2, 1, 0, 0, 0]
        k = 0
        n = 2
        expected = 'S[1,2,4]'
        self.assertEqual(str(part2indexD_inner(lam, k, n)), expected)

    def test_case3(self):
        lam = [2, 1, 0, 0, 0]
        k = 1
        n = 2
        expected = 'S[2,3]'
        self.assertEqual(str(part2indexD_inner(lam, k, n)), expected)

    def test_case4(self):
        lam = [2, 1, 0, 0, 0]
        k = 2
        n = 3
        expected = 'S[4,7]'
        self.assertEqual(str(part2indexD_inner(lam, k, n)), expected)

    def test_case5(self):
        lam = [2, 1, 0, 0, 0]
        k = 3
        n = 4
        expected = 'S[7,9]'
        self.assertEqual(str(part2indexD_inner(lam, k, n)), expected)


class TestIndex2PartAInner(unittest.TestCase):
    
    def test_case_1(self):
        idx = [1,2,3]
        k = 2
        n = 5
        expected = 'S[2,2,2]'
        self.assertEqual(str(index2partA_inner(idx, k, n)), expected)
        
    def test_case_2(self):
        idx = [2,1,0]
        k = 1
        n = 4
        expected = 'S[0,2,4]'
        self.assertEqual(str(index2partA_inner(idx, k, n)), expected)
        
    def test_case_3(self):
        idx = [3, 2, 1]
        k = 0
        n = 3
        expected = 'S[-2,0,2]'
        self.assertEqual(str(index2partA_inner(idx, k, n)), expected)
        
    def test_case_4(self):
        idx = [5, 4, 3]
        k = 3
        n = 6
        expected = 'S[-1,1,3]'
        self.assertEqual(str(index2partA_inner(idx, k, n)), expected)
        
    def test_case_5(self):
        idx = [2, 1, 0]
        k = 2
        n = 4
        expected = 'S[1,3]'
        self.assertEqual(str(index2partA_inner(idx, k, n)), expected)


class TestIndex2PartCInner(unittest.TestCase):
    
    def test_case_1(self):
        idx = [3,2,1]
        k = 2
        n = 5
        expected = 'S[5,6,7]'
        self.assertEqual(str(index2partC_inner(idx, k, n)), expected)
        
    def test_case_2(self):
        idx = [2,1,0]
        k = 1
        n = 4
        expected = 'S[4,5,6]'
        self.assertEqual(str(index2partC_inner(idx, k, n)), expected)
        
    def test_case_3(self):
        idx = [3, 2, 1]
        k = 0
        n = 3
        expected = 'S[1,2,3]'
        self.assertEqual(str(index2partC_inner(idx, k, n)), expected)
        
    def test_case_4(self):
        idx = [3,4,5]
        k = 3
        n = 6
        expected = 'S[7,6,5]'
        self.assertEqual(str(index2partC_inner(idx, k, n)), expected)
        
    def test_case_5(self):
        idx = [9, 4, 0]
        k = 2
        n = 4
        expected = 'S[-2,4]'
        self.assertEqual(str(index2partC_inner(idx, k, n)), expected)    


class TestIndex2PartBInner(unittest.TestCase):
    def test_case1(self):
        idx = [1, 2, 3, 4]
        k = 2
        n = 5
        expected = 'S[7,6,5]'
        self.assertEqual(str(index2partB_inner(idx, k, n)), expected)

    def test_case2(self):
        idx = [1,2,3,70]
        k = 1
        n = 5
        expected = 'S[6,5,4,-59]'
        self.assertEqual(str(index2partB_inner(idx, k, n)), expected)

    def test_case3(self):
        idx = [10, 11, 12, 13]
        k = 4
        n = 5
        expected = 'S[1]'
        self.assertEqual(str(index2partB_inner(idx, k, n)), expected)

    def test_case4(self):
        idx = [1, 2, 3, 4, 5]
        k = 3
        n = 5
        expected = 'S[8,7]'
        self.assertEqual(str(index2partB_inner(idx, k, n)), expected)


class TestIndex2PartDInner(unittest.TestCase):
    
    def test_case_1(self):
        idx = [1, 2, 3, 4]
        k = 2
        n = 5
        expected = 'S[7,6,5,4]'
        self.assertEqual(str(index2partD_inner(idx, k, n)), expected)
        
    def test_case_2(self):
        idx = [1, 2, 3, 70]
        k = 2
        n = 5
        expected = 'S[7,6,5,-58]'
        self.assertEqual(str(index2partD_inner(idx, k, n)), expected)
        
    def test_case_3(self):
        idx = [4, 4, 6, 7]
        k = 1
        n = 2
        expected = 'S[1,2,0]'
        self.assertEqual(str(index2partD_inner(idx, k, n)), expected)
        

class TestDualizeIndexInner(unittest.TestCase):
    
    def test_dualize_index_inner_tp_D_even_N(self):
        idx = [3,2,1]
        N = 4
        tp = "D"
        expected = 'S[4,3,2]'
        self.assertEqual(str(dualize_index_inner(idx, N, tp)), expected)

    # TODO: duythanh(should confirm with author again
    #       N/2 is fraction of N, not integer
    def test_dualize_index_inner_tp_D_odd_N(self):
        idx = [3,2,1]
        N = 3
        tp = "D"
        expected = 'S[3,2,1]'
        self.assertEqual(str(dualize_index_inner(idx, N, tp)), expected)
        
    def test_dualize_index_inner_tp_not_D(self):
        idx = [3,2,1]
        N = 5
        tp = "not_D"
        expected = 'S[5,4,3]'
        self.assertEqual(str(dualize_index_inner(idx, N, tp)), expected)
        
    def test_dualize_index_inner_empty_idx(self):
        idx = []
        N = 5
        tp = "D"
        expected = 'S[]'
        self.assertEqual(str(dualize_index_inner(idx, N, tp)), expected)
        





if __name__ == '__main__':
    unittest.main()
