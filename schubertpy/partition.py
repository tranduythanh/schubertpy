from collections import OrderedDict
from typing import *
from .util import *

def _is_non_increasing(part: List[int]):
    # Iterate through the list, comparing each element with the next one
    for i in range(len(part) - 1):
        # If the current element is smaller than the next one,
        # the list is not in descending order
        if part[i] < part[i + 1]:
            return False
    return True

def is_valid_part(part: List[int]) -> bool:
    if not isinstance(part, list):
        return False
    if not all(isinstance(x, int) for x in part):
        return False
    if not all(x >= 0 for x in part):
        return False
    if not _is_non_increasing(part):
        return False
    return True

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
    lambda_ = lambda_.copy()
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

class Partition:
    def __init__(self, partition: List[int]):
        if not is_valid_part(partition):
            raise ValueError("Invalid partition")
        self.partition = partition

    def __str__(self):
        return str(self.partition)

    def __repr__(self):
        return f"Partition({self.partition})"
    
    def draw(self):
        if len(self.partition) == 0:
            print("0")
            return
        
        for row in self.partition:
            print('[]' * row)

    def _max_rim_size(self) -> int:
        return sum(self.partition) + len(self.partition) - 1
    
    def is_in_range(self, nrow: int, ncol: int) -> bool:
        if nrow < 0 or ncol < 0:
            raise ValueError("nrow and ncol must be non-negative")
        
        if len(self.partition) == 0:
            return True
        
        if len(self.partition) > nrow:
            return False
        
        if self.partition[0] > ncol:
            return False
    
        return True

    def remove_rim_hooks(self, rim_size: int, acceptable_grid: Tuple[int, int]) -> 'Partition':
        if len(self.partition) == 0:
            return Partition([])
        if rim_size <= 0:
            return Partition(self.partition)
        if rim_size > self._max_rim_size():
            return Partition([])
        
        _partition = self.partition + [0]
        _rim_size = rim_size
        nrow, ncol = acceptable_grid

        # print("original partition")
        # self.draw()
        # print("\nlet's remove rim hooks")

        for i in range(len(_partition)-1):
            delta = _partition[i] - _partition[i+1]
            if delta >= _rim_size:
                _partition[i] -= _rim_size
                _rim_size -= delta
                break
            if _partition[i+1] > 0:
                delta += 1
            _rim_size -= delta
            _partition[i] -= delta
            # print(_partition, _rim_size)
    
        if _rim_size > 0:
            return Partition([])
        
        if not _is_non_increasing(_partition):
            return Partition([])
        
        _partition = part_clip(_partition)
        new_partition = Partition(_partition)
        
        # print("\nnew partition")
        new_partition.draw()
        if new_partition.is_in_range(nrow, ncol):
            return new_partition
        return new_partition.remove_rim_hooks(rim_size, acceptable_grid)

    
if __name__ == "__main__":
    p = Partition([5, 5])
    p.remove_rim_hooks(rim_size=5, acceptable_grid=(2, 3))