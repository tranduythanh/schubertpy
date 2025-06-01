from abc import ABC, abstractmethod
from typing import Callable, List, Union, Any
from .schur import Schur
from .lc import LinearCombination
import sympy as sp
from .utils.hash import hashable_lru_cache_method

from .qcalc import (
    apply_lc,
    isSchur,
    toSchur,
)

class AbstractGrassmannian(ABC):
    _type: str
    _k: int
    _n: int
    _pieri: Callable
    _qpieri: Callable
    
    def __init__(self, m: int, n:int):
        self._type = ''
        self._k = 0
        self._n = 0
        self._pieri = lambda i, lam, k, n: LinearCombination([])
        self._qpieri = lambda i, lam, k, n: LinearCombination([])

    @abstractmethod
    def degree_q(self) -> int:
        pass
    
    @abstractmethod
    def schub_classes(self) -> List[Schur]:
        pass
    
    @abstractmethod
    def generators(self) -> List[Schur]:
        pass

    @abstractmethod
    def point_class(self) -> Schur:
        pass

    @abstractmethod
    def part2pair(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        pass
    

    @abstractmethod
    def pair2part(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        pass
        
    @abstractmethod
    def part2index(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        pass
        

    @abstractmethod
    def index2part(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        pass
        
    @abstractmethod
    def dualize(self, lc: Union[sp.Expr, LinearCombination, str]) -> Any:
        pass
    
    @abstractmethod
    def type_swap(self, lc: Union[sp.Expr, LinearCombination, str, List[int]], k: int) -> LinearCombination:
        pass

    @abstractmethod
    def schub_type(self, lam: Union[Schur, List[int]]) -> int:
        pass

    
    @staticmethod
    def static_miami_swap_inner(lam: List[int], k: int) -> LinearCombination:
        # Check if k is not a member of lam
        if k not in lam:
            return LinearCombination(Schur(lam))
        
        # Check if the number of elements in lam greater than k is even
        count = sum(1 for lam_i in lam if lam_i > k)
        if count % 2 == 0:
            return LinearCombination(Schur(lam))
        
        # Check if the last element of lam is 0
        if lam[-1] == 0:
            return LinearCombination(Schur(lam[:-1]))
        
        a = lam.copy()+[0]
        return LinearCombination(Schur(a))
    
    
    def miami_swap(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return self.miami_swap(LinearCombination(lc))
        if self._type == "D":
            return apply_lc(lambda lam: self.static_miami_swap_inner(lam, self._k), lc)
        return LinearCombination(lc)

    
    def clone(self):
        return self.__class__(self._n-self._k, self._n)
        

    def pieri(self, i: int, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        if isinstance(lc, list):
            return self._pieri(i, lc, self._k, self._n)
        else:
            return apply_lc(lambda p: self._pieri(i, p, self._k, self._n), lc)


    def act(self, expr: Union[sp.Expr, LinearCombination, str], lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        expr = LinearCombination(expr).expr
        lc = LinearCombination(lc)
        return self.act_lc(expr, lc, lambda i, p: self._pieri(i, p, self._k, self._n))


    def giambelli(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc = LinearCombination(lc)
        # print("ag:-giambelli: ", lc)
        return self.giambelli_rec(lc, lambda i, p: self._pieri(i, p, self._k, self._n), self._k)


    def mult(self, lc1: Union[sp.Expr, LinearCombination, str], lc2: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc1 = LinearCombination(lc1)
        lc2 = LinearCombination(lc2)
        return self.act(self.giambelli(lc1), lc2)


    def toS(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc = LinearCombination(lc)
        return self.act(self.giambelli(lc), Schur([]).symbol())


    def qpieri(self, i: int, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc = LinearCombination(lc)
        if isSchur(lc.expr):
            lam = toSchur(lc.expr).p
            return self._qpieri(i, lam, self._k, self._n)
        return apply_lc(lambda p: self._qpieri(i, p, self._k, self._n), lc)


    def qact(self, expr: Union[sp.Expr, LinearCombination, str], lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        # print("qact")
        expr = LinearCombination(expr).expr
        lc = LinearCombination(lc)
        # print("expr: ", expr)
        # print("lc: ", lc)
        return self.act_lc(expr, lc, lambda i, p: self._qpieri(i, p, self._k, self._n))


    def qgiambelli(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        # print("qgiambelli")
        lc = LinearCombination(lc)
        # print("lc: ", lc)
        return self.giambelli_rec(lc, lambda i, p: self._qpieri(i, p, self._k, self._n), self._k)


    def qmult(
        self, 
        lc1: Union[sp.Expr, LinearCombination, str, Schur, List[int]], 
        lc2: Union[sp.Expr, LinearCombination, str, Schur, List[int]],
    ) -> LinearCombination:
        lc1 = LinearCombination(lc1)
        lc2 = LinearCombination(lc2)
        # if lc1.has_part_zero_padding():
        #     raise ValueError("The 1st input param contains a partition with zero padding")
        # if lc2.has_part_zero_padding():
        #     raise ValueError("The 2nd input param contains a partition with zero padding")
        # print("qmult")
        # print("lc1: ", lc1)
        # print("lc2: ", lc2)
        return self.qact(self.qgiambelli(lc1), lc2)
    

    def qtoS(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        # print("qtoS")
        lc = LinearCombination(lc)
        return self.qact(self.qgiambelli(lc).expr, LinearCombination(Schur([]).symbol()))
    
    def spec2num(self, sc: Union[Schur, sp.Expr]) -> int:
        if isinstance(sc, sp.Expr):
            sc = toSchur(sc)
        if not isinstance(sc, Schur):
            raise ValueError("special schubert class expected")
        if len(sc.p) > 1 and (self._type != "D" or sc.p[1] != 0):
            raise ValueError("single part expected")
        return -sc.p[0] if len(sc.p) > 1 else sc.p[0]

    def act_lc(self, expc: sp.Expr, lc: Union[sp.Expr, LinearCombination, str], pieri: Callable) -> LinearCombination:
        # print("act_lc")
        lc = LinearCombination(lc)

        q = sp.Symbol('q')
        vars = expc.free_symbols - {q}
        vars = sorted(vars, key=lambda x: str(x))
        
        # If there are no variables, multiply expc by lc and return
        if len(vars) == 0:
            return LinearCombination(expc * lc)

        v = list(vars)[0]
        
        i = self.spec2num(v)

        expc0 = expc.subs(v, 0)  # Replaces v with 0 in expc
        expc1 = sp.expand((expc - expc0) / v)

        # print("expc:                          ", expc)
        # print("expc0:                         ", expc0)
        # print("expc1:                         ", expc1)
        # print("v:                             ", v)

        lc_p1 = self.act_lc(expc1, lc, pieri)
        lc_p2 = self.act_lc(expc0, lc, pieri)
        # print("lc_p1", lc_p1)
        # print("lc_p2", lc_p2)
        
        # Assuming apply_lc is a previously defined function
        res1 = apply_lc(lambda p: pieri(i, p), lc_p1)
        # print("act_lc res 111111: ", res1)
        res = LinearCombination(res1 + lc_p2)
        return res

    @hashable_lru_cache_method(maxsize=None)
    def giambelli_rec_inner(self, lam: List[int], pieri: Callable, k: int) -> LinearCombination:
        
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
        a = self.giambelli_rec_inner(lam0, pieri, k)
        b = self.giambelli_rec(stuff, pieri, k)
        # print("a: ", a)
        # print("b: ", b)

        res = sp.expand(self.num2spec(p) * a.expr - b.expr)
        return LinearCombination(res)

    def giambelli_rec(self, lc: Union[sp.Expr, LinearCombination, str], pieri: Callable, k: int) -> LinearCombination:
        lc = LinearCombination(lc)
        # print("giambelli_rec lc: ", lc)
        return apply_lc(lambda x: self.giambelli_rec_inner(x, pieri, k), lc)

    def num2spec(self, p: int) -> Schur:
        return Schur([p]) if p > 0 else Schur([-p, 0])