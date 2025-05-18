import unittest
from schubertpy.utils.mix import padding_right

class TestPaddingRight(unittest.TestCase):
    
    def test_padding_zero(self):
        self.assertEqual(padding_right([1, 2, 3], 0, 0), [1, 2, 3])
        
    def test_padding_positive(self):
        self.assertEqual(padding_right([1, 2, 3], 0, 2), [1, 2, 3, 0, 0])
        
    def test_padding_negative(self):
        self.assertEqual(padding_right([1, 2, 3], 0, -2), [1, 2, 3])
        
    def test_padding_empty_list(self):
        self.assertEqual(padding_right([], 0, 3), [0, 0, 0])
        
    def test_padding_empty_list_with_negative_count(self):
        self.assertEqual(padding_right([], 0, -3), [])
        
    def test_padding_with_non_zero_value(self):
        self.assertEqual(padding_right([1, 2, 3], 5, 2), [1, 2, 3, 5, 5])
        
    def test_padding_with_non_zero_value_and_negative_count(self):
        self.assertEqual(padding_right([1, 2, 3], 5, -2), [1, 2, 3])
        
if __name__ == '__main__':
    unittest.main()