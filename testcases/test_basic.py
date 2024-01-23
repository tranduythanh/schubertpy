from qcalc import *
import unittest
from unittest.mock import patch

class Test_SetType_GetType(unittest.TestCase):
    
    def test_type_A(self):
        Gr(2,5)
        self.assertEqual(get_type(), ["A", 3, 5, "Gr", 2, 5, 5])
        self.assertEqual(schub_classes(), ['S[]', 'S[1]', 'S[2]', 'S[3]', 'S[1,1]', 'S[2,1]', 'S[2,2]', 'S[3,1]', 'S[3,2]', 'S[3,3]'])
        self.assertEqual(generators(), ['S[1]', 'S[2]', 'S[3]'])
        self.assertEqual(point_class(), 'S[3,3]')

    def test_type_B_27(self):
        OG(2,7)
        self.assertEqual(get_type(), ["B", 1, 3, "OG", 2, 7, 4])
        self.assertEqual(schub_classes(), ['S[]', 'S[1]', 'S[2]', 'S[3]', 'S[4]', 'S[1,1]', 'S[2,1]', 'S[3,1]', 'S[3,2]', 'S[4,1]', 'S[4,2]', 'S[4,3]'])
        self.assertEqual(generators(), ['S[1]', 'S[2]', 'S[3]', 'S[4]'])
        self.assertEqual(point_class(), 'S[4,3]')

    def test_type_B_25(self):
        OG(2,5)
        self.assertEqual(get_type(), ["B", 0, 2, "OG", 2, 5, 4])
        self.assertEqual(schub_classes(), ['S[]', 'S[1]', 'S[2]', 'S[2,1]'])
        self.assertEqual(generators(), ['S[1]', 'S[2]'])
        self.assertEqual(point_class(), 'S[2,1]')

    def test_type_C(self):
        IG(2,6)
        self.assertEqual(get_type(), ["C", 1, 3, "IG", 2, 6, 5])
        self.assertEqual(schub_classes(), ['S[]', 'S[1]', 'S[2]', 'S[3]', 'S[4]', 'S[1,1]', 'S[2,1]', 'S[3,1]', 'S[3,2]', 'S[4,1]', 'S[4,2]', 'S[4,3]'])
        self.assertEqual(generators(), ['S[1]', 'S[2]', 'S[3]', 'S[4]'])
        self.assertEqual(point_class(), 'S[4,3]')

    def test_type_D_24(self):
        OG(2, 4)
        self.assertEqual(get_type(), ["D", 0, 1, "OG", 2, 4, 2])
        self.assertEqual(schub_classes(), ['S[]', 'S[1]'])
        self.assertEqual(generators(), ['S[1]'])
        self.assertEqual(point_class(), 'S[1]')
    
    def test_type_D_26(self):
        OG(2, 6)
        self.assertEqual(get_type(), ["D", 1, 2, "OG", 2, 6, 3])
        self.assertEqual(schub_classes(), ['S[]', 'S[1]', 'S[2]', 'S[3]', 'S[1,0]', 'S[1,1]', 'S[2,1]', 'S[3,1]', 'S[3,2]', 'S[1,1,0]', 'S[2,1,0]', 'S[3,1,0]'])
        self.assertEqual(generators(), ['S[1]', 'S[1,0]', 'S[2]', 'S[3]'])
        self.assertEqual(point_class(), 'S[3,2]')

    def test_error(self):
        with self.assertRaises(ValueError):
            OG(-1, 5)
        with self.assertRaises(ValueError):
            OG(2, -3)
        with self.assertRaises(ValueError):
            OG(2, 3)
        with self.assertRaises(ValueError):
            set_type("E", 3, 5)
        with self.assertRaises(ValueError):
            IG(2, 5)

        with self.assertRaises(TypeError):
            set_type("A", 'a', 3)
        with self.assertRaises(TypeError):
            set_type("A", 3, 'a')
        with self.assertRaises(TypeError):
            set_type(3, 3, 'a')
        with self.assertRaises(TypeError):
            Gr(3, 'a')
        with self.assertRaises(TypeError):
            Gr('a', 3)
        with self.assertRaises(TypeError):
            OG(3, 'a')
        with self.assertRaises(TypeError):
            OG('a', 3)
        with self.assertRaises(TypeError):
            IG(3, 'a')
        with self.assertRaises(TypeError):
            IG('a', 4)

