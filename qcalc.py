# Quantum Calculator
# The Quantum Calculator is a Maple program that can carry out computations in the small quantum cohomology ring of any Grassmannian of classical type. More precisely, it covers ordinary Grassmannians (type A) and Grassmannians of isotropic subspaces in a symplectic vector space (type C) or in an orthogonal vector space (type B or D). This software was written as part of a joint project with Andrew Kresch and Harry Tamvakis, aimed at studying the small quantum cohomology rings of submaximal isotropic and orthogonal Grassmannians. The Quantum Calculator is open source software (under the GNU General Public License).

# To use the Quantum Calculator, download the file qcalc, place it in the current directory, and issue the Maple commands "read qcalc;" and "with(qcalc);". This makes several functions available. A detailed description can be found in the User Manual. The following example gives an impression of the capabilities:

# % maple
#     |\^/|     Maple 10 (IBM INTEL LINUX)
# ._|\|   |/|_. Copyright (c) Maplesoft, a division of Waterloo Maple Inc. 2005
#  \  MAPLE  /  All rights reserved. Maple is a trademark of
#  <____ ____>  Waterloo Maple Inc.
#       |       Type ? for help.
# > read qcalc:
# > with(qcalc):
# > Gr(3,7):
# > qtoS(S[2,1]^3);
#      4 S[4, 4, 1] + 8 S[4, 3, 2] + 2 S[3, 3, 3] + 5 q S[2] + 4 q S[1, 1]
# I will be grateful for any comments or bug reports regarding this package. Thanks to Weihong Xu for one such report. Enjoy!

import numpy as np
import sympy as sp
from collections import OrderedDict
from typing import *
from util import *

# qcalc := module()
# option package;

# export
#   set_type, get_type, Gr, IG, OG, type_string,
#   schub_classes, generators, point_class, all_kstrict,
#   pieri, act, giambelli, mult, toS,
#   qpieri, qact, qgiambelli, qmult, qtoS,
#   dualize, type_swap, miami_swap, schub_type,
#   part2pair, pair2part, part2index, index2part, apply_lc;

# local _k, _n, _type, _pieri, _qpieri, fail_no_type, _dcoef,
#   spec2num, num2spec, giambelli_rec_inner, giambelli_rec, act_lc,
#   pieri_set, count_comps, _pieri_fillA, _pieri_itrA,
#   _pieri_fill, _pieri_itr, _part_star,
#   _part_tilde, part2pair_inner, pair2part_inner,
#   type_swap_inner, miami_swap_inner, dualize_index_inner,
#   part2indexA_inner, part2indexC_inner, part2indexB_inner, part2indexD_inner,
#   index2partA_inner, index2partC_inner, index2partB_inner, index2partD_inner,
#   part_len, part_clip, part_conj, part_itr, part_itr_between,
#   _first_kstrict, _itr_kstrict,
#   pieriA_inner, pieriC_inner, pieriB_inner, pieriD_inner,
#   qpieriA_inner, qpieriC_inner, qpieriB_inner, qpieriD_inner;



# ##################################################################
# # Miscellaneous conversions
# ##################################################################

def _custom_sort_key(item: str):
    # Extract the numbers from the string representation
    item = item.replace(' ', '')
    numbers = [int(n) for n in item[2:-1].split(',') if n]
    return (len(numbers), numbers)

def _sort_s_list(s_list):
    # Sort the list using the custom sort key
    return sorted(s_list, key=_custom_sort_key)

def _unique(arr):
    return list(OrderedDict.fromkeys(arr).keys())


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


# ##################################################################
# # Miscellaneous conversions
# ##################################################################

def part2pair_inner(lam: List[int], k: int) -> Tuple[List[int], List[int]]:
    top = part_conj([min(lam_i, k) for lam_i in lam])
    bot = part_clip([max(lam_i - k, 0) for lam_i in lam])

    # Adjust lengths
    top.extend([0] * (k - len(top)))
    
    if len(lam) > 0 and lam[-1] == 0:
        bot.append(0)

    return S(top,bot)


def pair2part_inner(pair: Tuple[List[int], List[int]]) -> List[int]:
    p1, p2 = pair  # unpacking the pair
    
    if p1 is None or len(p1)==0:  # if the first element of the pair is empty
        return S(*p2)
    
    lam = part_conj(p1)
    np2 = len(p2)
    
    # Constructing the resultant list
    a = [lam[i] + p2[i] for i in range(np2)]
    a.extend(lam[np2:])
    
    if np2 > 0 and p2[-1] == 0:
        a.append(0)

    return S(*a)


