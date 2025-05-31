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
from typing import List, Optional, Tuple, Union, Any, Callable
from .utils.hash import hashable_lru_cache
from .utils.mix import padding_right
from .schur import Schur, isSchur, toSchur, unique_schur_list
from .lc import LinearCombination
from .utils.kstrict import part_clip, all_kstrict

# qcalc := module()
# option package;

# export
#   set_type, get_type, Gr, IG, OG, type_string,
#   schub_classes, generators, all_kstrict,
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

    return Schur([top,bot])


def pair2part_inner(pair: Tuple[List[int], List[int]]) -> List[int]:
    p1, p2 = pair  # unpacking the pair
    
    if p1 is None or len(p1)==0:  # if the first element of the pair is empty
        return Schur(p2)
    
    lam = part_conj(p1)
    np2 = len(p2)
    
    # Constructing the resultant list
    a = [lam[i] + p2[i] for i in range(np2)]
    a.extend(lam[np2:])
    
    if np2 > 0 and p2[-1] == 0:
        a.append(0)

    return Schur(a)


def miami_swap_inner(lam: List[int], k: int) -> str:
    # Check if k is not a member of lam
    if k not in lam:
        return Schur(lam)
    
    # Check if the number of elements in lam greater than k is even
    count = sum(1 for lam_i in lam if lam_i > k)
    if count % 2 == 0:
        return Schur(lam)
    
    # Check if the last element of lam is 0
    if lam[-1] == 0:
        return Schur(lam[:-1])
    else:
        a = lam.copy()+[0]
        return Schur(a)


def type_swap_inner(lam: List[int], k: int) -> List[Union[int, str]]:
    if lam is None or len(lam) == 0:
        return Schur([])
    if k not in lam:
        if lam[-1] == 0:
            return Schur(lam[:-1])
        return Schur(lam)
    if lam[-1] == 0:
        return Schur(lam[:-1])
    a = lam + [0]
    return Schur(a)


def part2indexA_inner(lam: List[int], k: int, n: int) -> List[int]:
    la = lam + [0] * (n - k)
    a = [k + j - la[j] + 1 for j in range(n - k)]
    return Schur(a)


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
    return Schur(res)


def part2indexC_inner(lam: List[int], k: int, n: int) -> List[int]:
    la = lam + [0] * (n-k)
    res = []
    for j in range(n - k):
        count = _count_inner(la, k, j)
        res.append(n + k + 1 - la[j] + count)
    return Schur(res)


def part2indexD_inner(lam: List[int], k: int, n: int) -> List[int]:
    la = lam + [0] * (n+1-k)
    nt = n + 2 if (len(lam) > 0 and lam[-1] == 0) else n + 1
    res = []
    for j in range(n + 1 - k):
        count = _count_inner(la, k, j, -1)
        value = n+k-la[j] + count
        if la[j] > k:
            value += 1
            res.append(value)
            continue
        if la[j] == k and (j==0 or k<la[j-1]) and (nt + j) % 2 == 1:
            value += 1
            res.append(value)
            continue
        value += 2
        res.append(value)
    return Schur(res)


def index2partA_inner(idx: List[int], k: int, n: int) -> List[int]:
    la = []
    for j in range(n - k):
        la.append(k + j+1 - idx[j])
    return Schur(part_clip(la))


def index2partC_inner(idx: List[int], k: int, n: int) -> List[int]:
    la = []
    for j in range(n - k):
        count = 0
        for i in range(j):
            if idx[i] + idx[j] > 2*n+1:
                count += 1
        la.append(n+k+1 - idx[j] + count)
    return Schur(part_clip(la))


def index2partB_inner(idx: List[int], k: int, n: int) -> List[Union[str, int]]:
    la = []
    for j in range(0, n-k):
        count = 0
        if idx[j] <= n:
            la.append(n+k+1 - idx[j])
            continue

        for i in range(j):
            if idx[i] + idx[j] > 2*n + 2:
                count += 1
        la.append(n+k+2 - idx[j] + count)
    return Schur(part_clip(la))


def index2partD_inner(idx: List[int], k: int, n: int) -> List[Union[str, int]]:
    la = []
    for j in range(n+1-k):
        count = 0
        if idx[j] <= n + 1:
            la.append(n + k + 1 - idx[j])
            continue
        for i in range(j):
            if idx[i] + idx[j] > 2*n + 3:
                count += 1
        la.append(n + k + 2 - idx[j] + count)
    
    la = part_clip(la)
    
    if k not in la:
        return Schur(la)

    missing_indices = set(range(1, n+2)) - set(idx)
    if len(missing_indices) % 2 == 1:
        la.append(0)
    return Schur(la)


