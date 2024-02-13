from functools import total_ordering
from typing import *
from .schur import *
from .const import *
import sympy as sp
import ast


class LinearCombination(object):
    def __init__(self, expr: Union[str, sp.Expr, int, 'LinearCombination']):
        if isinstance(expr, str):
            expr = expr.translate(ftable)
            self.expr = sp.parse_expr(expr)
        elif isinstance(expr, (sp.Expr, sp.Number, sp.Symbol)):
            self.expr = expr
        elif isinstance(expr, (int, float)):
            self.expr = sp.sympify(expr)
        elif isinstance(expr, LinearCombination):
            self.expr = expr.expr
        else:
            raise ValueError(f"Invalid type for LinearCombination: {type(expr)}")

    def __str__(self):
        return translate_schur(self.expr).replace('**', '^')

    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        if isinstance(other, LinearCombination):
            return LinearCombination(self.expr + other.expr)
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return LinearCombination(self.expr + other)
        raise ValueError(f"Invalid type for addition: {type(other)}")
    
    __radd__ = __add__

    def __mul__(self, other):
        # Handle scalar multiplication
        if isinstance(other, LinearCombination):
            return LinearCombination(self.expr * other.expr)
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return LinearCombination(self.expr * other)
        else:
            raise TypeError(f"Unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'")
    
    __rmul__ = __mul__

    
    def __pow__(self, other):
        if isinstance(other, LinearCombination):
            return LinearCombination(self.expr ** other.expr)
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return LinearCombination(self.expr ** other)
        raise ValueError(f"Invalid type for addition: {type(other)}")
    

    def __sub__(self, other):
        # Handle subtraction when LinearCombination is on the left
        if isinstance(other, (int, float, sp.Symbol, sp.Expr)):
            # Assuming you have a method to create a new LinearCombination from a scalar
            return self.expr - other
        if isinstance(other, LinearCombination):
            return LinearCombination(self.expr - other.expr)
        else:
            raise TypeError(f"Unsupported operand type(s) for -: '{type(self)}' and '{type(other)}'")
    
    def __rsub__(self, other):
        # Handle subtraction when LinearCombination is on the right
        if isinstance(other, (int, float, sp.Symbol, sp.Expr)):
            return other - self.expr
        if isinstance(other, LinearCombination):
            return LinearCombination(other.expr - self.expr)
        else:
            raise TypeError(f"Unsupported operand type(s) for -: '{type(other)}' and '{type(self)}'")
    
    
    def __len__(self):
        # Counting the number of top-level operands in the expression
        if self.expr.is_Add or self.expr.is_Mul:
            return len(self.expr.args)
        elif isinstance(self.expr, sp.Pow):
            # For a power expression, you might count it as a single term
            return 1
        else:
            # For other types of expressions, such as a single symbol or number,
            # you might also consider them as having a length of 1
            return 1
    
    def is_operator(self, op: str) -> bool:
        if op == '+':
            return isinstance(self.expr, sp.Add)
        elif op == '*':
            return isinstance(self.expr, sp.Mul)
        elif op == '^':
            return isinstance(self.expr, sp.Pow)
        
        raise ValueError(f"Invalid operator: {op}")
    

    def list_schur_oprands(self) -> List[Schur]:
        def recursive_list(expr: sp.Expr) -> List[Schur]:
            if expr.is_Add or expr.is_Mul or expr.is_Pow:
                return [recursive_list(arg) for arg in expr.args]
            if isSchur(expr):
                return toSchur(str(expr))
            return None
        
        return recursive_list(self.expr)


    def apply(self, func: Callable) -> 'LinearCombination':
        def recursive_apply(_expr: sp.Expr) -> sp.Expr:
            if isinstance(_expr, LinearCombination):
                _expr = _expr.expr
            if _expr.is_Add or _expr.is_Mul or _expr.is_Pow:
                ret1_args = []
                for arg in _expr.args:
                    x = recursive_apply(arg)
                    ret1_args.append(x)
                ret1 = _expr.func(*ret1_args)
                ret2 = sp.expand(ret1)
                # print("case1: ", ret2)
                return ret2
            
            if isSchur(_expr):
                s = toSchur(str(_expr))
                res = func(s.p)
                if isinstance(res, Schur):
                    # print("case2: ", res)
                    return res.symbol()
                if isinstance(res, LinearCombination):
                    # print("case2: ", res)
                    return res.expr
                # print("case2: ", res)
                return res
            
            # print("case3: ", _expr)
            return _expr
        
        new_expr = recursive_apply(self.expr)
        return LinearCombination(str(new_expr))