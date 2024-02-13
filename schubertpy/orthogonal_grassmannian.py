from .abstract_grassmannian import AbstractGrassmannian
from .qcalc import *

class OrthogonalGrassmannian(AbstractGrassmannian):
    def __init__(self, m: int, n: int):
        if n % 2 == 1:
            self._type = "B"
            self._k = (n-1)//2 - m
            self._n = (n-1)//2
            self._pieri = self.pieriB_inner
            self._qpieri = self.qpieriB_inner
        else:
            self._type = "D"
            self._k = n//2 - m
            self._n = n//2 -1
            self._pieri = self.pieriD_inner
            self._qpieri = self.qpieriD_inner


    def __str__(self) -> str:
        td = [
            "B", self._k, self._n, "OG", 
            self._n-self._k, 2*self._n+1, 
            self.degree_q()
        ]
        if self._type == "D":
            td = [
                "D", self._k, self._n, 
                "OG", self._n+1-self._k, 2*self._n+2,
                self.degree_q()
            ]
        return f"Type {td[0]} ;  (k,n) = ({td[1]},{td[2]}) ;  {td[3]}({td[4]},{td[5]}) ;  deg(q) = {td[6]}"
    
    def degree_q(self) -> int:
        return 2*self._n if self._k == 0 else self._n+self._k
    
    def schub_classes(self) -> List[Schur]:
        if not isinstance(self._type, str):
            raise ValueError("Must set type with IG or OG or set_type functions.")

        if self._type == "D":
            res = []
            mu_list = all_kstrict(self._k, self._n + 1 - self._k, self._n + self._k)
            for mu in mu_list:
                if self._k in mu:
                    res.append(Schur(mu))
                    res.append(Schur(mu+[0]))
                else:
                    res.append(Schur(mu))
            res = unique_schur_list(res)
            return res

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

        if self._type == "D" and self._k > 0:
            gen_list.append(Schur([self._k, 0]))

        gen_list.extend([Schur([i]) for i in range(self._k + 1, self._n + self._k + 1)])

        return gen_list

    def point_class(self) -> Schur:
        if not isinstance(self._type, str):
            raise ValueError("Must set type with IG or OG or set_type functions.")

        delta = 1
        if self._type == "D" and self._k > 0:
            delta = 0

        result = []
        for i in range(0, self._n - self._k - delta + 1):
            result.append(self._n + self._k - i)
        
        return Schur(result)

    def part2pair(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            lc = Schur(lc).symbol()
            return part2pair_inner(lc, self._k)
        else:
            lc = LinearCombination(lc)
            return apply_lc(lambda lam: part2pair_inner(lam, self._k), lc)
    

    def pair2part(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list) and len(lc) == 2:
            lc = Schur(lc).symbol()
            return pair2part_inner(lc)
        else:
            lc = LinearCombination(lc)
            return apply_lc(pair2part_inner, lc)
        
    def part2index(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return part2index(Schur(lc).symbol())
        
        lc = LinearCombination(lc)
        f = part2indexB_inner
        if self._type == "D":
            f = part2indexD_inner
        return apply_lc(lambda lam: f(lam, self._k, self._n), lc)
        

    def index2part(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return self.index2part(Schur(lc).symbol())
        
        lc = LinearCombination(lc)
        f = index2partB_inner
        if self._type == "D":
            f = index2partD_inner    
        return apply_lc(lambda idx: f(idx, self._k, self._n), lc)
    
    def dualize(self, lc: Union[sp.Expr, LinearCombination, str]) -> LinearCombination:
        lc = LinearCombination(lc)

        N = 2*self._n + 1
        if self._type == "D":
            N = 2*self._n + 2
        
        index = self.part2index(lc)
        # print("lc, index:", lc, index)
        return self.index2part(apply_lc(lambda idx: dualize_index_inner(idx, N, self._type), index))
    
    def type_swap(self, lc: Union[sp.Expr, LinearCombination, str, List[int]], k: int) -> LinearCombination:
        if isinstance(lc, list):
            return self.type_swap(Schur(lc).symbol())
        
        if self._type == "D":
            return apply_lc(lambda lam: type_swap_inner(lam, self._k), lc)
    
        return LinearCombination(lc)

    def miami_swap(self, lc: Union[sp.Expr, LinearCombination, str, List[int]]) -> LinearCombination:
        if isinstance(lc, list):
            return miami_swap(Schur(lc).symbol())
        if self._type == "D":
            return apply_lc(lambda lam: miami_swap_inner(lam, self._k), lc)
        return LinearCombination(lc)

    def schub_type(self, lam: Union[Schur, List[int]]) -> int:
        if self._type != "D" or not (isinstance(lam, list) or not isinstance(lam, Schur)):
            raise ValueError("No type defined.")
        
        if self._k not in lam:
            return 0
        elif len(lam) == 0 or lam[-1] > 0:
            return 1
        else:
            return 2



    # ##################################################################
    # # Type B: Quantum cohomology of odd orthogonal OG(n-k,2n+1).
    # ##################################################################
    @hashable_lru_cache(maxsize=None)
    def pieriB_inner(self, p: int, lam: List[int], k: int, n: int) -> LinearCombination:
        lam = list(lam)

        result = sp.Integer(0)
        b = 0 if p <= k else 1
        pset = pieri_set(p, lam, k, n, 0)
        for mu in pset:
            result += 2**(count_comps(lam, mu, False, k, 0) - b) * Schur(mu)
        return result

    def qpieriB_inner(self, p: int, lam: List[int], k: int, n: int) -> LinearCombination:
        q = sp.Symbol('q')
        
        res = self.pieriB_inner(p, lam, k, n)
        
        if k == 0:
            if len(lam) > 0 and lam[0] == n + k:
                res += q * apply_lc(lambda x: part_star(x, n+k), self.pieriB_inner(p, lam[1:], k, n))
        else:
            if len(lam) == n - k and lam[n-k-1] > 0:
                # print(self.pieriB_inner(p, lam, k, n + 1))
                res += q * apply_lc(lambda x: part_tilde(x, n-k+1, n+k), self.pieriB_inner(p, lam, k, n + 1))
            if len(lam) > 0 and lam[0] == n + k:
                # print(self.pieriB_inner(p, lam[1:], k, n))
                # print(apply_lc(lambda x: _part_star(x, n + k), self.pieriB_inner(p, lam[1:], k, n)))
                res += q**2 * apply_lc(lambda x: part_star(x, n + k), self.pieriB_inner(p, lam[1:], k, n))

        res = LinearCombination(res)
        return LinearCombination(sp.expand(res.expr))
    

    # ##################################################################
    # # Type D: Quantum cohomology of even orthogonal OG(n+1-k,2n+2).
    # ##################################################################
    @hashable_lru_cache(maxsize=None)
    def pieriD_inner(self, p: int, lam: List[int], k: int, n: int) -> LinearCombination:
        # print("pieriD_inner ------------------------")
        lam = list(lam)

        tlam = 0 if k not in lam else (2 if lam[-1] == 0 else 1)
        # print("lam: ", lam)
        # print("tlam: ", tlam)
        # print("pieriD_inner_pieri_set: ", pieri_set(abs(p),lam,k,n,1))
        # print("pieriD_inner -----------<<<<<<<<<<<<<<")

        res = sp.Integer(0)
        for mu in pieri_set(abs(p), lam, k, n, 1):
            res += self._dcoef(p, lam, mu, tlam, k, n)
        res = LinearCombination(res)
        # print("pieriD_inner res: ", res)
        return res

    def _dcoef(self, p: int, lam: List[int], mu: List[int], tlam: int, k: int, n: int) -> LinearCombination:
        cc = count_comps(lam, mu, False, k, 1) - (0 if abs(p) < k else 1)
        if cc >= 0:
            _expr = None
            if k not in mu or tlam == 1:
                _expr =  Schur(mu).symbol()
            elif tlam == 2:
                _expr = Schur(mu+[0]).symbol()
            else:
                _expr =  Schur(mu).symbol() + Schur(mu+[0]).symbol()
            return 2**cc * LinearCombination(_expr)
        
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
            if h == 0:
                return LinearCombination(Schur(mu).symbol())
            return LinearCombination(Schur(mu + [0]).symbol())
        if h == 0:
            return LinearCombination(0)
        if (tlam == 2 and k in mu):
            mu = mu + [0]
        return LinearCombination(Schur(mu).symbol())


    def _toSchurFromIntnMu(self, _intn: set, _mu: List[int]) -> LinearCombination:
        sch = Schur((list(_intn - set(_mu))[::-1]))
        return LinearCombination(sch.symbol())

    @hashable_lru_cache(maxsize=None)
    def qpieriD_inner(self, p, lam, k, n):
        # print("qpieriD_inner")

        lam = list(lam)

        q, q1, q2 = sp.symbols('q q1 q2')
        res = self.pieriD_inner(p, lam, k, n)

        # print("p, lam, k, n: ", p, lam, k, n)
        # print("(head) res: ", res)

        if k == 0:
            # print("case k==0")
            if len(lam) > 0 and lam[0] == n + k:
                res += q * apply_lc(lambda x: part_star(x, n + k),
                                    self.pieriD_inner(p, lam[1:], k, n))
        elif k == 1:
            # print("case k==1")
            if len(lam) >= n and lam[n-1] > 0:
                # print("case k==1, if1")
                lb = part_clip([max(x - 1, 0) for x in lam])
                # print("lb: ", lb)
                
                cprd = LinearCombination(Schur(lb).symbol())
                if abs(p) > 1:
                    cprd = self.pieriD_inner(abs(p) - 1, lb, 0, n) 
                # print("cprd: ", cprd)
                
                intn = set(range(1, n+1))
                # print("intn: ", intn)

                cprd = apply_lc(lambda mu: self._toSchurFromIntnMu(intn, mu), cprd)
                # print("cprd: ", cprd)
                
                res1 = 0
                if lam[-1] > 0 and p > 0:
                    res1 = q1 * apply_lc(lambda mu: Schur([x+1 for x in mu] + [1]*(n-len(mu))), cprd)
                if (lam[-1] == 0 or k not in lam) and (p == -1 or p > 1):
                    res1 += q2 * apply_lc(lambda mu: Schur([x+1 for x in mu] + [1]*(n-len(mu)) + [0]), cprd)
                
                # print("res: ", res)
                # print("res1: ", res1)
                # print("dualize_res1: ", dualize(res1))
                
                res += self.dualize(res1)

                # print("res: ", res)

            if len(lam) > 0 and lam[0] == n + k:
                # print("case k==1, if2")
                res += q1 * q2 * apply_lc(lambda x: part_star(x, n + k), self.pieriD_inner(p, lam[1:], k, n))
        else:
            # print("case k==else")
            if len(lam) >= n + 1 - k and lam[n + 1 - k - 1] > 0:
                # print("case k==else, if1")
                res += q * self.type_swap(apply_lc(lambda x: part_tilde(x, n - k + 2, n + k),
                                            self.pieriD_inner(p, lam, k, n + 1)), k)
            if len(lam) > 0 and lam[0] == n + k:
                # print("case k==else, if2")
                res += q**2 * apply_lc(lambda x: part_star(x, n + k), self.pieriD_inner(p, lam[1:], k, n))
            
            # print("res: ", res)
        res = LinearCombination(res)
        return LinearCombination(sp.expand(res.expr))

