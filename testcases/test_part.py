from qcalc import *
import unittest
from unittest.mock import patch


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

    def test_(self):
        self.assertEqual(part_conj([4,2,1,0]), [3,2,1,1])

class TestPartItrBetween(unittest.TestCase):
    
    def test_ok(self):
        self.assertEqual(part_itr_between([2,1],[3,1],[3,2]), [1,1])
        self.assertEqual(part_itr_between([2,1],[2,2],[3,2]), [2,0])
        self.assertEqual(part_itr_between([2,1],[3,3],[3,2]), [2,0])
        self.assertEqual(part_itr_between([4,3,1],[2,2,2],[4,3,2]), [4,3,0])
        self.assertEqual(part_itr_between([2,1,1],[3,2,1],[4,3,2]), [2,0,0])
        self.assertEqual(part_itr_between([9,9],[2,1],[3,2]), [9,2])
        self.assertEqual(part_itr_between([4],[3],[4]), [3])
        self.assertIsNone(part_itr_between([2,2],[2,2],[3,2]))
        

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

class TestTypeSwapInner(unittest.TestCase):
    
    def test_empty_list(self):
        self.assertEqual(type_swap_inner([], 2), 'S[]')
        
    def test_no_swap_needed(self):
        self.assertEqual(type_swap_inner([3,2,1], 4), 'S[3,2,1]')
        
    def test_swap_needed(self):
        self.assertEqual(type_swap_inner([3,2,1], 2), 'S[3,2,1,0]')
        
    def test_swap_needed_with_zero(self):
        self.assertEqual(type_swap_inner([3,2,1,0], 2), 'S[3,2,1]')
        
    def test_swap_needed_with_zero_at_end(self):
        self.assertEqual(type_swap_inner([3,2,1,0], 4), 'S[3,2,1]')

        
if __name__ == '__main__':
    unittest.main()
