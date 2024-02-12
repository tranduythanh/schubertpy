from qcalc import *

class Grassmannian(object):
    def __init__(self, m, n):
        self._type = "A"
        self._k = n-m
        self._n = n
    

    def __str__(self) -> str:
        td = ["A", self._k, self._n, "Gr", self._n-self._k, self._n, self._n]
        return f"Type {td[0]} ;  (k,n) = ({td[1]},{td[2]}) ;  {td[3]}({td[4]},{td[5]}) ;  deg(q) = {td[6]}"
    
    def schub_classes(self) -> List[Schur]:
        if not isinstance(self._type, str):
            fail_no_type()

        mu = [self._k] * (self._n - self._k)
        partitions = part_gen(mu)
        partitions.sort()
        res = [Schur(lam) for lam in partitions]
        res = unique_schur_list(res)
        return res
    
    def generators(self) -> List[Schur]:
        if not isinstance(self._type, str):
            fail_no_type()

        if self._type != "D" and self._k == self._n:
            return []

        gen_list = [Schur([i]) for i in range(1, self._k + 1)]

        return gen_list

    def point_class(self) -> Schur:
        if not isinstance(self._type, str):
            fail_no_type()

        if self._k > 0:
            return Schur((([self._k] * (self._n - self._k))))
        return []

    def part2pair(self, lc: Any) -> Any:
        raise Exception("Only types B,C,D.")
    

    def pair2part(self, lc: Any) -> Any:
        raise Exception("Only types B,C,D.")
        
    def part2index(self, lc: Any) -> LinearCombination:
        if isinstance(lc, list):
            return part2index(Schur(lc))
        return apply_lc(lambda lam: part2indexA_inner(lam, self._k, self._n), lc)
        

    def index2part(self, lc: Any) -> LinearCombination:
        if isinstance(lc, list):
            return self.index2part(Schur(lc))
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

    def miami_swap(self, lc: Any) -> Any:
        if isinstance(lc, list):
            return miami_swap(Schur(lc))
        return lc

    def schub_type(self, lam: Union[Schur, List[int]]) -> int:
        raise ValueError("No type defined.")
        

    def pieri(self, i: int, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        if isinstance(lc, list):
            return pieriA_inner(i, lc, self._k, self._n)
        else:
            return apply_lc(lambda p: pieriA_inner(i, p, self._k, self._n), lc)


    def act(self, expr: Union[sp.Expr, LinearCombination, str], lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        expr = LinearCombination(expr).expr
        lc = LinearCombination(lc)
        return act_lc(expr, lc, lambda i, p: pieriA_inner(i, p, self._k, self._n))


    def giambelli(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc = LinearCombination(lc)
        return giambelli_rec(lc, lambda i, p: pieriA_inner(i, p, self._k, self._n), self._k)


    def mult(self, lc1: Union[sp.Expr, LinearCombination, str], lc2: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc1 = LinearCombination(lc1)
        lc2 = LinearCombination(lc2)
        return self.act(giambelli(lc1), lc2)


    def toS(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc = LinearCombination(lc)
        return self.act(giambelli(lc), Schur([]).symbol())


    def qpieri(self, i: int, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc = LinearCombination(lc)
        if isSchur(lc.expr):
            lam = toSchur(lc.expr).p
            return qpieriA_inner(i, lam, self._k, self._n)
        return apply_lc(lambda p: qpieriA_inner(i, p, self._k, self._n), lc)


    def qact(self, expr: Union[sp.Expr, LinearCombination, str], lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        # print("qact")
        expr = LinearCombination(expr).expr
        lc = LinearCombination(lc)
        # print("expr: ", expr)
        # print("lc: ", lc)
        return act_lc(expr, lc, lambda i, p: qpieriA_inner(i, p, self._k, self._n))


    def qgiambelli(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        # print("qgiambelli")
        lc = LinearCombination(lc)
        # print("lc: ", lc)
        return giambelli_rec(lc, lambda i, p: qpieriA_inner(i, p, self._k, self._n), self._k)


    def qmult(self, lc1: Union[sp.Expr, LinearCombination, str], lc2: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc1 = LinearCombination(lc1)
        lc2 = LinearCombination(lc2)
        # print("qmult")
        # print("lc1: ", lc1)
        # print("lc2: ", lc2)
        return self.qact(self.qgiambelli(lc1), lc2)


    def qtoS(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        # print("qtoS")
        lc = LinearCombination(lc)
        return self.qact(self.qgiambelli(lc).expr, LinearCombination(Schur([]).symbol()))
    

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
                return LinearCombination(q * Schur())
            
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