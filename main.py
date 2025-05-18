from schubertpy.qcalc import *
from schubertpy.utils.mix import *
from schubertpy.schur import *

# Gr(2,5)
# print(type_string())
# print(all_kstrict(1,2,4))
# print(schub_classes())

def yd(partition):
    print('Young diagram for partition: ' + str(partition))
    for row in partition:
        print(('[]') * row)

# Example usage
lambda_partition = (2, 1)
yd(lambda_partition)

lam = []
if not lam:
    print('Empty list')

from sympy import Function, IndexedBase, Indexed, sympify, symbols, Add, Mul, Pow, parse_expr

# Example usage
expr_str = "S_3j2j1 + S_2j1"
expr = parse_expr(expr_str)
print(expr, isinstance(expr, Add))
print(expr.args)

expr_str = "-S_3j2j1 - S_2j1"
expr = parse_expr(expr_str)
print(expr, isinstance(expr, Add))
print(expr.args)

expr_str = "S_3j2j1**S_2j1"
expr = parse_expr(expr_str)
print(expr, isinstance(expr, Pow))
print(expr.args)

expr_str = "S_3j2j1*S_2j1"
expr = parse_expr(expr_str)
print(expr, isinstance(expr, Mul))
print(expr.args)

s1 = Schur([3,2,1])
print(s1, type(s1))
# Test the function
input_str = "[[2,1],[3,2,1,1]]"

import sympy as sp

def apply_func_to_expr(func, expr):
    if expr.is_Atom:
        # Base case: if the expression is an atom (cannot be decomposed further),
        # apply the function directly to the atom.
        return func(expr)
    else:
        # Recursive case: apply the function to each operand of the expression
        return expr.func(*[apply_func_to_expr(func, arg) for arg in expr.args])

# Usage:
x, y = sp.symbols('x y')
expr = x + y**2

# Define any function you want to apply, for example, increment each number by 1
def increment_by_one(atom):
    if atom.is_Number:
        return atom + 1
    return atom

new_expr = apply_func_to_expr(increment_by_one, expr)
print(new_expr)  # Output will depend on the function and expression
print(new_expr.shur_expansion())  # Output will depend on the function and expression

