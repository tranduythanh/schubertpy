from functools import total_ordering
from typing import *
from .schur import *
from .const import *
import sympy as sp
import ast


class LinearCombination(object):
    def __init__(self, expr: Union[str, sp.Expr, int, 'LinearCombination']):
        if isinstance(expr, str):
            expr = expr.replace('^', '**')
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
    
    def is_valid(self) -> bool:
        """
        Check if the expression is a linear combination.
        This version considers an expression linear if it involves only:
        - Scalar multiplication (a number multiplied by an expression).
        - Addition or subtraction of linear terms.
        """
        def is_linear(expr):
            if isinstance(expr, sp.Number):
                # A number is linear by itself
                return True
            elif isinstance(expr, sp.Symbol):
                # A symbol is linear by itself
                return True
            elif isinstance(expr, sp.Add):
                # Check if all components of the addition are linear
                return all(is_linear(arg) for arg in expr.args)
            elif isinstance(expr, sp.Mul):
                # Check if the multiplication is only between a scalar and another expression
                number_count = sum(1 for arg in expr.args if isinstance(arg, sp.Number))
                if number_count == 1 and len(expr.args) == 2:
                    # One argument should be a number and the other should be linear
                    return all(is_linear(arg) for arg in expr.args if not isinstance(arg, sp.Number))
                return False
            elif isinstance(expr, sp.Pow):
                # Check if it is a power with exponent equal to 1 or -1 which is still linear
                if isinstance(expr.exp, sp.Number) and expr.exp == 1:
                    return is_linear(expr.base)
                return False
            return False  # Non-linear for other types of expressions
        
        # Start the recursion with the main expression
        return is_linear(self.expr)

    def _count_Schur(self, expr) -> int:
        if isinstance(expr, sp.Mul):
            return sum(1 for arg in expr.args if isSchur(arg))
        raise ValueError(f"Invalid type for counting Schur: {expr}")
    
    def _cutoff_Schur(self, expr) -> Tuple['LinearCombination', 'Schur']:
        if isinstance(expr, sp.Mul):
            new_expr = sp.Mul(*[arg for arg in expr.args if not isSchur(arg)])
            ss = [arg for arg in expr.args if isSchur(arg)]
            if len(ss) <=0:
                raise ValueError(f"Schur function absent or not in order 1: {expr}")
            s = ss[0]
            return (LinearCombination(new_expr), Schur(s).partition())
        raise ValueError(f"Invalid type for cutoff Schur: {expr}")
    

    def _schur_expansion(self, expr, include_q=True) -> 'LinearCombination':
        if isinstance(expr, sp.Number):
            return (int(expr),[])
        if isSchur(expr):
            return (1, toSchur(str(expr)).partition())
        if isinstance(expr, sp.Mul):
            if self._count_Schur(expr) > 1:
                raise ValueError(f"Cannot convert a product with multiple Schur functions to schur_expansion. Please expand the expression first: {self.expr}")
            return(self. _cutoff_Schur(expr))
            
        if isinstance(self.expr, sp.Add):
            # Handle the case where the expression is a sum of terms
            res = []
            for term in self.expr.args:
                if not include_q and str(term).__contains__('q'):
                    continue
                res.append(self._schur_expansion(term))
            sorted_array = sorted(res, key=lambda x: x[1])
            return sorted_array
        raise ValueError(f"Invalid type for schur_expansion: {self.expr}")

    def schur_expansion(self, include_q=True) -> 'LinearCombination':
        """
        Expand each term in the expression individually.
        This method assumes that the expression is a polynomial and expands each term separately.
        """
        return self._schur_expansion(self.expr, include_q)