def dualize_index_inner(idx: List[int], N: int, tp: str) -> List[Union[str, int]]:
    res = []
    for item in reversed(idx):
        res.append(N + 1 - item)

    if tp == "D" and (N / 2) % 2 == 1:
        for i in range(len(res)):
            if res[i] == N/2:
                res[i] = N/2 + 1
                continue
            if res[i] == N/2 + 1:
                res[i] = N/2
    res = [int(x) if int(x)==x else x for x in res]

    return Schur(res)


# ##################################################################
# # Pieri rule internals
# ##################################################################

def _pieri_fillA(lam: List[int], inner: List[int], outer: List[int], row_index: int, p: int) -> Optional[List[int]]:    
    # print("-------------------------")
    # print("lam", lam)
    # print("inner", inner)
    # print("outer", outer)
    # print("row_index", row_index)
    # print("p", p)
    if not lam or len(lam) == 0:
        return lam
    
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


def calc_comps(
    top1: List[int], 
    bot1: List[int], 
    top2 : List[int], 
    bot2 : List[int],
    lb2: int, k : int, d : int):    
    comps = [0] * bot2[0]
    for i in range(lb2):
        for j in range(bot1[i], bot2[i]):
            comps[j] = 1

    b = 0
    for i in range(k):
        if top2[i] <= top1[i]:
            while b+1 < lb2 and bot1[b]+(b+1)-1 > top1[i]+k-(i+1)-d:
                b += 1
            minj = top2[i] + k - (i+1) - (b+1) + 2 - d
            maxj = min(top1[i] + k - (i+1) - (b+1) + 2 - d, bot2[0])
            
            # adjust for python index
            minj -= 1
            maxj -= 1
            # =======================
            for j in range(minj, maxj + 1):
                comps[j] = -1
    return comps

def count_ones(comps: List[int], skipfirst: bool, bot2_length: int) -> int:
    """Count occurrences of 1 in comps with skipfirst logic."""
    res = 0
    incomp = skipfirst
    for j in range(bot2_length):
        if comps[j] == 1 and not incomp:
            res += 1
        incomp = comps[j] == 1
    return res

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

    comps = calc_comps(top1, bot1, top2, bot2, lb2, k, d)

    return count_ones(comps, skipfirst, bot2[0])


def sort_part(tuples):
    return sorted(tuples, key=lambda lst: lst, reverse=True)

def pieri_set(p: int, lam: List[int], k: int, n: int, d:int):
    # print("p, lam, k, n, d: ")
    # print(p, lam, k, n, d)
    
    rows = n + d - k
    cols = n + k

    # Split up in PR partition pairs (to reuse old code).
    top = part_conj([min(item, k) for item in lam])
    top += [0] * (k - len(top))
    topk = cols if k == 0 else top[k - 1]  # Python lists are 0-indexed
    bot = part_clip([max(0, item - k) for item in lam]) + [0]
    lbot = len(bot) - 1

    # Find bounds for new top partition
    outer = [min(rows, top[j]+1) for j in range(k)]
    inner = []
    if k != 0:
        inner = [max(lbot, top[j + 1]) for j in range(len(top) - 1)] + [lbot]

    b = 0
    for i in range(k):
        while (b+1) <= lbot and bot[b]+(b+1)-1 > top[i]+k-(i+1)-d:
            b += 1
        if top[i] + k - (i+1) + 2 - (b+1) - d <= 0:
            inner[i] = max(top[i], inner[i])
        else:
            inner[i] = max(bot[b] + (b+1) - 1 + (i+1) - k + d, inner[i])


    # Iterate through all possible top partitions
    res = set()
    top_1 = outer.copy()
    
    while isinstance(top_1, list):
        top1 = top_1.copy()
        top_1 = part_itr_between(top1, inner, outer)
        p1 = p + sum(top) - sum(top1)
        if p1 < 0:
            continue

        # Obvious bounds for bottom partition
        top1k = rows if k == 0 else top1[k-1]
        inbot = bot[:lbot]
        outbot = []
        if lbot < top1k:
            inbot += [0]
        
        if lbot == 0:
            if top1k > 0:
                outbot = [cols - k] 
        else:
            _delta = []
            if lbot < top1k:
                _delta = [bot[lbot-1]]
            outbot = [cols-k] + bot[:lbot-1] + _delta
        
        # Find exact bounds for bottom partition, using shift-under conditions
        b = 0
        for i in range(k):
            while b+1 <= lbot and bot[b]+(b+1)-1 > top[i] + k - (i+1) - d:
                b += 1
            if top1[i] < top[i]:
                if b+1 > len(inbot):
                    inbot = False
                    break
                inbot[b] = max(inbot[b], top[i] + k - (i+1) - (b+1) + 2 - d)

            b1 = b
            while b1+1 < len(outbot) and bot[b1] + (b1+1) - 1 <= top[i] + k - (i+1) - d:
                outbot[b1+1] = min(outbot[b1+1], top1[i] + k - (i+1) - (b1+1) - d)
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
                value = [top1c[i] + bot1[i] for i in range(j)] + top1c[j:]
                res.add(tuple(value))
            bot1 = _pieri_itr(bot1, inbot, outbot)
        
    res = [list(item) for item in res]

    # print("pieri_set: ", res)
    return sort_part(res)


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