def miami_swap_inner(lam: List[int], k: int) -> str:
    # Check if k is not a member of lam
    if k not in lam:
        return S(*lam)
    
    # Check if the number of elements in lam greater than k is even
    count = sum(1 for lam_i in lam if lam_i > k)
    if count % 2 == 0:
        return S(*lam)
    
    # Check if the last element of lam is 0
    if lam[-1] == 0:
        return S(*lam[:-1])
    else:
        a = lam.copy()+[0]
        return S(*a)


def type_swap_inner(lam: List[int], k: int) -> List[Union[int, str]]:
    if lam is None or len(lam) == 0:
        return S(*[])
    if k not in lam:
        if lam[-1] == 0:
            return S(*lam[:-1])
        return S(*lam)
    if lam[-1] == 0:
        return S(*lam[:-1])
    a = lam + [0]
    return S(*a)


def part2indexA_inner(lam: List[int], k: int, n: int) -> List[int]:
    la = lam + [0] * (n - k)
    a = [k + j - la[j] + 1 for j in range(n - k)]
    return S(*a)


def _count_inner(la: List[int], k: int, j:int, delta:int=0) -> int:
    count = 0
    for i in range(j):
        if la[i] + la[j] <= 2 * k + delta + j - i:
            count += 1
    return count

def part2indexB_inner(lam: List[int], k: int, n: int) -> List[int]:
    la = lam + [0] * (n - k)
    res = []
    for j in range(n - k):
        if la[j] > k:
            res.append(n + k + 1 - la[j])
            continue
        count = _count_inner(la, k, j)
        a = n + k + 2 - la[j] + count
        res.append(a)
    return S(*res)


def part2indexC_inner(lam: List[int], k: int, n: int) -> List[int]:
    la = lam + [0] * (n-k)
    res = []
    for j in range(n - k):
        count = _count_inner(la, k, j)
        res.append(n + k + 1 - la[j] + count)
    return S(*res)


def part2indexD_inner(lam: List[int], k: int, n: int) -> List[int]:
    la = lam + [0] * (n+1-k)
    nt = n + 2 if (len(lam) > 0 and lam[-1] == 0) else n + 1
    res = []
    for j in range(n + 1 - k):
        count = _count_inner(la, k, j, -1)
        value = n + k - la[j] + count
        if la[j] > k:
            value += 1
            res.append(value)
            continue
        if la[j] == k and (j == 0 or k < la[j-1]) and (nt + j) % 2 == 0:
            value += 1
            res.append(value)
            continue
        value += 2
        res.append(value)
    return S(*res)


def index2partA_inner(idx: List[int], k: int, n: int) -> List[int]:
    la = []
    for j in range(n - k):
        la.append(k + j - idx[j])
    return S(*part_clip(la))

def index2partC_inner(idx: List[int], k: int, n: int) -> List[int]:
    la = []
    for j in range(n - k):
        count = 0
        for i in range(j):
            if idx[i] + idx[j] > 2 * n + 1:
                count += 1
        la.append(n + k + 1 - idx[j] + count)
    return ['S'] + part_clip(la)


def index2partB_inner(idx: List[int], k: int, n: int) -> List[Union[str, int]]:
    la = []
    for j in range(1, n - k + 1):
        count = 0
        if idx[j - 1] <= n:
            la.append(n + k + 1 - idx[j - 1])
        else:
            for i in range(1, j):
                if idx[i - 1] + idx[j - 1] > 2 * n + 2:
                    count += 1
            la.append(n + k + 2 - idx[j - 1] + count)
    return ['S'] + part_clip(la)


def index2partD_inner(idx: List[int], k: int, n: int) -> List[Union[str, int]]:
    la = []
    for j in range(1, n + 2 - k):
        count = 0
        if idx[j - 1] <= n + 1:
            la.append(n + k + 1 - idx[j - 1])
        else:
            for i in range(1, j):
                if idx[i - 1] + idx[j - 1] > 2 * n + 3:
                    count += 1
            la.append(n + k + 2 - idx[j - 1] + count)
    
    la = part_clip(la)
    
    if k not in la:
        return ['S'] + la

    missing_indices = set(range(1, n + 2)) - set(idx)
    if len(missing_indices) % 2 == 1:
        la.append(0)
    return ['S'] + la


