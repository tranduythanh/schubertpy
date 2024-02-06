from qcalc import *
from util import *
from schur import *

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

from sympy import Function, IndexedBase, Indexed, sympify, symbols, Add

# Example usage
expr_str = "S_3j2j1 + S_2j1"
expr = sympify(expr_str)
print(expr, isinstance(expr, Add))
print(expr.args)

s1 = Schur([3,2,1])
print(s1, type(s1))
# Test the function
input_str = "[[2,1],[3,2,1,1]]"
print(parse(input_str))
