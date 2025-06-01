from schubertpy.qcalc import *
from schubertpy import Grassmannian, OrthogonalGrassmannian, IsotropicGrassmannian
import unittest
from unittest.mock import patch

class Test_SetType_GetType(unittest.TestCase):
    
    def test_type_A(self):
        gr = Grassmannian(2, 5)
        expected_type = ["A", 3, 5, "Gr", 2, 5, 5]
        actual_type = gr.get_type_data()
        self.assertEqual(actual_type, expected_type)
        self.assertEqual(str(gr.schub_classes()), '[S[], S[1], S[1,1], S[2], S[2,1], S[2,2], S[3], S[3,1], S[3,2], S[3,3]]')
        self.assertEqual(str(gr.generators()), '[S[1], S[2], S[3]]')
        self.assertEqual(str(gr.point_class()), 'S[3,3]')

    def test_type_B_27(self):
        og = OrthogonalGrassmannian(2, 7)
        expected_type = ["B", 1, 3, "OG", 2, 7, 4]
        actual_type = og.get_type_data()
        self.assertEqual(actual_type, expected_type)
        self.assertEqual(str(og.schub_classes()), '[S[], S[1], S[1,1], S[2], S[2,1], S[3], S[3,1], S[3,2], S[4], S[4,1], S[4,2], S[4,3]]')
        self.assertEqual(str(og.generators()), '[S[1], S[2], S[3], S[4]]')
        self.assertEqual(str(og.point_class()), 'S[4,3]')

    def test_type_B_25(self):
        og = OrthogonalGrassmannian(2, 5)
        expected_type = ["B", 0, 2, "OG", 2, 5, 4]
        actual_type = og.get_type_data()
        self.assertEqual(actual_type, expected_type)
        self.assertEqual(str(og.schub_classes()), '[S[], S[1], S[2], S[2,1]]')
        self.assertEqual(str(og.generators()), '[S[1], S[2]]')
        self.assertEqual(str(og.point_class()), 'S[2,1]')

    def test_type_C(self):
        ig = IsotropicGrassmannian(2, 6)
        expected_type = ["C", 1, 3, "IG", 2, 6, 5]
        actual_type = ig.get_type_data()
        self.assertEqual(actual_type, expected_type)
        self.assertEqual(str(ig.schub_classes()), '[S[], S[1], S[1,1], S[2], S[2,1], S[3], S[3,1], S[3,2], S[4], S[4,1], S[4,2], S[4,3]]')
        self.assertEqual(str(ig.generators()), '[S[1], S[2], S[3], S[4]]')
        self.assertEqual(str(ig.point_class()), 'S[4,3]')

    def test_type_D_24(self):
        og = OrthogonalGrassmannian(2, 4)
        expected_type = ["D", 0, 1, "OG", 2, 4, 2]
        actual_type = og.get_type_data()
        self.assertEqual(actual_type, expected_type)
        self.assertEqual(str(og.schub_classes()),'[S[], S[1]]')
        self.assertEqual(str(og.generators()), '[S[1]]')
        self.assertEqual(str(og.point_class()), 'S[1]')
    
    def test_type_D_26(self):
        og = OrthogonalGrassmannian(2, 6)
        expected_type = ["D", 1, 2, "OG", 2, 6, 3]
        actual_type = og.get_type_data()
        self.assertEqual(actual_type, expected_type)
        self.assertEqual(str(og.schub_classes()), '[S[], S[1], S[1,0], S[1,1], S[1,1,0], S[2], S[2,1], S[2,1,0], S[3], S[3,1], S[3,1,0], S[3,2]]')
        self.assertEqual(str(og.generators()), '[S[1], S[1,0], S[2], S[3]]')
        self.assertEqual(str(og.point_class()), 'S[3,2]')

    def test_error(self):
        with self.assertRaises(ValueError):
            OrthogonalGrassmannian(-1, 5)
        with self.assertRaises(ValueError):
            OrthogonalGrassmannian(2, -3)
        with self.assertRaises(ValueError):
            IsotropicGrassmannian(2, 5)

        # Note: Type errors for constructor parameters are handled by Python's type system
        # The old tests with string arguments would now raise TypeError during construction


if __name__ == '__main__':
    unittest.main()
