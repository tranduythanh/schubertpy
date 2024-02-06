from typing import *
from schur import *
import sympy as sp
import ast


class LinearCombination(object):
    def __init__(self, expr: str):
        self.expr = sp.sympify(expr)

    def __str__(self):
        return translate_schur(self.expr)

    def __repr__(self):
        return self.__str__()
    
    def is_operator(self, op: str) -> bool:
        if op == '+':
            return isinstance(self.expr, sp.Add)
        elif op == '*':
            return isinstance(self.expr, sp.Mul)
        elif op == '^':
            return isinstance(self.expr, sp.Pow)
        
        raise ValueError(f"Invalid operator: {op}")
    

    def apply(self, func: Callable) -> 'LinearCombination':
        def recursive_apply(expr: sp.Expr) -> sp.Expr:
            if expr.is_Add or expr.is_Mul or expr.is_Pow:
                return expr.func(*[recursive_apply(arg) for arg in expr.args])
            if isSchur(expr):
                s = toSchur(str(expr))
                res = func(s.p)
                if isinstance(res, Schur):
                    return res.symbol()
                return res
            return expr
        
        new_expr = recursive_apply(self.expr)
        return LinearCombination(str(new_expr))