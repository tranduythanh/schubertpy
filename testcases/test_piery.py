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

    
# class TestPieriItrA(unittest.TestCase):

#     # def test_empty_lam(self):
#     #     self.assertIsNone(pieri_itrA([], [1], [2]))

#     # def test_last_element(self):
#     #     # Assuming certain behaviors from _pieri_fillA
#     #     self.assertIsNone(pieri_itrA([1], [1], [2]))
#     #     self.assertIsNone(pieri_itrA([2], [1], [2]))
#     #     self.assertIsNone(pieri_itrA([0], [1], [2]))

#     # def test_lam_gt_inner(self):
#     #     # Assuming certain behaviors from _pieri_fillA
#     #     self.assertIsNone(pieri_itrA([2, 3], [1, 2], [2, 3]))
#     #     self.assertIsNone(pieri_itrA([1, 3], [1, 2], [2, 3]))

#     # def test_loop_execution(self):
#     #     # Assuming certain behaviors from _pieri_fillA
#     #     self.assertIsNone(pieri_itrA([2, 3, 4], [1, 2, 3], [2, 3, 4]))

#     # def test_return_none(self):
#     #     self.assertIsNone(pieri_itrA([2], [3], [4]))

#     # def test_modify_lam_inside_loop(self):
#     #     self.assertIsNone(pieri_itrA([3, 3], [2, 2], [4, 4]))

#     # def test_all_lists_empty(self):
#     #     self.assertIsNone(pieri_itrA([], [], []))
#     #     self.assertIsNone(pieri_itrA([2,2], [2,1], [3,2]))
#     #     self.assertIsNone(pieri_itrA([1, 0, 0], [1, 0, 0], [2, 1, 0]))
#     #     self.assertIsNone(pieri_itrA([3, 3], [3, 2], [3, 3]))
#     #     self.assertIsNone(pieri_itrA([2, 1, 0], [2, 1, 0], [2, 2, 1]))

#     def test_not_none_cases(self):
#         # self.assertEqual(pieri_itrA([3,1], [2,1], [3,2]), [2,2])
#         self.assertEqual(pieri_itrA([2,1,0], [1,0,0], [2,1,0]), [2,0,0])


if __name__ == '__main__':
    unittest.main()
