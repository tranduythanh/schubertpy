from functools import total_ordering
from typing import *
from schur import *
from const import *
import sympy as sp
import ast


class LinearCombination(object):
    def __init__(self, expr: Union[str, sp.Expr, int, 'LinearCombination']):
        if isinstance(expr, str):
            expr = expr.translate(btable)
            self.expr = sp.sympify(expr)
        elif isinstance(expr, sp.Expr):
            self.expr = expr
        elif isinstance(expr, int):
            self.expr = sp.sympify(expr)
        elif isinstance(expr, LinearCombination):
            self.expr = expr.expr
        else:
            raise ValueError(f"Invalid type for LinearCombination: {type(expr)}")

    def __str__(self):
        return translate_schur(self.expr)

    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        if isinstance(other, LinearCombination):
            return LinearCombination(self.expr + other.expr)
        if isinstance(other, int):
            return LinearCombination(self.expr + other)
        if isinstance(other, sp.Expr):
            return LinearCombination(self.expr + other)
        raise ValueError(f"Invalid type for addition: {type(other)}")
    
    def __mul__(self, other):
        if isinstance(other, LinearCombination):
            return LinearCombination(self.expr * other.expr)
        if isinstance(other, int):
            return LinearCombination(self.expr * other)
        if isinstance(other, sp.Expr):
            return LinearCombination(self.expr * other)
        raise ValueError(f"Invalid type for addition: {type(other)}")
    
    def __pow__(self, other):
        if isinstance(other, LinearCombination):
            return LinearCombination(self.expr ** other.expr)
        if isinstance(other, int):
            return LinearCombination(self.expr ** other)
        if isinstance(other, sp.Expr):
            return LinearCombination(self.expr ** other)
        raise ValueError(f"Invalid type for addition: {type(other)}")
    
    def is_operator(self, op: str) -> bool:
        if op == '+':
            return isinstance(self.expr, sp.Add)
        if op == '-':
            return isinstance(self.expr, sp.Substr)
        elif op == '*':
            return isinstance(self.expr, sp.Mul)
        elif op == '/':
            return isinstance(self.expr, sp.Div)
        elif op == '^':
            return isinstance(self.expr, sp.Pow)
        
        raise ValueError(f"Invalid operator: {op}")
    

    def apply(self, func: Callable) -> 'LinearCombination':
        def recursive_apply(expr: sp.Expr) -> sp.Expr:
            if expr.is_Add or expr.is_Mul or expr.is_Pow:
                ret1 = expr.func(*[recursive_apply(arg) for arg in expr.args])
                return sp.expand(ret1)
            if isSchur(expr):
                s = toSchur(str(expr))
                res = func(s.p)
                if isinstance(res, Schur):
                    return res.symbol()
                return res
            return expr
        
        new_expr = recursive_apply(self.expr)
        return LinearCombination(str(new_expr))