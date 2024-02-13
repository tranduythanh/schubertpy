import numpy as np
import sympy as sp
from collections import OrderedDict
from typing import *
from .util import *
from .schur import *
from .lc import *

def _first_kstrict(k: int, rows: int, cols: int) -> List[int]:
    return [max(k, cols - i) for i in range(rows)]


def _itr_kstrict(lambda_: List[int], k: int) -> Optional[List[int]]:
    n = len(lambda_)
    clip_lambda = part_clip(lambda_)
    if clip_lambda is None:
        return None
    if len(clip_lambda) == 0:
        return []

    i = len(clip_lambda)

    li = lambda_[i-1] - 1
    
    if li <= k:
        return lambda_[:i-1] + [li] * (n - i + 1)
    elif li + i - n > k:
        return lambda_[:i-1] + [li - j for j in range(n - i + 1)]
    else:
        return lambda_[:i-1] + [li - j for j in range(li - k + 1)] + [k] * (n - i - li + k)


def part_clip(lambda_: List[int]) -> List[int]:
    '''
    trims or removes trailing zeros from the list lambda.
    '''
    i = len(lambda_) - 1
    while i >= 0 and lambda_[i] == 0:
        i -= 1
    return lambda_[:i+1] if i >= 0 else []

def all_kstrict(k: int, rows: int, cols: int) -> Set[Tuple[int, ...]]:
    res = []
    lam = _first_kstrict(k, rows, cols)
    
    while True: # Check if lam is a list
        clipped = part_clip(lam)
        if clipped:  # Check if clipped is not None
            res.append(clipped)
            lam = _itr_kstrict(lam, k)
            continue
        
        res.append([])
        break

    return res


def part_conj(lambda_: List[int]) -> List[int]:
    lambda_ = part_clip(lambda_)
    n = len(lambda_)
    if n == 0:
        return []

    if min(lambda_) < 0:
        return []
    
    m = lambda_[0]
    lam = lambda_.copy()
    res = [0] * m
    
    for i in range(0, m):
        res[i] = len(lam)
        lam = [lam[j] - 1 for j in range(len(lam))]
        lam = part_clip(lam)
    return res
    

def part_gen(lam: List[int]):
    if lam is None:
        return []
    if lam == []:
        return []
    
    mu = lam.copy()
    ret = []
    while mu is not None:
        pmu = part_clip(mu)

        if pmu is not None and len(mu) > 0:
            ret.append(pmu)
            mu = part_itr(mu)
            continue
        
        ret.append([])
        break
        
    return ret


def part_itr(mu: List[int]) -> Optional[List[int]]:
    if mu is None:
        return None
    if len(mu)==0:
        return None
    pmu = part_clip(mu)
    if pmu is None:
        return None
    if len(pmu) == 0:
        return None
    
    last_idx = part_len(mu)-1
    a = mu[last_idx] - 1
    return mu[:last_idx] + [a] * (len(mu) - last_idx)


# tau < mu < lambda
def part_itr_between(mu: List[int], tau: List[int], lam: List[int]) -> Optional[List[int]]:
    i = len(mu)-1
    while i>=0 and mu[i] == tau[i]:
        i -= 1
    if i < 0:
        return None
    return mu[:i] + [min(mu[i]-1, lam[j]) for j in range(i, len(mu))]


def part_len(lambda_: List[int]) -> int:
    cl = part_clip(lambda_)
    if cl is None:
        return 0
    return len(cl)

first_kstrict = _first_kstrict