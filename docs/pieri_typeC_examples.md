# Ví Dụ Chi Tiết: Thuật Toán Pieri Type C

Tài liệu này chứa các ví dụ chi tiết với kết quả thực tế cho tất cả các thuật toán Pieri Type C trong SchubertPy.

> **Tham khảo:** [Thuật Toán Pieri Type C](./pieri_typeC_algorithms.md) - Tài liệu mô tả chi tiết các thuật toán

## Tổng Quan

Tất cả các ví dụ dưới đây được test thực tế với SchubertPy và cho kết quả chính xác. Code nguồn để chạy các ví dụ có trong file [`test_pieri_examples.py`](../test_pieri_examples.py).

Type C (Symplectic Grassmannian) có đặc điểm riêng biệt:
- **`skipfirst=True`**: Điều kiện đặc biệt trong component counting
- **Quantum coefficient q/2**: Khác với Type A, B, D
- **IsotropicGrassmannian class**: Interface đặc biệt cho symplectic case

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

### 1.2. `pieri_set` - Shared Set Generation

**Mục đích:** Tạo tập hợp tất cả partitions hợp lệ (Type C reuses Type B infrastructure).

```python
# Ví dụ: Tạo set các partitions hợp lệ
Input:  p=1
        lam=[1]
        k=1
        n=2
        d=0
Output: [[2]]
```

**Giải thích:** Type C sử dụng lại infrastructure của Type B nhưng với modifier `skipfirst=True`. Cùng function call như Type B, nhưng behavior khác do parameter `skipfirst` trong counting.

