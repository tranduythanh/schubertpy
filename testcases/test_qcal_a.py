from qcalc import *
import unittest
from unittest.mock import patch

class Test_qcal(unittest.TestCase):
    
    def test_type_A(self):
        Gr(2,5)
        res = qpieri(1, 'S[2,1]+S[3,2]')
        self.assertEqual(str(res), 'S[3,1] + S[2,2] + S[3,3] + S[1]*q')
        
        # > qact(S[1]+S[2]*S[3], S[2,1]+S[3,2]);
        # S[3, 1] + S[2, 2] + S[3, 3] + q S[1] + q S[3] + q S[2, 1] + q S[3, 2]

        #         2
        #     + q  S[]

        # > qgiambelli(S[2,1]*S[2,1]);
        #                         2     2                          2
        #                     S[2]  S[1]  - 2 S[3] S[2] S[1] + S[3]

        # > qmult(S[2,1], S[2,1]+S[3,2]);
        #                     S[3, 3] + q S[1] + q S[3] + q S[2, 1]

        # > qtoS(S[2,1]*S[2,1]*S[2,1]);
        #                         2 q S[3, 1] + q S[2, 2]
        
        


if __name__ == '__main__':
    unittest.main()


