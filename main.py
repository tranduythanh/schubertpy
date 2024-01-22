from qcalc import *
from util import *

Gr(2,5)
print(type_string())
print(all_kstrict(1,2,4))
print(schub_classes())

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