def dualize_index_inner(idx: List[int], N: int, tp: str) -> List[Union[str, int]]:
    res = ['S']
    for i in reversed(idx):
        res.append(N + 1 - i)
    if tp == "D" and (N // 2) % 2 == 1:
        for i in range(len(res)):
            if res[i] == N // 2:
                res[i] = N // 2 + 1
            elif res[i] == N // 2 + 1:
                res[i] = N // 2
    return res


# ##################################################################
# # Pieri rule internals
# ##################################################################

def _pieri_fillA(lam: List[int], inner: List[int], outer: List[int], row_index: int, p: int) -> Optional[List[int]]:    
    if not lam or len(lam) == 0:
        return None
    
    res = lam.copy()
    pp = p
    rr = row_index
    
    if rr == 0:
        x = min(outer[0], inner[0] + pp)
        res[0] = x
        pp = pp - x + inner[0]
        rr = 1

    while rr < len(lam):
        x = min(outer[rr], inner[rr] + pp, res[rr-1])
        res[rr] = x
        pp = pp - x + inner[rr]
        rr += 1

    if pp > 0:
        return None

    return res[:len(lam)]


def _pieri_itrA(lam: List[int], inner: List[int], outer: List[int]) -> Optional[List[int]]:
    if not lam or len(lam) == 0:
        return None
    
    p = lam[-1] - inner[-1]
    for r in range(len(lam) - 2, -1, -1):
        if lam[r] > inner[r]:
            lam1 = lam.copy()
            lam1[r] = lam[r] - 1
            lam1 = _pieri_fillA(lam1, inner, outer, r+1, p+1)
            if lam1 is not None:
                return lam1
            p = p + lam[r] - inner[r]
    return None


def count_comps(lam1: List[int], lam2: List[int], skipfirst: bool, k: int, d: int) -> int:
    top1 = part_conj([min(item, k) for item in lam1])
    top1.extend([0] * (k - len(top1)))
    bot1 = part_clip([max(0, item - k) for item in lam1])
    bot1.append(0)

    top2 = part_conj([min(item, k) for item in lam2])
    top2.extend([0] * (k - len(top2)))
    bot2 = part_clip([max(0, item - k) for item in lam2])

    lb2 = len(bot2)
    if lb2 == 0:
        return 0

    comps = [0] * bot2[0]
    for i in range(lb2):
        for j in range(bot1[i], bot2[i]):
            comps[j] = 1

    b = 1
    for i in range(k):
        if top2[i] <= top1[i]:
            while b < lb2 and bot1[b] + b - 1 > top1[i] + k - i - d:
                b += 1
            minj = top2[i] + k - i - b + 2 - d
            maxj = min(top1[i] + k - i - b + 2 - d, bot2[0])
            for j in range(minj, maxj + 1):
                comps[j] = -1

    res = 0
    incomp = skipfirst
    for j in range(bot2[0]):
        if comps[j] == 1 and not incomp:
            res += 1
        incomp = comps[j] == 1

    return res

def pieri_set(p, lam, k, n, d):
    rows = n + d - k
    cols = n + k

    top = part_conj([min(item, k) for item in lam])
    top += [0] * (k - len(top))
    topk = cols if k == 0 else top[k - 1]  # Python lists are 0-indexed
    bot = part_clip([max(0, item - k) for item in lam]) + [0]
    lbot = len(bot) - 1

    # Find bounds for new top partition
    outer = [min(rows, top[j]) for j in range(k)]
    inner = []
    if k != 0:
        inner = [max(lbot, top[j + 1]) for j in range(len(top) - 1)] + [lbot]
    
    b = 1
    for i in range(1, k + 1):
        while b <= lbot and bot[b - 1] + b - 1 > top[i - 1] + k - i - d:
            b += 1
        if top[i - 1] + k - i + 2 - b - d <= 0:
            inner[i - 1] = max(top[i - 1], inner[i - 1])
        else:
            inner[i - 1] = max(bot[b - 1] + b - 1 + i - k + d, inner[i - 1])


    # Iterate through all possible top partitions
    res = set()
    top_1 = outer.copy()

    while isinstance(top_1, list):
        top1 = top_1
        top_1 = part_itr_between(top1, inner, outer)
        p1 = p + sum(top) - sum(top1)
        if p1 < 0:
            continue

        # Obvious bounds for bottom partition
        top1k = rows if k == 0 else top1[k-1]
        inbot = bot[:lbot] + [0] if lbot < top1k else bot[:lbot]
        if lbot == 0:
            outbot = [cols - k] if top1k > 0 else []
        else:
            outbot = [cols - k] + bot[:lbot-1] + ([bot[lbot-1]] if lbot < top1k else [])

        # Find exact bounds for bottom partition, using shift-under conditions
        b = 1
        for i in range(1, k+1):
            while b <= lbot and bot[b-1] + b - 1 > top[i-1] + k - i - d:
                b += 1
            if top1[i-1] < top[i-1]:
                if b > len(inbot):
                    inbot = False
                    break
                inbot[b-1] = max(inbot[b-1], top[i-1] + k - i - b + 2 - d)

            b1 = b
            while b1 < len(outbot) and bot[b1-1] + b1 - 1 <= top[i-1] + k - i - d:
                outbot[b1] = min(outbot[b1], top1[i-1] + k - i - b1 - d)
                b1 += 1

        if inbot == False:
            continue

        j = sum(bot)
        if sum(outbot) - j < p1:
            continue
        p1 = p1 - sum(inbot) + j
        if p1 < 0:
            continue

        bot1 = _pieri_fill(inbot, inbot, outbot, 1, p1)
        top1c = part_conj(top1)
        while isinstance(bot1, list):
            if k == 0:
                res.add(tuple(part_clip(bot1)))
            else:
                j = min(len(top1c), len(bot1))
                res.add(tuple(top1c[i] + bot1[i] for i in range(j)) + tuple(top1c[j:]))
            bot1 = _pieri_itr(bot1, inbot, outbot)

    return res


def _pieri_fill(lam: List[int], inner: List[int], outer: List[int], r: int, p: int) -> Union[List[int], None]:
    if not lam:
        return lam
    
    res = lam.copy()
    pp = p
    rr = r
    
    if rr == 1:
        x = min(outer[0], inner[0] + pp)
        res[0] = x
        pp = pp - x + inner[0]
        rr = 2

    while rr <= len(lam):
        x = min(outer[rr-1], inner[rr-1] + pp, res[rr-2] - 1)
        res[rr-1] = x
        pp = pp - x + inner[rr-1]
        rr += 1

    if pp > 0:
        return None

    return res


def _pieri_itr(lam: List[int], inner: List[int], outer: List[int]) -> Union[List[int], None]:
    if not lam:
        return None
    
    p = lam[-1] - inner[-1]
    
    for r in range(len(lam) - 1, 0, -1):
        if lam[r-1] > inner[r-1]:
            lam1 = lam.copy()
            lam1[r-1] -= 1
            lam1 = _pieri_fill(lam1, inner, outer, r + 1, p + 1)
            if lam1 is not None:
                return lam1
            p = p + lam[r-1] - inner[r-1]
    
    return None


def _part_star(lam: List[int], cols: int) -> Union[int, List[int]]:
    if not lam or lam[0] != cols:
        return 0
    return ['S'] + lam[1:]

def _part_tilde(lam: List[int], rows: int, cols: int) -> Union[int, List[Union[str, int]]]:
    if part_len(lam) != rows or (lam and lam[0] > cols):
        return 0
    
    r = rows + lam[0] - cols if lam else -cols
    
    if r <= 0:
        return 0
    if r < rows and len(lam) > r and lam[r] > 1:
        return 0

    result = ['S'] + lam[1:r]
    if lam and lam[-1] == 0:
        result.append(0)
    return result


# ##################################################################
# # General cohomology calculations, depending on Pieri rule.
# ##################################################################

def spec2num(sc: List[Union[str, int]]) -> int:
    if not isinstance(sc, list) or sc[0] != 'S' or len(sc) == 0:
        raise ValueError("special schubert class expected")

    if len(sc) > 1 and (_type != "D" or sc[1] != 0):
        raise ValueError("single part expected")

    return -sc[0] if len(sc) > 1 else sc[0]


def num2spec(p: int) -> List[Union[int, str]]:
    return [p] if p > 0 else [-p, 0]


def apply_lc(f: Callable, lc: Union[int, List[Union[str, int]]]) -> Union[int, List[Union[str, int]]]:
    # if lc is an integer coefficient
    if isinstance(lc, int):
        return lc
    elif lc and isinstance(lc, list) and lc[0] == 'S':  # if lc is a Schubert class
        return f(lc[1:])
    else:  # if lc is a linear combination
        return [apply_lc(f, item) for item in lc]


q = sp.symbols('q')

def act_lc(expc, lc, pieri: Callable) -> sp.Expr:
    # Use sympy's function to get the free symbols (variables) in the expression
    vars = expc.free_symbols - {q}
    
    # If there are no variables, multiply expc by lc and return
    if len(vars) == 0:
        return expc * lc

    v = list(vars)[0]
    
    # Assuming spec2num is a previously defined function
    i = spec2num(v)

    expc0 = expc.subs(v, 0)  # Replaces v with 0 in expc
    expc1 = sp.expand((expc - expc0) / v)

    # Assuming apply_lc is a previously defined function
    return apply_lc(lambda p: pieri(i, p), act_lc(expc1, lc, pieri)) + act_lc(expc0, lc, pieri)


def giambelli_rec_inner(lam: List[int], pieri: Callable, k: int) -> sp.Expr:
    # Use memoization with a cache
    cache = {}
    
    # Convert to tuple for using as dictionary key (since lists are not hashable)
    key = (tuple(lam), k)
    if key in cache:
        return cache[key]

    if not lam:
        return 1

    p = lam[0]
    if p == k and lam[-1] == 0:
        p = -k

    # Using list slicing for the equivalent of Maple's `op` function
    if lam[-1] == 0 and lam[1] < k:
        lam0 = lam[1:-2]
    else:
        lam0 = lam[1:-1]

    # Assuming pieri and S are previously defined functions or expressions
    stuff = pieri(p, lam0) - S(*lam)  # *lam unpacks the list

    # Assuming num2spec is a previously defined function
    result = sp.expand(num2spec(p) * giambelli_rec_inner(lam0, pieri, k) -
                       giambelli_rec(stuff, pieri, k))

    # Store result in cache before returning
    cache[key] = result
    return result

def giambelli_rec(lc: sp.Expr, pieri: Callable, k: int) -> sp.Expr:
    # Assuming apply_lc is a previously defined function
    return apply_lc(lambda x: giambelli_rec_inner(x, pieri, k), lc)




# ##################################################################
# # Type A: Quantum cohomology of Gr(n-k,n).
# ##################################################################

# DO NOT MODIFY THIS FUNCTION
def pieriA_inner(i: int, lam: List[int], k: int, n: int) -> sp.Expr:
    inner = padding_right(lam, 0, n-k-len(lam))
    outer = [k] + inner[:-1]
    mu = _pieri_fillA(inner, inner, outer, 1, i)
    res = 0
    while isinstance(mu, list):
        res += S(*part_clip(mu))
        mu = _pieri_itrA(mu, inner, outer)
    return res


def qpieriA_inner(i: int, lam: List[int], k: int, n: int) -> sp.Expr:
    res = pieriA_inner(i, lam, k, n)
    if len(lam) == n - k and lam[n - k] > 0:
        if k == 1:
            return q * S()
        lab = [(lam[j] - 1) if lam[j] > 1 else None for j in range(len(lam))]
        res += q * sp.expand(apply_lc(lambda x: _part_star(x, k - 1), pieriA_inner(i - 1, lab, k - 1, n)))
    return res


# ##################################################################
# # Type B: Quantum cohomology of odd orthogonal OG(n-k,2n+1).
# ##################################################################

def pieriB_inner(p: int, lam: List[int], k: int, n: int) -> sp.Expr:
    result = sp.Integer(0)
    b = 0 if p <= k else 1
    for mu in pieri_set(p, lam, k, n, 0):
        result += 2**(count_comps(lam, mu, False, k, 0) - b) * S(*mu)
    return result

def qpieriB_inner(p: int, lam: List[int], k: int, n: int) -> sp.Expr:
    res = pieriB_inner(p, lam, k, n)
    
    if k == 0:
        if len(lam) > 0 and lam[0] == n + k:
            res += q * apply_lc(lambda x: _part_star(x, n+k), pieriB_inner(p, lam[1:], k, n))
    else:
        if len(lam) == n - k and lam[n - k] > 0:
            res += q * apply_lc(lambda x: _part_tilde(x, n - k + 1, n + k), pieriB_inner(p, lam, k, n + 1))
        if len(lam) > 0 and lam[0] == n + k:
            res += q**2 * apply_lc(lambda x: _part_star(x, n + k), pieriB_inner(p, lam[1:], k, n))
    
    return sp.expand(res)

# ##################################################################
# # Type C: Quantum cohomology of symplectic IG(n-k,2n).
# ##################################################################

def pieriC_inner(i: int, lam: List[int], k: int, n: int) -> sp.Expr:
    result = sp.Integer(0)
    for x in pieri_set(i, lam, k, n, 0):
        result += 2**count_comps(lam, x, True, k, 0) * S(*x)
    return result


def qpieriC_inner(i: int, lam: List[int], k: int, n: int) -> sp.Expr:
    inner_result = pieriC_inner(i, lam, k, n)
    second_term = q/2 * apply_lc(lambda x: _part_star(x, n+k+1), pieriC_inner(i, lam, k, n+1))
    return inner_result + second_term


# ##################################################################
# # Type D: Quantum cohomology of even orthogonal OG(n+1-k,2n+2).
# ##################################################################

def pieriD_inner(p: int, lam: List[int], k: int, n: int) -> sp.Expr:
    tlam = 0 if k not in lam else (2 if lam[-1] == 0 else 1)
    result = sp.Integer(0)
    for mu in pieri_set(abs(p), lam, k, n, 1):
        result += _dcoef(p, lam, mu, tlam, k, n)
    return result

def _dcoef(p: int, lam: List[int], mu: List[int], tlam: int, k: int, n: int) -> sp.Expr:
    cc = count_comps(lam, mu, False, k, 1) - (0 if abs(p) < k else 1)
    if cc >= 0:
        if k not in mu or tlam == 1:
            return 2**cc * S(*mu)
        elif tlam == 2:
            return 2**cc * S(*mu, 0)
        else:
            return 2**cc * (S(*mu) + S(*mu, 0))
    else:
        # Tie breaking
        h = k + tlam + (1 if p < 0 else 0)
        pmu = 0
        for i in range(len(mu) - 1, -1, -1):
            lami = lam[i] if i < len(lam) else 0
            if lami < min(mu[i], k):
                h = h - (min(mu[i], k) - max(pmu, lami))
            pmu = mu[i]
        h %= 2
        if tlam == 0 and k in mu:
            return S(*mu, 0 if h == 0 else 1)
        elif h == 0:
            return 0
        else:
            return S(*mu, 0 if (tlam == 2 and k in mu) else None)


def qpieriD_inner(p, lam, k, n):
    res = pieriD_inner(p, lam, k, n)

    if k == 0:
        if len(lam) > 0 and lam[0] == n + k:
            res += q * apply_lc(lambda x: _part_star(x, n + k),
                                 pieriD_inner(p, lam[1:], k, n))
    elif k == 1:
        if len(lam) >= n and lam[n-1] > 0:
            lb = [max(x - 1, 0) for x in lam]
            cprd = pieriD_inner(abs(p) - 1, lb, 0, n) if abs(p) > 1 else S(*lb)
            intn = set(range(1, n+1))
            cprd = apply_lc(lambda mu: S(*(list(intn - set(mu))[::-1])), cprd)
            res1 = 0
            if lam[-1] > 0 and p > 0:
                res1 += q1 * apply_lc(lambda mu: S(*[x+1 for x in mu] + [1]*(n-len(mu))), cprd)
            if lam[-1] == 0 or k not in lam and (p == -1 or p > 1):
                res1 += q2 * apply_lc(lambda mu: S(*[x+1 for x in mu] + [1]*(n-len(mu)), 0), cprd)
            res += dualize(res1)
        if len(lam) > 0 and lam[0] == n + k:
            res += q1 * q2 * apply_lc(lambda x: _part_star(x, n + k), pieriD_inner(p, lam[1:], k, n))
    else:
        if len(lam) >= n + 1 - k and lam[n + 1 - k - 1] > 0:
            res += q * type_swap(apply_lc(lambda x: _part_tilde(x, n - k + 2, n + k),
                                          pieriD_inner(p, lam, k, n + 1)), k)
        if len(lam) > 0 and lam[0] == n + k:
            res += q**2 * apply_lc(lambda x: _part_star(x, n + k), pieriD_inner(p, lam[1:], k, n))
    
    return sp.expand(res)



# ##################################################################
# # Common interface for all types
# ##################################################################

def fail_no_type() -> None:
    raise ValueError("Must set type with IG or OG or set_type functions.")

# Using Python's None instead of Maple's false to represent unset values
_type = None
_k = None
_n = None
_pieri = fail_no_type
_qpieri = fail_no_type

# Grassmaniann Gr(l,N):
#           => k = N-l
# Trong cong thuc, nguoi ta thuong dung Gr(l,N) 
# trong cac giai thuat duoi day, ngta xai k=N-l
def set_type(tp: str, k: int, n: int) -> str:
    if not isinstance(tp, str):
        raise TypeError(f"tp must be a string, got {type(tp)}")
  
    if not isinstance(k, int): 
        raise TypeError(f"k must be an int, got {type(k)}")

    if not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n)}")

    # Additional checks
    if tp not in ['A', 'B', 'C', 'D']:
        fail_no_type()

    if k < 0 or n < k:
        raise ValueError("Need 0 <= k <= n.")
    
    global _pieri, _qpieri, _k, _n, _type
    
    if tp == "A":
        _pieri = pieriA_inner
        _qpieri = qpieriA_inner
    elif tp == "C":
        _pieri = pieriC_inner
        _qpieri = qpieriC_inner
    elif tp == "B":
        _pieri = pieriB_inner
        _qpieri = qpieriB_inner
    elif tp == "D":
        _pieri = pieriD_inner
        _qpieri = qpieriD_inner
    
    _k = k
    _n = n
    _type = tp
    
    return type_string()  # Assuming type_string() is a function returning a string


