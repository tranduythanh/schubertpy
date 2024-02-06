from functools import total_ordering

from typing import *
import sympy as sp
import ast

ftable = {
    ',': 'j',
    '[': 'p',
    ']': 'q'
}

btable = {value: key for key, value in ftable.items()}


def toSchur(sym: sp.Symbol) -> 'Schur':
        # Convert symbol back to string and translate using reverse table
        parsed_str = str(sym).translate(btable).replace('S', '')
        # Parse the string back into a list structure
        pl = ast.literal_eval(parsed_str)
        if isinstance(pl, list) and all(isinstance(i, list) for i in pl):
            return Schur(pl)
        raise ValueError("Input string does not represent a list of lists")


def unique_schur_list(schur_list: List['Schur']):
    return  sorted(list(set(schur_list)))


class Schur(object):
    def __init__(self, p):
        # Set self.p to p or [] if p is None
        self.p = p if p is not None else []

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

    def symbol(self) -> sp.Symbol:
        # Return the sympified version of the string representation of the object
        return sp.sympify(self.__str__().translate(ftable))

    