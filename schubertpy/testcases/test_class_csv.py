from schubertpy.grassmannian import *
from schubertpy.isotropic_grassmannian import *
from schubertpy.orthogonal_grassmannian import *
import sympy as sp
import csv
import unittest
import time
from schubertpy.csv_bijection import check_bijection_with_permutation as isbijection
from schubertpy.utils.const import encode


# Dispatcher to map the command to the appropriate function
def dispatch(command, params):
    if command == "OG":
        return OrthogonalGrassmannian(*params)
    elif command == "IG":
        return IsotropicGrassmannian(*params)
    elif command == "Gr":
        return Grassmannian(*params)
    else:
        print(f"Unknown command: {command}")

class TestWithCSVFile(unittest.TestCase):

    def test_1(self):
        csv_file_path = './schubertpy/testcases/results.csv'
        count = 0
        with open(csv_file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            for row in csv_reader:
                count += 1
                command_with_params = row[0].split('(')
                command = command_with_params[0]
                params = command_with_params[1][:-1]
                params = params.split(',')
                params = [int(p) for p in params]
                
                gr = dispatch(command, params)

                if count%1000 == 0:
                    print(count)
                
                s1 = row[2]
                s2 = row[3]
                
                result = None
                start = time.time()
                try:
                    result = gr.qmult(s1, s2)
                except Exception as e:
                    print("current row:", row)
                    raise Exception(f"qmult failed: {e}")
                
                elapsed_time = time.time() - start
                
                result = sp.expand(result.expr).simplify()
                
                expected_result = sp.parse_expr(encode(row[4].replace('^', '**')))
                expected_result = sp.expand(expected_result).simplify()
                
                self.assertTrue(result == expected_result)
                print(f"ok\t{elapsed_time}\t{row}")
    
    def test_2(self):
        csv_file_path = './schubertpy/testcases/results.csv'
        count = 0
        with open(csv_file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            for row in csv_reader:
                # print("\n\n=====================================================")
                # print(f"Current test case: {row[0]}\t {row[1]}({row[2]}, {row[3]}) = {row[4]}")

                count += 1
                command_with_params = row[0].split('(')
                command = command_with_params[0]
                params = command_with_params[1][:-1]
                params = params.split(',')
                params = [int(p) for p in params]
                
                if command != "Gr":
                    continue


                gr = dispatch(command, params)

                if count%1000 == 0:
                    print(count)
                
                s1 = row[2]
                s2 = row[3]
                
                result = None
                start = time.time()
                try:
                    result = gr.qmult_rh(s1, s2)
                except Exception as e:
                    print("current row:", row)
                    raise Exception(f"qmult_rh failed: {e}")
                
                elapsed_time = time.time() - start
                
                # print("-----> result\t", LinearCombination(result))
                result = sp.expand(result.expr).simplify()
                
                expected_result = sp.parse_expr(encode(row[4].replace('^', '**')))
                expected_result = sp.expand(expected_result).simplify()
                
                
                # print("-----> expected\t", LinearCombination(expected_result))
                self.assertTrue(result == expected_result)
                print(f"ok\t{elapsed_time}\t{row}")


if __name__ == '__main__':
    unittest.main()