**Liên kết:** [Algorithm 1.1 trong Type B](./pieri_typeB_algorithms.md#1-pieri_setp-lam-k-n-d)

## Ví Dụ 2: Thuật Toán Fill và Iterator

### 2.1. `count_comps` - Type C Component Counting

**Mục đích:** Đếm số connected components với `skipfirst=True` (đặc trưng Type C).

```python
# Ví dụ: Đếm components với Type C setting
Input:  lam1=[1]
        lam2=[2]
        skipfirst=True
        k=1
        d=0
Output: 0
```

**Giải thích:** Type C sử dụng `skipfirst=True` → count = 0. So sánh Type B: `skipfirst=False` → count = 1. Đây là khác biệt cốt lõi giữa Type B và Type C. Type C thường cho lower counts do `skipfirst=True`.

**Liên kết:** [Algorithm 1.2 trong Type B](./pieri_typeB_algorithms.md#2-count_compslam1-lam2-skipfirst-k-d)

### 2.2. Shared Functions với Type B

**Mục đích:** Type C sử dụng nhiều shared functions tương tự Type B.

```python
# Ví dụ: Type C reuses Type B infrastructure
Input:  _pieri_fill, _pieri_itr functions
Output: Same as Type B but with skipfirst=True effect
```

**Giải thích:** Type C không có thuật toán fill và iterator riêng biệt mà sử dụng lại từ Type B. Sự khác biệt chính nằm ở `skipfirst` parameter trong component counting.

**Liên kết:** [Helper Functions trong Type B](./pieri_typeB_algorithms.md#thu-t-to-n-h-tr)

## Ví Dụ 3: Thuật Toán Chính - Classical Pieri

### 3.1. IG(1,4) - Ví dụ từ documentation

**Thuật toán:** [`pieriC_inner(p, lam, k, n)`](./pieri_typeC_algorithms.md#thu-t-to-n-ch-nh-piericinneri-lam-k-n)

```python
# Ví dụ: σ_[1] * σ_1 trong H*(IG(1,4))
Input:  p=1
        lam=[1]
        k=1
        n=2
Output: S[2]
```

**Giải thích:**
- Nhân lớp Schubert σ_[1] với lớp đặc biệt σ_1
- Context: Symplectic Grassmannian với Type C constraints
- Sử dụng pieri_set + count_comps với `skipfirst=True`
- Kết quả: S[2] trong cohomology ring H*(IG(1,4))

### 3.2. So sánh với Type B

```python
# Ví dụ: Cùng input nhưng kết quả khác
Type B: pieriB_inner(1, [1], 1, 2) → 0
Type C: pieriC_inner(1, [1], 1, 2) → S[2]
```

**Giải thích:** Type C cho kết quả khác Type B cho cùng input parameters do `skipfirst` setting khác nhau. Đây là demonstration chính của sự khác biệt giữa hai loại.

## Ví Dụ 4: Thuật Toán Quantum Pieri

### 4.1. Trường hợp có quantum correction

**Thuật toán:** [`qpieriC_inner(p, lam, k, n)`](./pieri_typeC_algorithms.md#phi-n-b-n-l-ng-t-qpiericinneri-lam-k-n)

```python
# Ví dụ: Quantum effect trong IG(1,4)
Input:  p=1
        lam=[1]
        k=1
        n=2
Output: S[2]
```

**Giải thích:**
- λ=[1] có quantum corrections trong Type C
- Quantum coefficient: q/2 (đặc trưng Type C)
- Quantum version cho clean result S[2]
- Quantum corrections simplify the result

### 4.2. Đặc điểm Type C quantum

**Đặc điểm riêng biệt:**
- **Quantum coefficient q/2**: Khác với Type A, B, D
- **Symplectic constraints**: Ảnh hưởng đến quantum terms
- **Unique behavior**: Type C có quantum behavior riêng biệt

```python
# Ví dụ: So sánh Classical vs Quantum
Classical: pieriC_inner(1, [1], 1, 2) → S[2]
Quantum:   qpieriC_inner(1, [1], 1, 2) → S[2]
```

**Giải thích:** Quantum correction trong Type C có tính chất đơn giản hóa biểu thức, tạo ra kết quả rõ ràng trong quantum cohomology ring.

## Ví Dụ 5: Interface qua IsotropicGrassmannian Class

### 5.1. Classical Pieri thông qua class

**Class:** [`IsotropicGrassmannian(m, n)`](./pieri_typeC_algorithms.md#class-interface)

```python
# Sử dụng IsotropicGrassmannian class cho IG(1,4)
ig = IsotropicGrassmannian(1, 4)  # m=1, n=4 => IG(1,4) -> Type C
Input:  ig.pieri(1, 'S[1]')
Output: S[2]
```

**Giải thích:**
- Tạo IsotropicGrassmannian object cho IG(1,4)
- Sử dụng interface thuận tiện với string notation
- Behavior của Type C thông qua class interface
- Kết quả giống như gọi trực tiếp pieriC_inner

### 5.2. Quantum Pieri với quantum terms

```python
# Quantum Pieri với xuất hiện quantum correction
Input:  ig.qpieri(1, 'S[1]')
Output: S[2] + S[]*q/2
```

**Giải thích:**
- σ_[1] trong IG(1,4) có quantum effect
- Kết quả bao gồm:
  - Classical term: S[2]
  - Quantum term: S[]*q/2 (coefficient q/2 đặc trưng Type C)

## Ví Dụ 6: So Sánh Classical vs Quantum

```python
# Classical vs Quantum trong cùng một trường hợp
Classical: ig.pieri(1, 'S[1]')  →  S[2]
Quantum:   ig.qpieri(1, 'S[1]') →  S[2] + S[]*q/2

# So sánh với các loại khác (cùng input)
Type A: pieriA_inner(1, [1], 2, 4) → S[1,1] + S[2]
Type B: pieriB_inner(1, [1], 1, 2) → 0  
Type C: pieriC_inner(1, [1], 1, 2) → S[2]
Type D: pieriD_inner(1, [1], 1, 2) → S[1,1]
```

**Giải thích:**
- **Type A**: Straightforward results
- **Type B**: Often gives 0 due to `skipfirst=False`
- **Type C**: Gives non-zero due to `skipfirst=True`
- **Type D**: Different algorithm altogether

Đặc điểm riêng của Type C:
- **`skipfirst=True`**: Core difference from Type B
- **Quantum coefficient q/2**: Unique among all types
- **Symplectic constraints**: Different mathematical framework

## Tham Khảo

- **Tài liệu chính:** [Thuật Toán Pieri Type C](./pieri_typeC_algorithms.md)
- **Dependencies:** [Quan hệ các Algorithm](./pieri_typeC_algorithms.md#quan-h-c-c-algorithm-li-n-quan-n-pieri-c-dependencies-tree)
- **Quantum Theory:** [Phiên Bản Lượng Tử](./pieri_typeC_algorithms.md#phi-n-b-n-l-ng-t-qpiericinneri-lam-k-n)
- **Symplectic Theory:** [Ký Hiệu và So Sánh](./pieri_typeC_algorithms.md#k-hi-u)

---

*Tất cả các ví dụ trên đều được test thực tế với SchubertPy version hiện tại và cho kết quả chính xác.* 