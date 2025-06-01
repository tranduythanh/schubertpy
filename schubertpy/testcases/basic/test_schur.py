import unittest
from sympy import symbols
from schubertpy.schur import Schur

class TestToPolynomial(unittest.TestCase):
    
    def test_to_polynomial_with_positive_n(self):
        x, y, z = symbols('x1 x2 x3')
        schur = Schur([3, 2])
        polynomial = schur.to_polinomial_str(3)
        expected_polynomial = "x1^3*x2^2 + x1^3*x2*x3 + x1^3*x3^2 + x1^2*x2^3 + 2*x1^2*x2^2*x3 + 2*x1^2*x2*x3^2 + x1^2*x3^3 + x1*x2^3*x3 + 2*x1*x2^2*x3^2 + x1*x2*x3^3 + x2^3*x3^2 + x2^2*x3^3"
        self.assertEqual(polynomial, expected_polynomial)
        
if __name__ == '__main__':
    unittest.main()