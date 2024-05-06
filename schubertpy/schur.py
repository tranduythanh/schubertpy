from functools import total_ordering

from typing import *
import sympy as sp
from .const import *
import ast

class Schur(object):
    def __init__(self, p: Union[List[int], sp.Expr, str]):
        # Set self.p to p or [] if p is None
        if isinstance(p, (list, tuple)):
            self.p = p if p is not None else []
            return
        p = toSchur(p)
        self.p = p.p

    def __str__(self):
        return f"S{self.p}".replace(' ', '')

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        # Check if 'other' is instance of Schur and compare
        if isinstance(other, Schur):
            return self.p == other.p
        return NotImplemented

    def __lt__(self, other):
        # Check if 'other' is instance of Schur and compare
        if isinstance(other, Schur):
            return self.p < other.p
        return NotImplemented
    
    def __hash__(self):
        return hash(str(self.p))
    

    def __add__(self, other):
        if isinstance(other, Schur):
            return self.symbol() + other.symbol()
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return self.symbol() + other
        if other.expr and isinstance(other.expr, sp.Expr):
            return self.symbol() + other.expr
        raise ValueError(f"Invalid type for addition: {type(other)}")
    
    __radd__ = __add__
    
    def __mul__(self, other):
        if isinstance(other, Schur):
            return self.symbol() * other.symbol()
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return self.symbol() * other
        if other.expr and isinstance(other.expr, sp.Expr):
            return self.symbol() * other.expr
        raise ValueError(f"Invalid type for addition: {type(other)}")
    
    __rmul__ = __mul__
    
    def __pow__(self, other):
        if isinstance(other, Schur):
            return self.symbol() ** other.symbol()
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return self.symbol() ** other
        if other.expr and isinstance(other.expr, sp.Expr):
            return self.symbol() ** other.expr
        raise ValueError(f"Invalid type for addition: {type(other)}")

    def symbol(self) -> sp.Symbol:
        return sp.parse_expr(self.__str__().translate(ftable))

    def partition(self) -> List[int]:
        return self.p


def unique_schur_list(schur_list: List[Schur]):
    return  sorted(list(set(schur_list)))



def isSchur(expr: sp.Expr) -> bool:
    return expr.is_Symbol and str(expr).startswith('S')


def translate_schur(sym: Union[sp.Symbol, str]) -> str:
    # Convert symbol back to string and translate using reverse table
    return str(sym).translate(btable)

def toSchur(sym: Union[sp.Symbol, str]) -> Schur:
        # Convert symbol back to string and translate using reverse table
        parsed_str = str(sym).translate(btable).replace('S', '')
        # Parse the string back into a list structure
        pl = ast.literal_eval(parsed_str)
        if isinstance(pl, list) and all(isinstance(i, list) or isinstance(i, int) for i in pl):
            return Schur(pl)
        raise ValueError("Input string does not represent a list of lists")
        