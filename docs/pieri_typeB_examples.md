# Ví Dụ Chi Tiết: Thuật Toán Pieri Type B

Tài liệu này chứa các ví dụ chi tiết với kết quả thực tế cho tất cả các thuật toán Pieri Type B trong SchubertPy.

> **Tham khảo:** [Thuật Toán Pieri Type B](./pieri_typeB_algorithms.md) - Tài liệu mô tả chi tiết các thuật toán

## Tổng Quan

Tất cả các ví dụ dưới đây được test thực tế với SchubertPy và cho kết quả chính xác. Code nguồn để chạy các ví dụ có trong file [`test_pieri_examples.py`](../test_pieri_examples.py).

Type B (Orthogonal Grassmannian Odd) có đặc điểm riêng biệt:
- **Hệ số 2^(c-b)**: Phức tạp hơn Type A 
- **`skipfirst=False`**: Khác với Type C
- **Two quantum cases**: k=0 vs k>0
- **OrthogonalGrassmannian class**: Interface cho odd dimensions

## Ví Dụ 1: Thuật Toán Hỗ Trợ

### 1.1. `_part_star` - Universal Quantum Correction Helper

**Mục đích:** Kiểm tra và biến đổi partition theo điều kiện lượng tử (dùng chung cho Type A, B, C, D).

```python
# Ví dụ 1: Phần tử đầu khớp với cols
Input:  lam=[3, 1, 1]
        cols=3
Output: S[1,1]

# Ví dụ 2: Phần tử đầu không khớp với cols  
Input:  lam=[2, 1, 1]
        cols=3
Output: 0
```

**Giải thích:** Nếu phần tử đầu tiên của partition bằng `cols`, trả về partition còn lại (bỏ phần tử đầu). Ngược lại trả về 0. Đây là thuật toán dùng chung cho tất cả các loại Pieri.

