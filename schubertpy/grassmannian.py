from .abstract_grassmannian import AbstractGrassmannian
from .qcalc import *

class Grassmannian(AbstractGrassmannian):
    _type: str
    _k: int
    _n: int
    _pieri: Callable
    _qpieri: Callable

    def __init__(self, m: int, n: int):
        self._type = "A"
        self._k = n-m
        self._n = n
        self._pieri = self.pieriA_inner
        self._qpieri = self.qpieriA_inner
    

    def __str__(self) -> str:
        td = [
            "A", self._k, self._n, 
            "Gr", self._n-self._k, self._n, 
            self.degree_q()
        ]
        return f"Type {td[0]} ;  (k,n) = ({td[1]},{td[2]}) ;  {td[3]}({td[4]},{td[5]}) ;  deg(q) = {td[6]}"
    
    def degree_q(self) -> int:
        return self._n
    
    def schub_classes(self) -> List[Schur]:
        if not isinstance(self._type, str):
            raise ValueError("Must set type with IG or OG or set_type functions.")

        mu = [self._k] * (self._n - self._k)
        partitions = part_gen(mu)
        partitions.sort()
        res = [Schur(lam) for lam in partitions]
        res = unique_schur_list(res)
        return res
    
    def generators(self) -> List[Schur]:
        if not isinstance(self._type, str):
            raise ValueError("Must set type with IG or OG or set_type functions.")

        if self._type != "D" and self._k == self._n:
            return []

        gen_list = [Schur([i]) for i in range(1, self._k + 1)]

        return gen_list

    def point_class(self) -> Schur:
        if not isinstance(self._type, str):
            raise ValueError("Must set type with IG or OG or set_type functions.")

        if self._k > 0:
            return Schur((([self._k] * (self._n - self._k))))
        return []

    def part2pair(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        raise Exception("Only types B,C,D.")
    

    def pair2part(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        raise Exception("Only types B,C,D.")
        
    def part2index(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return part2index(Schur(lc).symbol())
        return apply_lc(lambda lam: part2indexA_inner(lam, self._k, self._n), lc)
        

    def index2part(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return self.index2part(Schur(lc).symbol())
        return apply_lc(lambda idx: index2partA_inner(idx, self._k, self._n), lc)
        
    def dualize(self, lc: Union[sp.Expr, LinearCombination, str]) -> Any:
        lc = LinearCombination(lc)
        N = self._n
        
        index = self.part2index(lc)
        # print("lc, index:", lc, index)
        return self.index2part(apply_lc(lambda idx: dualize_index_inner(idx, N, self._type), index))
    
    def type_swap(self, lc: Union[sp.Expr, LinearCombination, str, List[int]], k: int) -> LinearCombination:
        if isinstance(lc, list):
            return self.type_swap(Schur(lc).symbol())
        return LinearCombination(lc)

    def miami_swap(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return miami_swap(Schur(lc).symbol())
        return lc

    def schub_type(self, lam: Union[Schur, List[int]]) -> int:
        raise ValueError("No type defined.")


    # ##################################################################
    # # Type A: Quantum cohomology of Gr(n-k,n).
    # ##################################################################

    # DO NOT MODIFY THIS FUNCTION
    @hashable_lru_cache(maxsize=None)
    def pieriA_inner(self, i: int, lam: List[int], k: int, n: int) -> LinearCombination:
        lam = list(lam)

        inner = padding_right(lam, 0, n-k-len(lam))
        outer = [k] + inner[:-1]
        mu = pieri_fillA(inner, inner, outer, row_index=0, p=i)
        res = 0
        while isinstance(mu, list):
            res = Schur(part_clip(mu)) + res
            mu = pieri_itrA(mu, inner, outer)
        return LinearCombination(res)


    def qpieriA_inner(self, i: int, lam: List[int], k: int, n: int) -> LinearCombination:
        q = sp.Symbol('q')
        res = self.pieriA_inner(i, lam, k, n)
        if len(lam) == n-k and lam[n-k-1] > 0:
            if k == 1:
                return LinearCombination(q * Schur([]))
            
            # gen new lab
            lab = []
            for j in range(len(lam)):
                if lam[j] > 1:
                    lab.append(lam[j] - 1)

            z = apply_lc(lambda x: part_star(x, k - 1), self.pieriA_inner(i - 1, lab, k - 1, n))
            if isinstance(z, sp.Number):
                z = LinearCombination(z)
            res += q * sp.expand(z.expr)
        return LinearCombination(res)
    
    def qmult_rh(
        self, 
        lc1: Union[sp.Expr, LinearCombination, str, Schur, List[int]], 
        lc2: Union[sp.Expr, LinearCombination, str, Schur, List[int]],
    ) -> LinearCombination:
        n = self._n
        kp = n - self._k

        _gr = self.clone()
        _kp = _gr._n-_gr._k
        # _gr._n = _gr._n + _delta
        # _gr._k = _gr._k + _delta

        
        _gr._n = 2*n - 1
        _gr._k = _gr._n - kp

        # print(f"expanded Grassmannian: Gr({_gr._n-_gr._k},{_gr._n})")
        res = _gr.mult(lc1, lc2)
        # print("qmult_rh")
        # print("_gr:\t", _gr)
        # print("res:\t", res)
        # print("---------------------------------")
        # print(res.expr)

        def __rm_rim_hook(arr: List) -> Partition:
            p = Partition(arr)
            acceptable_grid = (self._n-self._k, self._k)
            rim_size = self._n

            # print("__rm_rim_hook: ", arr, "\trim_size = ", rim_size, "\tacceptable_grid = ", acceptable_grid)
            
            # if the partiton is in acceptable grid, just return the symbol
            if p.is_in_range(acceptable_grid[0], acceptable_grid[1]):
                return Schur(p.partition).symbol()

            # if the partiton is not in acceptable grid, apply the rim hooks
            # print("let's remove the rim hooks with rim_size = ", rim_size, " and acceptable_grid = ", acceptable_grid)
            x, q_num, height = p.remove_rim_hooks(rim_size=rim_size, acceptable_grid=acceptable_grid)

            sign = (-1)**(height-kp)
            # sign = (-1)**(n - kp - height)

            # print("removed rim hooks:", x, "\tq_num = ", q_num, "\theight = ", height, "\tsign = ", sign)


            if q_num > 0:
                return Schur(x.partition).symbol() * sp.Symbol('q')**int(q_num) * sign
            if x == 0 or len(x.partition) == 0:
                return 0
            return Schur(x.partition).symbol() * sign
        
        # print("intermediate resolution:\t", res)
        res = res.apply2(lambda arr: __rm_rim_hook(arr))
        # print("res2:\t", res)
        return res