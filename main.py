from qcalc import *
from util import *

Gr(2,5)
print(type_string())
print(all_kstrict(1,2,4))
print(schub_classes())

inner = padding_right([2,1], 0, 3)
print(inner)
outer = [9] + inner[:-1]
print(outer)