from qcalc import *
import unittest
from unittest.mock import patch

class Test_SetType_GetType(unittest.TestCase):
    
    def test_type_A(self):
        Gr(2,5)
        self.assertEqual(get_type(), ["A", 3, 5, "Gr", 2, 5, 5])

    def test_type_B(self):
        OG(2,5)
        self.assertEqual(get_type(), ["B", 0, 2, "OG", 2, 5, 4])

    def test_type_C(self):
        IG(2,6)
        self.assertEqual(get_type(), ["C", 1, 3, "IG", 2, 6, 5])

    def test_type_D(self):
        OG(2, 4)
        self.assertEqual(get_type(), ["D", 0, 1, "OG", 2, 4, 2])

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
    
if __name__ == "__main__":
    unittest.main()
