from abc import ABC, abstractmethod
from typing import *
from .qcalc import *
from .partition import Partition

class AbstractGrassmannian(ABC):
    _type: str
    _k: int
    _n: int
    _pieri: Callable
    _qpieri: Callable
    
    def __init__(self, m: int, n:int):
        self._type = None
        self._k = None
        self._n = None
        self._pieri = None
        self._qpieri = None

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
    def miami_swap(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        pass

    @abstractmethod
    def schub_type(self, lam: Union[Schur, List[int]]) -> int:
        pass

    
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
        return giambelli_rec(lc, lambda i, p: self._pieri(i, p, self._k, self._n), self._k)


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
        return giambelli_rec(lc, lambda i, p: self._qpieri(i, p, self._k, self._n), self._k)


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
    
    def qmult_rh(
        self, 
        lc1: Union[sp.Expr, LinearCombination, str, Schur, List[int]], 
        lc2: Union[sp.Expr, LinearCombination, str, Schur, List[int]],
    ) -> LinearCombination:
        _gr = self.clone()
        _delta = _gr._n-_gr._k
        _gr._n = _gr._n + _delta
        _gr._k = _gr._k + _delta

        res = _gr.mult(lc1, lc2)
        # print("qmult_rh")
        # print("_gr:\t", _gr)
        # print("res:\t", res)
        # print("---------------------------------")
        # print(res.expr)

        def __rm_rim_hook(list: List) -> Partition:
            p = Partition(list)
            acceptable_grid = (self._n-self._k, self._k)
            rim_size = self._n
            
            # if the partiton is in acceptable grid, just return the symbol
            if p.is_in_range(acceptable_grid[0], acceptable_grid[1]):
                return Schur(p.partition).symbol()

            # if the partiton is not in acceptable grid, apply the rim hooks
            # print("let's remove the rim hooks with rim_size = ", rim_size, " and acceptable_grid = ", acceptable_grid)
            x = p.remove_rim_hooks(rim_size=rim_size, acceptable_grid=acceptable_grid)
            exponent = (sum(list)-sum(x.partition))/rim_size
            return Schur(x.partition).symbol() * sp.Symbol('q')**int(exponent)
        
        res = res.apply2(lambda list: __rm_rim_hook(list))
        # print("res2:\t", res)
        return res


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


    def num2spec(self, p: int) -> Schur:
        return Schur([p]) if p > 0 else Schur([-p, 0])
    
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
