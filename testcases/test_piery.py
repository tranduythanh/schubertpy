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
        self.assertEqual(pieri_fillA([], [2,1,0,0,0], [5,2,1,0,0], 2, 1), [])
        self.assertEqual(pieri_fillA([2,1], [2,1], [3,2], row_index=0, p=1), [3,1])

    
class TestPieriItrA(unittest.TestCase):

    def test_ok(self):
        self.assertEqual(pieri_itrA([3,1,0,0,0], [2,1,0,0,0], [5,2,1,0,0,0]), [2,2,0,0,0])
        self.assertEqual(pieri_itrA([3,1,0,0,0], [2,1,0,0,0], [9,2,1,0,0,0]), [2,2,0,0,0])
        self.assertEqual(pieri_itrA([2,2,0,0,0], [2,1,0,0,0], [2,2,1,0,0,0]), [2,1,1,0,0])
        self.assertIsNone(pieri_itrA([2,1,0,0,0], [2,1,0,0,0], [5,2,1,0,0,0]))
        self.assertIsNone(pieri_itrA([], [2,1,0,0,0], [5,2,1,0,0,0]))


class TestPieriSet(unittest.TestCase):
    
    def test_1(self):
        p = 1
        lam = [3,2,1]
        k = 1
        n = 3
        d = 2
        expected = [[4,2,1],[3,2,1,1]]
        self.assertEqual(pieri_set(p, lam, k, n, d), expected)

    def test_2(self):
        p = 1
        lam = [3,2,1]
        k = 0
        n = 4
        d = 2
        expected = [[4,2,1]]
        self.assertEqual(pieri_set(p, lam, k, n, d), expected)

    def test_3(self):
        p = 1
        lam = [3,2,1]
        k = 4
        n = 6
        d = 2
        expected = [[4,2,1],[3,3,1],[3,2,2],[3,2,1,1]]
        self.assertEqual(pieri_set(p, lam, k, n, d), expected)




if __name__ == '__main__':
    unittest.main()