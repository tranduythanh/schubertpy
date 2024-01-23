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






if __name__ == '__main__':
    unittest.main()
