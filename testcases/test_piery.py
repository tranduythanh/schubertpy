import unittest
from qcalc import *

class TestPieriFillA(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(pieri_fillA([2,1,0,0,0], [2,1,0,0,0], [5,2,1,0,0], 0, 1), [3,1,0,0,0])
        self.assertEqual(pieri_fillA([2,1,0,0,0], [2,1,0,0,0], [9,2,1,0,0], 0, 1), [3,1,0,0,0])
        self.assertEqual(pieri_fillA([2,1,0,0,0], [2,1,0,0,0], [2,2,1,0,0], 0, 1), [2,2,0,0,0])
        self.assertIsNone(pieri_fillA([2,1,0,0,0], [2,1,0,0,0], [2,2,1,0,0], 5, 1))
        self.assertEqual(pieri_fillA([2,1,0,0,0], [2,1,0,0,0], [5,2,1,0,0], 2, 1), [2,1,1,0,0])
        self.assertIsNone(pieri_fillA(None, [2,1,0,0,0], [5,2,1,0,0], 2, 1))
        self.assertIsNone(pieri_fillA([], [2,1,0,0,0], [5,2,1,0,0], 2, 1))

    
class TestPieriItrA(unittest.TestCase):

    def test_ok(self):
        self.assertEqual(pieri_itrA([3,1,0,0,0], [2,1,0,0,0], [5,2,1,0,0,0]), [2,2,0,0,0])
        self.assertEqual(pieri_itrA([3,1,0,0,0], [2,1,0,0,0], [9,2,1,0,0,0]), [2,2,0,0,0])
        self.assertEqual(pieri_itrA([2,2,0,0,0], [2,1,0,0,0], [2,2,1,0,0,0]), [2,1,1,0,0])
        self.assertIsNone(pieri_itrA([2,1,0,0,0], [2,1,0,0,0], [5,2,1,0,0,0]))
        self.assertIsNone(pieri_itrA([], [2,1,0,0,0], [5,2,1,0,0,0]))


class TestMiamiSwapInner(unittest.TestCase):
    def test_k_not_in_lam(self):
        lam = [3,2,1]
        k = 4
        result = miami_swap_inner(lam, k)
        self.assertEqual(result, 'S[3,2,1]')
    
    def test_even_count_greater_than_k(self):
        lam = [5,4,3,2,1]
        k = 3
        result = miami_swap_inner(lam, k)
        self.assertEqual(result, 'S[5,4,3,2,1]')
    
    def test_odd_count_greater_than_k(self):
        lam = [5,4,3,2,1]
        k = 2
        result = miami_swap_inner(lam, k)
        self.assertEqual(result, 'S[5,4,3,2,1,0]')
    
    def test_last_element_zero(self):
        lam = [3,2,1,0]
        k = 3
        result = miami_swap_inner(lam, k)
        self.assertEqual(result, 'S[3,2,1,0]')

    def test_last_element_zero_2(self):
        lam = [3,2,1,0,0,0,0]
        k = 2
        result = miami_swap_inner(lam, k)
        self.assertEqual(result, 'S[3,2,1,0,0,0]')
    
    def test_last_element_non_zero(self):
        lam = [4,3,2,1]
        k = 3
        result = miami_swap_inner(lam, k)
        self.assertEqual(result, 'S[4,3,2,1,0]')


if __name__ == '__main__':
    unittest.main()
