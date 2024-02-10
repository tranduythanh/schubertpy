from qcalc import *
from schur import *
import sympy as sp
import csv
import unittest
from csv_bijection import check_bijection_with_permutation as isbijection

class TestWithCSVFile(unittest.TestCase):

    def test_1(self):
        data_to_write = []
        IG(2, 6)
        for h in generators():
            for sc in schub_classes():
                res = qmult(h.symbol(), sc.symbol())
                res = sp.simplify(res.expr)
                data_row = [
                    str(h), 
                    str(sc),
                    decode(str(res)).replace(' ', '')
                ]  # Example format
                data_to_write.append(data_row)

        temp_csv_filename = './testcases/temp_ig26.csv'
        with open(temp_csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
            for row in data_to_write:
                if not any(row):
                    continue
                try:
                    writer.writerow(row)
                except csv.Error as e:
                    print(f'Error writing row {row}: {e}')

        result = isbijection(temp_csv_filename, './testcases/ig26.csv')

        self.assertTrue(result)
    

    def test_2(self):
        data_to_write = []
        OG(2, 6)
        for s1 in schub_classes():
            for s2 in schub_classes():
                res = qmult(s1.symbol(), s2.symbol())
                res = sp.simplify(res.expr)
                data_row = [
                    str(s1), 
                    str(s2),
                    decode(str(res)).replace(' ', '')
                ]  # Example format
                data_to_write.append(data_row)

        temp_csv_filename = './testcases/temp_og26.csv'
        with open(temp_csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
            for row in data_to_write:
                if not any(row):
                    continue
                try:
                    writer.writerow(row)
                except csv.Error as e:
                    print(f'Error writing row {row}: {e}')

        result = isbijection(temp_csv_filename, './testcases/og26.csv')

        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