def _part_star(lam: List[int], cols: int) -> Union[int, Schur]:
    if not lam or len(lam)==0 or lam[0] != cols:
        return 0
    return Schur(lam[1:])

def _part_tilde(lam: List[int], rows: int, cols: int) -> Union[int, Schur]:
    if part_len(lam) != rows or (lam and len(lam)>0 and lam[0] > cols):
        return 0
    
    r = rows + lam[0] - cols
    if r <= 0:
        return 0
    if r < rows and len(lam) > r and lam[r] > 1:
        return 0

    res = lam[1:r]
    if lam and lam[-1] == 0:
        res.append(0)
    return Schur(res)


# ##################################################################
# # General cohomology calculations, depending on Pieri rule.
# ##################################################################

def spec2num(sc: Union[Schur, sp.Expr]) -> int:
    if isinstance(sc, sp.Expr):
        sc = toSchur(sc)
    if not isinstance(sc, Schur):
        raise ValueError("special schubert class expected")
    if len(sc.p) > 1 and (_type != "D" or sc.p[1] != 0):
        raise ValueError("single part expected")
    return -sc.p[0] if len(sc.p) > 1 else sc.p[0]


def num2spec(p: int) -> Schur:
    return Schur([p]) if p > 0 else Schur([-p, 0])


