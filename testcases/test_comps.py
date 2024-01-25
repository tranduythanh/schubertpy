import unittest
from qcalc import *


class TestCalcComps(unittest.TestCase):
    
    def test_calc_comps(self):
        top1 = [6,5,4]
        bot1 = [8,7,6]
        top2 = [4,3,2]
        bot2 = [12,6,5]
        lb2 = 3
        k = 3
        d = 0
        comps = [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1, 1, 1]
        result = calc_comps(top1, bot1, top2, bot2, lb2, k, d)
        self.assertEqual(result, comps)
    

class TestCountComps(unittest.TestCase):
    
    def test_empty_lists(self):
        lam1 = []
        lam2 = []
        skipfirst = False
        k = 0
        d = 0
        result = count_comps(lam1, lam2, skipfirst, k, d)
        self.assertEqual(result, 0)
    
    # def test_no_comparisons_needed(self):
    #     lam1 = [3,2,1]
    #     lam2 = [6,5,4]
    #     skipfirst = False
    #     k = 3
    #     d = 0
    #     result = count_comps(lam1, lam2, skipfirst, k, d)
    #     self.assertEqual(result, 1)
    
    def test_comparisons_needed(self):
        lam1 = [3,2,1]
        lam2 = [4,3,2]
        skipfirst = False
        k = 3
        d = 0
        result = count_comps(lam1, lam2, skipfirst, k, d)
        self.assertEqual(result, 1)
    
    def test_skip_first_comparison(self):
        lam1 = [3,2,1]
        lam2 = [4,3,2]
        skipfirst = True
        k = 3
        d = 2
        result = count_comps(lam1, lam2, skipfirst, k, d)
        self.assertEqual(result, 0)
    
    def test_no_skip_first_comparison(self):
        lam1 = [3,2,1]
        lam2 = [4,3,2]
        skipfirst = False
        k = 3
        d = 2
        result = count_comps(lam1, lam2, skipfirst, k, d)
        self.assertEqual(result, 1)
    

if __name__ == '__main__':
    unittest.main()