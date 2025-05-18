from typing import List, Optional, Set, Tuple
from ..partition import part_clip

def _first_kstrict(k: int, rows: int, cols: int) -> List[int]:
    """Generate the first k-strict partition in lexicographic order.
    
    A k-strict partition is a partition where each part is at least k and the difference
    between consecutive parts is at most 1. This function generates the first such partition
    with given dimensions.
    
    Args:
        k (int): The minimum value for each part in the partition
        rows (int): The number of rows in the partition
        cols (int): The maximum number of columns in the partition
        
    Returns:
        List[int]: A list representing the first k-strict partition, where each element
                  is the length of the corresponding row. The partition is constructed
                  by starting with the maximum possible value (cols) and decreasing by 1
                  for each row, but never going below k.
                  
    Example:
        >>> _first_kstrict(k=2, rows=3, cols=5)
        [5, 4, 3]  # First k-strict partition with k=2, 3 rows, max width 5
    """
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

itr_kstrict = _itr_kstrict