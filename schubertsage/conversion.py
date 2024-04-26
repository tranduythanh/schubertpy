from schubertpy.schur import Schur
# from sage.combinat.sf.schur import SymmetricFunctions
from sage.symbolic.ring import SR
from sage.symbolic.function import SymbolicFunction

from sage.all import SymmetricFunctions, SymmetricFunctionAlgebra_schur
sym = SymmetricFunctions(SR)
S = sym.schur()

# Function to convert from SageMath Schur function to Schur object
def sage_schur_to_schur(sage_schur: SymmetricFunctionAlgebra_schur) -> Schur:
    print(type(sage_schur))
    if sage_schur.parent()!=S:
        raise ValueError("SageMath Schur function is not a Schur function")
    
    partition = list(sage_schur.monomial_coefficients().keys())[0]
    print(partition)
    return Schur(partition)

def schur_to_sage_schur(schur) -> SymmetricFunctionAlgebra_schur:
    return S(schur.partition)