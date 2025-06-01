from schubertpy.qcalc import *
import unittest
from unittest.mock import patch


class TestPart2PairInner(unittest.TestCase):
    
    def test_part2pair_inner_empty_list(self):
        res = part2pair_inner([], 3)
        self.assertEqual(str(res), 'S[[0,0,0],[]]')
        
    def test_part2pair_inner_all_zeros(self):
        res = part2pair_inner([0, 0, 0], 2)
        self.assertEqual(str(res), 'S[[0,0],[0]]')
    
    def test_ok(self):
        self.assertEqual(str(part2pair_inner([3, 1], 0)), 'S[[],[3,1]]')
        self.assertEqual(str(part2pair_inner([3, 1], 1)), 'S[[2],[2]]')
        self.assertEqual(str(part2pair_inner([3, 1], 2)), 'S[[2,1],[1]]')
        self.assertEqual(str(part2pair_inner([3, 1], 3)), 'S[[2,1,1],[]]')
        self.assertEqual(str(part2pair_inner([3, 1], 4)), 'S[[2,1,1,0],[]]')
        self.assertEqual(str(part2pair_inner([3, 1], 5)), 'S[[2,1,1,0,0],[]]')


class TestPair2PartInner(unittest.TestCase):
    
    def test_pair2part_inner_empty_list(self):
        res = pair2part_inner([[0,0,0], []])
        self.assertEqual(str(res), 'S[]')
        
    def test_pair2part_inner_all_zeros(self):
        with self.assertRaises(IndexError):
            pair2part_inner([[0, 0, 0], [2]])
        with self.assertRaises(IndexError):
            pair2part_inner([[1], [3, 1]])
    
    def test_ok(self):
        self.assertEqual(str(pair2part_inner([[], [3,1]])), 'S[3,1]')
        self.assertEqual(str(pair2part_inner([[2], [3,1]])), 'S[4,2]')
        self.assertEqual(str(pair2part_inner([[3], [3,1]])), 'S[4,2,1]')
        self.assertEqual(str(pair2part_inner([[4], [3,1]])), 'S[4,2,1,1]')
        self.assertEqual(str(pair2part_inner([[5], [3,1]])), 'S[4,2,1,1,1]')
        self.assertEqual(str(pair2part_inner([[5], [3,1,0]])), 'S[4,2,1,1,1,0]')
        


if __name__ == '__main__':
    unittest.main()