class TestPartClip(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(part_clip([]), [])

    def test_no_trailing_zeros(self):
        self.assertEqual(part_clip([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_trailing_zeros(self):
        self.assertEqual(part_clip([3, 4, 5, 0, 0]), [3, 4, 5])
        self.assertEqual(part_clip([1, 0, 0, 0, 0]), [1])
    
    def test_all_zeros(self):
        self.assertEqual(part_clip([0, 0, 0, 0, 0]), [])
    
    def test_single_element_no_zero(self):
        self.assertEqual(part_clip([5]), [5])
    
    def test_single_element_zero(self):
        self.assertEqual(part_clip([0]), [])

class TestItrKstrict(unittest.TestCase):

    def test_empty_input(self):
        self.assertEqual(itr_kstrict([], 1), [])

    def test_all_zeros(self):
        self.assertEqual(itr_kstrict([0, 0, 0], 1), [])

    def test_lambda_i_lesser_than_k(self):
        self.assertEqual(itr_kstrict([3, 2, 1], 2), [3, 2, 0])

    def test_lambda_i_greater_than_k(self):
        self.assertEqual(itr_kstrict([3, 2, 1], 1), [3, 2, 0])

    def test_li_plus_i_minus_n_greater_than_k(self):
        self.assertEqual(itr_kstrict([3, 5, 2], 1), [3, 5, 1])

    def test_else_branch(self):
        self.assertEqual(itr_kstrict([3, 2, 1], 0), [3, 2, 0])


class TestPartConj(unittest.TestCase):
    
    def test_empty_list(self):
        self.assertEqual(part_conj([]), [])
        
    def test_single_element_list(self):
        self.assertEqual(part_conj([3]), [1, 1, 1])
            
    def test_unsorted_list(self):
        self.assertEqual(part_conj([5, 2]), [2, 2, 1, 1, 1])
        
    def test_duplicate_elements(self):
        self.assertEqual(part_conj([2, 2, 2]), [3, 3])
        
    def test_negative_elements(self):
        self.assertEqual(part_conj([-1, -2, -3]), [])

class TestPartItrBetween(unittest.TestCase):
    
    def test_ok(self):
        self.assertEqual(part_itr_between([2,1],[3,1],[3,2]), [1,1])
        self.assertEqual(part_itr_between([2,1],[2,2],[3,2]), [2,0])
        self.assertEqual(part_itr_between([2,1],[3,3],[3,2]), [2,0])
        self.assertEqual(part_itr_between([4,3,1],[2,2,2],[4,3,2]), [4,3,0])
        self.assertEqual(part_itr_between([2,1,1],[3,2,1],[4,3,2]), [2,0,0])
        self.assertEqual(part_itr_between([9,9],[2,1],[3,2]), [9,2])
        self.assertIsNone(part_itr_between([2,2],[2,2],[3,2]))

class TestPart2PairInner(unittest.TestCase):
    
    def test_part2pair_inner_empty_list(self):
        res = part2pair_inner([], 3)
        self.assertEqual(res, 'S[[0, 0, 0],[]]')
        
    def test_part2pair_inner_all_zeros(self):
        res = part2pair_inner([0, 0, 0], 2)
        self.assertEqual(res, 'S[[0, 0],[0]]')
    
    def test_ok(self):
        self.assertEqual(part2pair_inner([3, 1], 0), 'S[[],[3, 1]]')
        self.assertEqual(part2pair_inner([3, 1], 1), 'S[[2],[2]]')
        self.assertEqual(part2pair_inner([3, 1], 2), 'S[[2, 1],[1]]')
        self.assertEqual(part2pair_inner([3, 1], 3), 'S[[2, 1, 1],[]]')
        self.assertEqual(part2pair_inner([3, 1], 4), 'S[[2, 1, 1, 0],[]]')
        self.assertEqual(part2pair_inner([3, 1], 5), 'S[[2, 1, 1, 0, 0],[]]')
        
        

if __name__ == '__main__':
    unittest.main()
