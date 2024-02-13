from .abstract_grassmannian import AbstractGrassmannian
from .qcalc import *

class IsotropicGrassmannian(AbstractGrassmannian):
    def __init__(self, m: int, n: int):
        if n % 2 == 1:
            raise ValueError("n must be even.")
    
        self._type = "C"
        self._k = n//2 - m
        self._n = n//2
        self._pieri = self.pieriC_inner
        self._qpieri = self.qpieriC_inner
    

    def __str__(self) -> str:
        td = [
            "C", self._k, self._n, 
            "IG", self._n-self._k, 2*self._n, 
            self.degree_q()
        ]
        return f"Type {td[0]} ;  (k,n) = ({td[1]},{td[2]}) ;  {td[3]}({td[4]},{td[5]}) ;  deg(q) = {td[6]}"
    
    
    def degree_q(self) -> int:
        return self._n+1+self._k
    

    def schub_classes(self) -> List[Schur]:
        if not isinstance(self._type, str):
            raise ValueError("Must set type with IG or OG or set_type functions.")

        lam_list = all_kstrict(self._k, self._n - self._k, self._n + self._k)
        res = [Schur(lam) for lam in lam_list]
        res = unique_schur_list(res)
        return res
    

    def generators(self) -> List[Schur]:
        if not isinstance(self._type, str):
            raise ValueError("Must set type with IG or OG or set_type functions.")

        if self._type != "D" and self._k == self._n:
            return []

        gen_list = [Schur([i]) for i in range(1, self._k + 1)]
        gen_list.extend([Schur([i]) for i in range(self._k + 1, self._n + self._k + 1)])

        return gen_list


    def point_class(self) -> Schur:
        if not isinstance(self._type, str):
            raise ValueError("Must set type with IG or OG or set_type functions.")

        delta = 1
        result = []
        for i in range(0, self._n - self._k - delta + 1):
            result.append(self._n + self._k - i)        
        return Schur(result)


    def part2pair(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return part2pair_inner(lc, self._k)
        else:
            return apply_lc(lambda lam: part2pair_inner(lam, self._k), lc)
    

    def pair2part(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list) and len(lc) == 2:
            return pair2part_inner(lc)
        else:
            return apply_lc(pair2part_inner, lc)
        
        
    def part2index(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return part2index(Schur(lc).symbol())
        return apply_lc(lambda lam: part2indexC_inner(lam, self._k, self._n), lc)
        

    def index2part(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return self.index2part(Schur(lc).symbol())
        return apply_lc(lambda idx: index2partC_inner(idx, self._k, self._n), lc)
        
    def dualize(self, lc: Union[sp.Expr, LinearCombination, str]) -> Any:
        lc = LinearCombination(lc)
        N = 2*self._n
        
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
    # # Type C: Quantum cohomology of symplectic IG(n-k,2n).
    # ##################################################################
    @hashable_lru_cache(maxsize=None)
    def pieriC_inner(self, i: int, lam: List[int], k: int, n: int) -> LinearCombination:
        lam = list(lam)

        result = sp.Integer(0)
        for x in pieri_set(i, lam, k, n, 0):
            result += 2**count_comps(lam, x, True, k, 0) * Schur(x)
        return result


    def qpieriC_inner(self, i: int, lam: List[int], k: int, n: int) -> LinearCombination:
        q = sp.Symbol('q')
        inner_result = self.pieriC_inner(i, lam, k, n)
        second_term = q/2 * apply_lc(lambda x: part_star(x, n+k+1), self.pieriC_inner(i, lam, k, n+1))
        return inner_result + second_term