def apply_lc(f: Callable, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    lc = LinearCombination(lc)
    return lc.apply(f)

def act_lc(expc: sp.Expr, lc: Union[sp.Expr, LinearCombination, str], pieri: Callable) -> LinearCombination:
    # print("act_lc")
    lc = LinearCombination(lc)

    q = sp.Symbol('q')
    vars = expc.free_symbols - {q}
    vars = sorted(vars, key=lambda x: str(x))
    
    # If there are no variables, multiply expc by lc and return
    if len(vars) == 0:
        return LinearCombination(expc * lc)

    v = list(vars)[0]
    
    i = spec2num(v)

    expc0 = expc.subs(v, 0)  # Replaces v with 0 in expc
    expc1 = sp.expand((expc - expc0) / v)

    # print("expc:                          ", expc)
    # print("expc0:                         ", expc0)
    # print("expc1:                         ", expc1)
    # print("v:                             ", v)

    lc_p1 = act_lc(expc1, lc, pieri)
    lc_p2 = act_lc(expc0, lc, pieri)
    # print("lc_p1", lc_p1)
    # print("lc_p2", lc_p2)
    
    # Assuming apply_lc is a previously defined function
    res1 = apply_lc(lambda p: pieri(i, p), lc_p1)
    # print("act_lc res 111111: ", res1)
    res = LinearCombination(res1 + lc_p2)
    return res


@hashable_lru_cache(maxsize=None)
def giambelli_rec_inner(lam: List[int], pieri: Callable, k: int) -> LinearCombination:
    
    lam = list(lam)
    # print("----------------------giambelli_rec_inner\n", lam, k)
    # print("len(lam): ", len(lam))

    if not lam or len(lam) == 0:
        # print("return 1")
        return LinearCombination(1)

    p = lam[0]
    if p == k and lam[-1] == 0:
        p = -k

    # Using list slicing for the equivalent of Maple's `op` function
    lam0 = lam[1:]
    if lam[-1] == 0 and lam[1] < k:
        lam0 = lam[1:-1]

    # print("lam, lam0: ", lam, lam0)
    # print("pieri(p, lam0): ", pieri(p, lam0))
    stuff = pieri(p, lam0) - LinearCombination(Schur(lam).symbol())
    
    # Assuming num2spec is a previously defined function
    a = giambelli_rec_inner(lam0, pieri, k)
    b = giambelli_rec(stuff, pieri, k)
    # print("a: ", a)
    # print("b: ", b)

    res = sp.expand(num2spec(p) * a.expr - b.expr)
    return LinearCombination(res)

def giambelli_rec(lc: Union[sp.Expr, LinearCombination, str], pieri: Callable, k: int) -> LinearCombination:
    lc = LinearCombination(lc)
    # print("giambelli_rec lc: ", lc)
    return apply_lc(lambda x: giambelli_rec_inner(x, pieri, k), lc)




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





def part2pair(lc: Any) -> Any:
    if _type == "A":
        raise Exception("Only types B,C,D.")
    
    if isinstance(lc, list):
        return part2pair_inner(lc, _k)
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
        return part2index(Schur(lc))
    
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
        return index2part(Schur(lc))
    
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


def dualize(lc: Union[sp.Expr, LinearCombination, str]) -> Any:
    lc = LinearCombination(lc)
    N = {
        "A": _n,
        "C": 2*_n,
        "B": 2*_n+1,
        "D": 2*_n+2
    }.get(_type, _n)
    
    index = part2index(lc)
    # print("lc, index:", lc, index)

    return index2part(apply_lc(lambda idx: dualize_index_inner(idx, N, _type), index))


def type_swap(lc: Union[sp.Expr, LinearCombination, str, List[int]], k: int) -> LinearCombination:
    if isinstance(lc, list):
        return type_swap(Schur(lc).symbol())
    
    if _type == "D":
        return apply_lc(lambda lam: type_swap_inner(lam, _k), lc)
    
    return LinearCombination(lc)

def miami_swap(lc: Any) -> Any:
    if isinstance(lc, list):
        return miami_swap(Schur(lc))
    
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


def pieri(i: int, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    if isinstance(lc, list):
        return _pieri(i, lc, _k, _n)
    else:
        return apply_lc(lambda p: _pieri(i, p, _k, _n), lc)


def act(expr: Union[sp.Expr, LinearCombination, str], lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    expr = LinearCombination(expr).expr
    lc = LinearCombination(lc)
    return act_lc(expr, lc, lambda i, p: _pieri(i, p, _k, _n))


def giambelli(lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    lc = LinearCombination(lc)
    return giambelli_rec(lc, lambda i, p: _pieri(i, p, _k, _n), _k)


def mult(lc1: Union[sp.Expr, LinearCombination, str], lc2: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    lc1 = LinearCombination(lc1)
    lc2 = LinearCombination(lc2)
    return act(giambelli(lc1), lc2)


def toS(lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    lc = LinearCombination(lc)
    return act(giambelli(lc), Schur([]).symbol())


def qpieri(i: int, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    lc = LinearCombination(lc)
    if isSchur(lc.expr):
        lam = toSchur(lc.expr).p
        return _qpieri(i, lam, _k, _n)
    return apply_lc(lambda p: _qpieri(i, p, _k, _n), lc)


def qact(expr: Union[sp.Expr, LinearCombination, str], lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    # print("qact")
    expr = LinearCombination(expr).expr
    lc = LinearCombination(lc)
    # print("expr: ", expr)
    # print("lc: ", lc)
    return act_lc(expr, lc, lambda i, p: _qpieri(i, p, _k, _n))


def qgiambelli(lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    # print("qgiambelli")
    lc = LinearCombination(lc)
    # print("lc: ", lc)
    return giambelli_rec(lc, lambda i, p: _qpieri(i, p, _k, _n), _k)


def qtoS(lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
    # print("qtoS")
    lc = LinearCombination(lc)
    return qact(qgiambelli(lc).expr, LinearCombination(Schur([]).symbol()))

pieri_fillA = _pieri_fillA
pieri_itrA = _pieri_itrA
part_star = _part_star
part_tilde = _part_tilde