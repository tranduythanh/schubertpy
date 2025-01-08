from schubertpy.qcalc import *
import unittest
from unittest.mock import patch

class Test_SetType_GetType(unittest.TestCase):
    
    def test_type_A(self):
        Gr(2,5)
        self.assertEqual(get_type(), ["A", 3, 5, "Gr", 2, 5, 5])
        self.assertEqual(str(schub_classes()), '[S[], S[1], S[1,1], S[2], S[2,1], S[2,2], S[3], S[3,1], S[3,2], S[3,3]]')
        self.assertEqual(str(generators()), '[S[1], S[2], S[3]]')
        self.assertEqual(str(point_class()), 'S[3,3]')

    def test_type_B_27(self):
        OG(2,7)
        self.assertEqual(get_type(), ["B", 1, 3, "OG", 2, 7, 4])
        self.assertEqual(str(schub_classes()), '[S[], S[1], S[1,1], S[2], S[2,1], S[3], S[3,1], S[3,2], S[4], S[4,1], S[4,2], S[4,3]]')
        self.assertEqual(str(generators()), '[S[1], S[2], S[3], S[4]]')
        self.assertEqual(str(point_class()), 'S[4,3]')

    def test_type_B_25(self):
        OG(2,5)
        self.assertEqual(get_type(), ["B", 0, 2, "OG", 2, 5, 4])
        self.assertEqual(str(schub_classes()), '[S[], S[1], S[2], S[2,1]]')
        self.assertEqual(str(generators()), '[S[1], S[2]]')
        self.assertEqual(str(point_class()), 'S[2,1]')

    def test_type_C(self):
        IG(2,6)
        self.assertEqual(get_type(), ["C", 1, 3, "IG", 2, 6, 5])
        self.assertEqual(str(schub_classes()), '[S[], S[1], S[1,1], S[2], S[2,1], S[3], S[3,1], S[3,2], S[4], S[4,1], S[4,2], S[4,3]]')
        self.assertEqual(str(generators()), '[S[1], S[2], S[3], S[4]]')
        self.assertEqual(str(point_class()), 'S[4,3]')

    def test_type_D_24(self):
        OG(2, 4)
        self.assertEqual(get_type(), ["D", 0, 1, "OG", 2, 4, 2])
        self.assertEqual(str(schub_classes()),'[S[], S[1]]')
        self.assertEqual(str(generators()), '[S[1]]')
        self.assertEqual(str(point_class()), 'S[1]')
    
    def test_type_D_26(self):
        OG(2, 6)
        self.assertEqual(get_type(), ["D", 1, 2, "OG", 2, 6, 3])
        self.assertEqual(str(schub_classes()), '[S[], S[1], S[1,0], S[1,1], S[1,1,0], S[2], S[2,1], S[2,1,0], S[3], S[3,1], S[3,1,0], S[3,2]]')
        self.assertEqual(str(generators()), '[S[1], S[1,0], S[2], S[3]]')
        self.assertEqual(str(point_class()), 'S[3,2]')

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


if __name__ == '__main__':
    unittest.main()
