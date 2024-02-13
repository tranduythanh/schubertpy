# from qcalc import *
# from schur import *
# import sympy as sp
# import csv
# import unittest
# from csv_bijection import check_bijection_with_permutation as isbijection


# # Dispatcher to map the command to the appropriate function
# def dispatch(command, params):
#     if command == "OG":
#         OG(*params)
#     elif command == "IG":
#         IG(*params)
#     elif command == "Gr":
#         Gr(*params)
#     else:
#         print(f"Unknown command: {command}")

# class TestWithCSVFile(unittest.TestCase):

#     def test_1(self):
#         csv_file_path = './testcases/testcase.csv'
#         with open(csv_file_path, newline='') as csvfile:
#             csv_reader = csv.reader(csvfile, delimiter=';')
#             for row in csv_reader:
#                 command_with_params = row[0].split('(')
#                 command = command_with_params[0]
#                 params = command_with_params[1][:-1]
#                 params = params.split(',')
#                 params = [int(p) for p in params]
                
#                 dispatch(command, params)
                
#                 s1 = row[2]
#                 s2 = row[3]
                
#                 result = None
#                 try:
#                     result = qmult(s1, s2)
#                 except Exception as e:
#                     print("current row:", row)
#                     raise Exception(f"qmult failed: {e}")
                
#                 result = sp.expand(result.expr).simplify()
                
#                 expected_result = sp.parse_expr(encode(row[4].replace('^', '**')))
#                 expected_result = sp.expand(expected_result).simplify()
                
#                 self.assertTrue(result == expected_result)
#                 print(f"ok\t{row}")


# if __name__ == '__main__':
#     unittest.main()
