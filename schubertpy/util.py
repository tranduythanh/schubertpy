from typing import *

import numpy as np
from sympy import symbols, Poly, Symbol

def padding_right(lam, value, count):
    return lam + [value]*count


def yd(partition):
    print('Young diagram for partition: ' + str(partition))
    for row in partition:
        print(('[]') * row)

def partition_to_ascii(partition: List[int]) -> List[str]:
    """
    Convert a partition to an ASCII art representation using `[]`.
    """
    max_row = max(partition) if partition else 0
    return ["[]"*row + "  " * (max_row - row) for row in partition]

def embed_str(s: str, height: int) -> List[str]:
    width = len(s)
    center = 0
    res = []
    for i in range(0, height):
        if i == center:
            res.append(s)
        else:
            res.append(" " * width)
    return res

def embed_partition(partition: List[int], width, height: int) -> List[str]:
    res = partition_to_ascii(partition)
    if width*2 > len(res[0]):
        for i, row in enumerate(res):
            res[i] = row + "  "*(width - int(len(row)/2))
    if height > len(res):
        res += ["  "*width]*(height - len(res))
    return res




def __N__(kappa, mu):
    n = len(kappa)
    if n == 0:
        return 0
    nu = kappa + 1
    M = np.array([np.prod(nu[(i+1):]) for i in range(n)])
    return np.sum(mu * M)

def __is_decreasing__(x):
    l = len(x)
    i = 0
    out = True
    while i < l-1 and out:
        out = x[i] >= x[i+1]
        i = i + 1
    return out


def __drop_trailing_zeros__(x):
    n = len(x) - 1
    while n >= 0 and x[n] == 0:
        x.pop()
        n = n - 1
    return x

def __make_partition__(x):
    mu = __drop_trailing_zeros__(x)
    integers = map(lambda i: isinstance(i, int), mu)
    if not all(integers):
        raise ValueError("invalid integer partition.")
    if not __is_decreasing__(list(mu) + [0]):
        raise ValueError("invalid integer partition.")
    return np.asarray(mu, dtype=int)

def SchurPol(n, kappa):
    """
    Schur polynomial of an integer partition.

    Parameters
    ----------
    n : int
        Positive integer, the number of variables of the polynomial.
    kappa : list of integers
        An integer partition given as a list of decreasing integers. Trailing 
        zeros are dropped.

    Returns
    -------
    Poly
        The Schur polynomial of `kappa` in `n` variables `x_1`, ..., `x_n`, 
        with integer coefficents.
    
    Examples
    --------

    """
    if not (isinstance(n, int) and n >= 1):
        raise ValueError("`n` must be a strictly positive integer.")
    kappa_ = __make_partition__(kappa)
    variables = [symbols(f'x_{i}') for i in range(1, n+1)]
    x = [Poly(v, *variables, domain='ZZ') for v in variables]
    def sch(S, m, k, nu):
        if len(nu) == 0 or nu[0] == 0 or m == 0:
            return Poly(1, *variables, domain='ZZ')
        if len(nu) > m and nu[m] > 0:
            return Poly(0, *variables, domain='ZZ')
        if m == 1:
            return x[0]**nu[0]
        N = __N__(kappa_, nu)
        s = S[N-1, m-1]
        if s is not None:
            return s
        s = sch(S.copy(), m-1, 1, nu)
        i = k
        while len(nu) >= i and nu[i-1] > 0:
            if len(nu) == i or nu[i-1] > nu[i]:
                _nu = nu.copy()
                _nu[i-1] = nu[i-1]-1
                if nu[i-1] > 1:
                    s = s + x[m-1] * sch(S.copy(), m, i, _nu)
                else:
                    s = s + x[m-1] * sch(S.copy(), m-1, 1, _nu)
            i = i + 1
        if k == 1:
            S[__N__(kappa_, nu)-1, m-1] = s
        return s
    S = np.full((__N__(kappa_,kappa_), n), None)
    return sch(S.copy(), n, 1, kappa_)