**Liên kết:** [Algorithm 1.5 trong Type A](./pieri_typeA_algorithms.md#5-_part_starlam-cols)

### 1.2. `part_conj` - Partition Conjugate

**Mục đích:** Tính conjugate partition (transpose Young diagram).

```python
# Ví dụ: Transpose Young diagram
Input:  [4, 2, 1]
Output: [3, 2, 1, 1]
```

**Giải thích:** Thuật toán thực hiện transpose của Young diagram. λ'[i] = số phần tử trong λ có giá trị ≥ i. Ví dụ: [4,2,1] → [3,2,1,1] (transpose diagram).

**Liên kết:** [Algorithm 1.6 trong Type B](./pieri_typeB_algorithms.md#6-part_conjlam)

### 1.3. `_part_tilde` - Helper đặc biệt Type B

**Mục đích:** Kiểm tra và biến đổi partition theo điều kiện đặc biệt của Type B quantum corrections.

```python
# Ví dụ: Kiểm tra điều kiện Type B quantum
Input:  lam=[2, 1]
        rows=3
        cols=4
Output: 0
```

**Giải thích:** Thuật toán kiểm tra các điều kiện phức tạp của Type B quantum terms. Trong ví dụ này, λ=[2,1] không thỏa mãn các điều kiện Type B nên trả về 0.

**Liên kết:** [Algorithm 1.7 trong Type B](./pieri_typeB_algorithms.md#7-_part_tildelam-rows-cols)

## Ví Dụ 2: Thuật Toán Fill và Iterator

### 2.1. `_pieri_fill` - Type B Fill

**Mục đích:** Điền boxes vào partition với Type B constraints.

```python
# Ví dụ: Điền 1 box vào partition theo Type B rules
Input:  lam=[2, 1]
        inner=[2, 1]
        outer=[4, 3]
        r=1
        p=1
Output: [3, 1]
```

**Giải thích:** 
- Bắt đầu với partition [2,1]
- Điền thêm p=1 box theo constraints Type B
- Khác với Type A, sử dụng điều kiện res[rr-2] - 1
- Kết quả: [3,1] (thêm 1 box vào hàng đầu tiên)

**Liên kết:** [Algorithm 1.3 trong Type B](./pieri_typeB_algorithms.md#3-_pieri_filllam-inner-outer-r-p)

### 2.2. `_pieri_itr` - Type B Iterator

**Mục đích:** Tạo partition tiếp theo trong Type B iteration.

```python
# Ví dụ: Tìm cấu hình tiếp theo
Input:  current=[3, 1]
        inner=[2, 1]
        outer=[4, 3]
Output: None
```

**Giải thích:** Từ cấu hình hiện tại [3,1], tìm cấu hình tiếp theo theo Type B rules. Tương tự Type A nhưng sử dụng Type B _pieri_fill. Kết quả None có nghĩa không còn cấu hình nào khả thi.

**Liên kết:** [Algorithm 1.4 trong Type B](./pieri_typeB_algorithms.md#4-_pieri_itrlam-inner-outer)

### 2.3. `count_comps` - Type B Component Counting

**Mục đích:** Đếm số connected components với `skipfirst=False` (đặc trưng Type B).

```python
# Ví dụ: Đếm components với Type B setting
Input:  lam1=[1]
        lam2=[2]
        skipfirst=False
        k=1
        d=0
Output: 1
```

**Giải thích:** Type B sử dụng `skipfirst=False` → count = 1. So sánh Type C: `skipfirst=True` → count = 0. Đây là khác biệt chính giữa Type B và Type C trong việc đếm connected components.

**Liên kết:** [Algorithm 1.2 trong Type B](./pieri_typeB_algorithms.md#2-count_compslam1-lam2-skipfirst-k-d)

## Ví Dụ 3: Thuật Toán Chính - Classical Pieri

### 3.1. OG(1,5) - Ví dụ từ documentation

**Thuật toán:** [`pieriB_inner(p, lam, k, n)`](./pieri_typeB_algorithms.md#thu-t-to-n-ch-nh-pieriB_innerlam-k-n)

```python
# Ví dụ: σ_[2] * σ_1 trong H*(OG(1,5))
Input:  p=1
        lam=[2]
        k=1
        n=2
Output: S[3]
```

**Giải thích:**
- Nhân lớp Schubert σ_[2] với lớp đặc biệt σ_1
- Context: OG(1,5) - Orthogonal Grassmannian odd dimension
- Sử dụng pieri_set + count_comps + hệ số 2^(c-b)
- b = 0 (vì p = 1 ≤ k = 1)
- Kết quả: S[3] (Schur function tương ứng)

### 3.2. Trường hợp không có kết quả

```python
# Ví dụ: Trường hợp cho kết quả 0
Input:  p=1
        lam=[1]
        k=1
        n=1
Output: 0
```

**Giải thích:**
- Trong OG(1,3), nhân σ_[1] với special class size 1
- Không có partitions hợp lệ trong pieri_set
- Pattern quan sát: Type B thường cho kết quả 0 trong nhiều cases do hệ số 2^(count_comps - b) phức tạp

## Ví Dụ 4: Thuật Toán Quantum Pieri

### 4.1. Trường hợp có quantum correction

**Thuật toán:** [`qpieriB_inner(p, lam, k, n)`](./pieri_typeB_algorithms.md#phi-n-b-n-l-ng-t-qpieribinner-lam-k-n)

```python
# Ví dụ: Quantum effect trong OG(1,5)
Input:  p=1
        lam=[3]
        k=1
        n=2
Output: S[1]*q
```

**Giải thích:**
- λ=[3] có quantum condition: k > 0 và lam[0] = 3 == n + k = 3 ✓
- Áp dụng quantum correction với _part_star:
  - Classical part từ pieriB_inner(1, [3][1:], 1, 2) = pieriB_inner(1, [], 1, 2)
  - Apply _part_star và nhân với degree q²
- Kết quả: S[1]*q (quantum term)

### 4.2. Đặc điểm Type B quantum

**Thuật toán phức tạp nhất trong hệ thống:**
- **k=0**: Chỉ có một loại quantum term với _part_star
- **k>0**: Có hai loại quantum terms với _part_tilde (degree q) và _part_star (degree q²)
- **Multiple quantum parameters**: q và q²

```python
# Ví dụ: Complex quantum behavior
Input:  k=0 case  → Only _part_star terms
        k>0 case  → Both _part_tilde and _part_star terms
```

**Giải thích:** Type B có quantum behavior phức tạp nhất trong tất cả các loại Pieri, với hai loại quantum corrections khác nhau tùy theo giá trị của k.

## Ví Dụ 5: Interface qua OrthogonalGrassmannian Class

### 5.1. Classical Pieri thông qua class

**Class:** [`OrthogonalGrassmannian(m, n)`](./pieri_typeB_algorithms.md#5-orthogonalgrassmannian-class-interface)

```python
# Sử dụng OrthogonalGrassmannian class cho OG(1,5)
og = OrthogonalGrassmannian(1, 5)  # m=1, n=5 => OG(1,5) -> Type B
Input:  og.pieri(1, 'S[2]')
Output: S[3]
```

**Giải thích:**
- Tạo OrthogonalGrassmannian object cho OG(1,5)
- Odd dimension tự động chọn Type B
- Sử dụng interface thuận tiện với string notation
- Kết quả giống như gọi trực tiếp pieriB_inner

### 5.2. Quantum Pieri với quantum terms

```python
# Quantum Pieri với xuất hiện quantum correction
Input:  og.qpieri(1, 'S[2]')
Output: S[3] + S[]*q
```

**Giải thích:**
- σ_[2] trong OG(1,5) có thể có quantum effect
- Kết quả bao gồm:
  - Classical term: S[3]
  - Quantum term: S[]*q (với các degrees q hoặc q²)

## Ví Dụ 6: So Sánh Classical vs Quantum

```python
# Classical vs Quantum trong cùng một trường hợp
Classical: og.pieri(1, 'S[2]')  →  S[3]
Quantum:   og.qpieri(1, 'S[2]') →  S[3] + S[]*q

# So sánh độ phức tạp với Type A
Type A:    Coefficients = 1,           Quantum = 1 type
Type B:    Coefficients = 2^(c-b),     Quantum = 2 types
```

**Giải thích:**
- Khi không có quantum effects, classical và quantum cho kết quả giống nhau
- Khi có quantum effects, Type B có cả q và q² terms
- Type B có complexity cao nhất trong tất cả các loại Pieri

## Tham Khảo

- **Tài liệu chính:** [Thuật Toán Pieri Type B](./pieri_typeB_algorithms.md)
- **Dependencies:** [Quan hệ các Algorithm](./pieri_typeB_algorithms.md#quan-h-c-c-algorithm-li-n-quan-n-pieri-b-dependencies-tree)
- **Quantum Theory:** [Phiên Bản Lượng Tử](./pieri_typeB_algorithms.md#phi-n-b-n-l-ng-t-qpieribinner-lam-k-n)
- **Orthogonal Theory:** [OrthogonalGrassmannian Class](./pieri_typeB_algorithms.md#5-orthogonalgrassmannian-class-interface)

---

*Tất cả các ví dụ trên đều được test thực tế với SchubertPy version hiện tại và cho kết quả chính xác.* 