def type_string() -> str:
    td = get_type()
    return f"Type {td[0]} ;  (k,n) = ({td[1]},{td[2]}) ;  {td[3]}({td[4]},{td[5]}) ;  deg(q) = {td[6]}"


def get_type() -> list:
    global _type, _k, _n
    if _type == "A":
        return ["A", _k, _n, "Gr", _n-_k, _n, _n]
    elif _type == "C":
        return ["C", _k, _n, "IG", _n-_k, 2*_n, _n+1+_k]
    elif _type == "B":
        return ["B", _k, _n, "OG", _n-_k, 2*_n+1, 2*_n if _k == 0 else _n+_k]
    elif _type == "D":
        return ["D", _k, _n, "OG", _n+1-_k, 2*_n+2, 2*_n if _k == 0 else _n+_k]
    else:
        fail_no_type()


def Gr(m: int, N: int) -> None:   
    if not isinstance(m, int): 
        raise TypeError(f"m must be an int, got {type(m)}")

    if not isinstance(N, int):
        raise TypeError(f"N must be an int, got {type(N)}")
     
    set_type("A", N-m, N)


def IG(m: int, N: int) -> None:
    if not isinstance(m, int): 
        raise TypeError(f"m must be an int, got {type(m)}")

    if not isinstance(N, int):
        raise TypeError(f"N must be an int, got {type(N)}")
    
    if N % 2 == 1:
        raise ValueError("Second argument must be even.")
    set_type("C", N//2-m, N//2)


def OG(m: int, N: int) -> None:
    if not isinstance(m, int): 
        raise TypeError(f"m must be an int, got {type(m)}")

    if not isinstance(N, int):
        raise TypeError(f"N must be an int, got {type(N)}")
        
    if N % 2 == 1:
        set_type("B", (N-1) // 2 - m, (N-1) // 2)
    else:
        set_type("D", N // 2 - m, N // 2 - 1)


def S(*args: int) -> str:
    mu = ','.join(map(str, args))
    return f"S[{mu}]".replace(' ', '')


def schub_classes() -> List[str]:
    if not isinstance(_type, str):
        fail_no_type()

    if _type == "A":
        mu = [_k] * (_n - _k)
        partitions = part_gen(mu)

        res = [S(*lam) for lam in partitions]
        res = _unique(res)
        return _sort_s_list(res)

    if _type == "D":
        res = []
        for mu in all_kstrict(_k, _n + 1 - _k, _n + _k):
            if _k in mu:
                res.append(S(*mu))
                res.append(S(*mu, 0))
            else:
                res.append(S(*mu))
        res = _unique(res)
        return _sort_s_list(res)

    res = [S(*lam) for lam in all_kstrict(_k, _n - _k, _n + _k)]
    res = _unique(res)
    return _sort_s_list(res)


def generators() -> List[str]:
    if not isinstance(_type, str):
        fail_no_type()

    if _type != "D" and _k == _n:
        return []

    gen_list = [S(i) for i in range(1, _k + 1)]

    if _type == "D" and _k > 0:
        gen_list.append(S(_k, 0))

    if _type != "A":
        gen_list.extend([S(i) for i in range(_k + 1, _n + _k + 1)])

    return gen_list

def point_class() -> str:
    if not isinstance(_type, str):
        fail_no_type()

    if _type == "A":
        if _k > 0:
            return S(*(([_k] * (_n - _k))))
        return []

    delta = 1
    if _type == "D" and _k > 0:
        delta = 0

    result = []
    for i in range(0, _n - _k - delta + 1):
        result.append(_n + _k - i)
    
    return S(*result)


def part2pair(lc: Any) -> Any:
    if _type == "A":
        raise Exception("Only types B,C,D.")
    
    if isinstance(lc, list):
        return part2pair_inner(lc)
    else:
        return apply_lc(lambda lam: part2pair_inner(lam, _k), lc)


def pair2part(lc: Any) -> Any:
    if _type == "A":
        raise Exception("Only types B,C,D.")
    
    if isinstance(lc, list) and len(lc) == 2:
        return pair2part_inner(lc)
    else:
        return apply_lc(pair2part_inner, lc)


def part2index(lc: Any) -> Any:
    if isinstance(lc, list):
        return part2index(S(*lc))
    
    if _type == "A":
        return apply_lc(lambda lam: part2indexA_inner(lam, _k, _n), lc)
    elif _type in ["C", "B", "D"]:
        inner_functions = {
            "C": part2indexC_inner,
            "B": part2indexB_inner,
            "D": part2indexD_inner
        }
        return apply_lc(lambda lam: inner_functions[_type](lam, _k, _n), lc)
    else:
        fail_no_type()


def index2part(lc: Any) -> Any:
    if isinstance(lc, list):
        return index2part(S(*lc))
    
    if _type == "A":
        return apply_lc(lambda idx: index2partA_inner(idx, _k, _n), lc)
    elif _type in ["C", "B", "D"]:
        inner_functions = {
            "C": index2partC_inner,
            "B": index2partB_inner,
            "D": index2partD_inner
        }
        return apply_lc(lambda idx: inner_functions[_type](idx, _k, _n), lc)
    else:
        fail_no_type()


def dualize(lc: Any) -> Any:
    N = {
        "A": _n,
        "C": 2*_n,
        "B": 2*_n+1,
        "D": 2*_n+2
    }.get(_type, _n)
    
    return index2part(apply_lc(lambda idx: dualize_index_inner(idx, N, _type), part2index(lc)))


def type_swap(lc: Any) -> Any:
    if isinstance(lc, list):
        return type_swap(S(*lc))
    
    if _type == "D":
        return apply_lc(lambda lam: type_swap_inner(lam, _k), lc)
    
    return lc

def miami_swap(lc: Any) -> Any:
    if isinstance(lc, list):
        return miami_swap(S(*lc))
    
    if _type == "D":
        return apply_lc(lambda lam: miami_swap_inner(lam, _k), lc)
    
    return lc


def schub_type(lam: Any) -> int:
    if not isinstance(_type, str):
        raise ValueError("No type defined.")
    
    if _type != "D" or not (isinstance(lam, list) or isinstance(lam, (sp.Indexed, sp.IndexedBase))):
        raise ValueError("No type defined.")
    
    if _k not in lam:
        return 0
    elif len(lam) == 0 or lam[-1] > 0:
        return 1
    else:
        return 2


def pieri(i: int, lc: Any) -> Any:
    if isinstance(lc, list):
        return _pieri(i, lc, _k, _n)
    else:
        return apply_lc(lambda p: _pieri(i, p, _k, _n), lc)


def act(expr: Any, lc: Any) -> Any:
    return act_lc(expr, lc, lambda i, p: _pieri(i, p, _k, _n))


def giambelli(lc: Any) -> Any:
    return giambelli_rec(lc, lambda i, p: _pieri(i, p, _k, _n), _k)


def mult(lc1: Any, lc2: Any) -> Any:
    return act(giambelli(lc1), lc2)


def toS(lc: Any) -> Any:
    return act(giambelli(lc), S())


def qpieri(i: int, lc: Any) -> Any:
    if isinstance(lc, list):
        return _qpieri(i, lc, _k, _n)
    else:
        return apply_lc(lambda p: _qpieri(i, p, _k, _n), lc)


def qact(expr: Any, lc: Any) -> Any:
    return act_lc(expr, lc, lambda i, p: _qpieri(i, p, _k, _n))


def qgiambelli(lc: Any) -> Any:
    return giambelli_rec(lc, lambda i, p: _qpieri(i, p, _k, _n), _k)


def qmult(lc1: Any, lc2: Any) -> Any:
    return qact(qgiambelli(lc1), lc2)


def qtoS(lc: Any) -> Any:
    return qact(qgiambelli(lc), S())

pieri_fillA = _pieri_fillA
pieri_itrA = _pieri_itrA
first_kstrict = _first_kstrict
itr_kstrict = _itr_kstrict