import csv
import sympy as sp
from .const import *

def _read_csv_transformed(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        transformed_set = set()
        for row in reader:
            if not any(row):
                continue
            if len(row) >= 3:
                col3 = encode(row[2])
                col3 = sp.parse_expr(col3)
                col3 = sp.expand(col3).simplify()
                col3 = decode(str(col3))
                transformed_row = (row[0], row[1], col3)
                transformed_set.add(transformed_row)
        return transformed_set

def check_bijection_with_permutation(file1, file2):
    set1 = _read_csv_transformed(file1)
    set2 = _read_csv_transformed(file2)

    # Check if there's a bijection
    if len(set1) == len(set2) and len(set1.intersection(set2)) == len(set1):
        return True
    else:
        return False
