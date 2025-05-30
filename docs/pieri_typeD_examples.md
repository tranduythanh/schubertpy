# Ví Dụ Chi Tiết: Thuật Toán Pieri Type D

Tài liệu này chứa các ví dụ chi tiết với kết quả thực tế cho tất cả các thuật toán Pieri Type D trong SchubertPy.

> **Tham khảo:** [Thuật Toán Pieri Type D](./pieri_typeD_algorithms.md) - Tài liệu mô tả chi tiết các thuật toán

## Tổng Quan

Tất cả các ví dụ dưới đây được test thực tế với SchubertPy và cho kết quả chính xác. Code nguồn để chạy các ví dụ có trong file [`test_pieri_examples.py`](../test_pieri_examples.py).

Type D (Orthogonal Grassmannian Even) là loại phức tạp nhất với:
- **Unique `_dcoef` function**: Hệ số đặc biệt cho Type D
- **Complex partition generation**: Khác với Type B và C
- **Special orthogonal constraints**: Cho even dimensional spaces
- **Unique algorithm structure**: Khác hoàn toàn với Type A, B, C

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

### 1.2. `pieri_set` - Type D Set Generation

**Mục đích:** Type D sử dụng shared functions nhưng với parameters khác.

```python
# Ví dụ: Tạo set với d=1 parameter đặc trưng Type D
Input:  p=1
        lam=[1]
        k=1
        n=2
        d=1
Output: [[2], [1, 1]]
```

**Giải thích:** `d=1` parameter phân biệt Type D từ Type B/C (sử dụng `d=0`). Kết quả: Tương tự Type B/C nhưng computed với constraints khác nhau, cho more results.

**So sánh:**
- Type B/C: `d=0` → `[[2]]`
- Type D: `d=1` → `[[2], [1, 1]]` (more results)

**Liên kết:** [Algorithm 1.1 trong Type B](./pieri_typeB_algorithms.md#1-pieri_setp-lam-k-n-d)

### 1.3. `_dcoef` - Type D Coefficient Function

**Mục đích:** Tính toán hệ số đặc biệt cho Type D algorithms.

```python
# Ví dụ: Tính hệ số Type D
Input:  p=1
        lam1=[1]
        lam2=[2]
        k=1
        d=1
        n=2
Output: 0
```

**Giải thích:** Type D specific coefficient calculation. Complex calculation involving orthogonal constraints for even dimensions. Pattern: `_dcoef` thường trả về 0 trong nhiều cases, phản ánh complexity của Type D.

**Liên kết:** [Algorithm 1.1 trong Type D](./pieri_typeD_algorithms.md#1-_dcoeflam-mu-tlam-k-n)

## Ví Dụ 2: Thuật Toán Fill và Iterator

### 2.1. `count_comps` - Type D Component Counting

**Mục đích:** Type D sử dụng different parameters trong shared functions.

```python
# Ví dụ: Đếm components với Type D parameters
Input:  lam1=[1]
        lam2=[2]
        skipfirst=False
        k=1
        d=1
Output: 0
```

**Giải thích:** Type D sử dụng `d=1` parameter khác với Type B/C. Kết quả khác biệt đáng kể so với các loại khác.

**So sánh:**
- Type B: `d=0, skipfirst=False` → `1`
- Type C: `d=0, skipfirst=True` → `0`
- Type D: `d=1, skipfirst=False` → `0`

**Liên kết:** [Algorithm 1.2 trong Type B](./pieri_typeB_algorithms.md#2-count_compslam1-lam2-skipfirst-k-d)

### 2.2. Shared Infrastructure với parameters khác

**Mục đích:** Type D reuses shared functions nhưng với Type D specific parameters.

```python
# Ví dụ: Type D uses same functions with d=1
Input:  All shared functions use d=1 instead of d=0
Output: Different behavior due to d parameter
```

**Giải thích:** Type D không có fill/iterator riêng biệt nhưng sử dụng shared infrastructure với `d=1` parameter. Điều này tạo ra behavior pattern khác biệt với Type B/C.

**Liên kết:** [Helper Functions trong Type B](./pieri_typeB_algorithms.md#thu-t-to-n-h-tr)

## Ví Dụ 3: Thuật Toán Chính - Classical Pieri

### 3.1. OG(1,6) - Ví dụ từ documentation

**Thuật toán:** [`pieriD_inner(p, lam, k, n)`](./pieri_typeD_algorithms.md#thu-t-to-n-ch-nh-pieridinner-lam-k-n)

```python
# Ví dụ: σ_[1] * σ_1 trong H*(OG(1,6))
Input:  p=1
        lam=[1]
        k=1
        n=2
Output: S[1,1]
```

**Giải thích:**
- Nhân lớp Schubert σ_[1] với lớp đặc biệt σ_1
- Context: Orthogonal Grassmannian cho even dimensions
- Sử dụng unique Type D coefficient calculations via `_dcoef`
- Kết quả: S[1,1] (clean result)

### 3.2. So sánh với Type B (Orthogonal Odd)

```python
# Ví dụ: Cùng input, algorithms khác nhau
Type B: pieriB_inner(1, [1], 1, 2) → 0
Type D: pieriD_inner(1, [1], 1, 2) → S[1,1]
```

**Giải thích:**
- **Type B**: Orthogonal odd dimensions → often gives 0
- **Type D**: Orthogonal even dimensions → gives clean result
- **Algorithm**: Completely different coefficient calculations
- **Mathematical framework**: Even vs odd orthogonal groups

## Ví Dụ 4: Thuật Toán Quantum Pieri

### 4.1. Trường hợp có quantum correction

**Thuật toán:** [`qpieriD_inner(p, lam, k, n)`](./pieri_typeD_algorithms.md#phi-n-b-n-l-ng-t-qpieridinner-lam-k-n)

```python
# Ví dụ: Quantum effect trong OG(1,6)
Input:  p=1
        lam=[1]
        k=1
        n=2
Output: S[1,1]
```

**Giải thích:**
- λ=[1] với Type D quantum corrections
- Quantum behavior: Type D specific quantum framework
- Kết quả: S[1,1] (same as classical in this case)
- Quantum = classical, indicating no quantum corrections for this input

### 4.2. Đặc điểm Type D quantum

**Đặc điểm riêng biệt:**
- **Same as classical**: In many cases, quantum = classical for Type D
- **Unique quantum corrections**: When they occur, specific to even orthogonal
- **Different from Type B**: Even vs odd quantum behavior

```python
# Ví dụ: So sánh Classical vs Quantum
Classical: pieriD_inner(1, [1], 1, 2) → S[1,1]
Quantum:   qpieriD_inner(1, [1], 1, 2) → S[1,1]
```

**Giải thích:** Type D quantum behavior thường simpler than Type B. Trong nhiều cases, quantum corrections không xuất hiện hoặc minimal impact.

## Ví Dụ 5: Interface qua OrthogonalGrassmannian Class

### 5.1. Classical Pieri thông qua class

**Class:** [`OrthogonalGrassmannian(m, n)`](./pieri_typeD_algorithms.md#class-interface)

```python
# Sử dụng OrthogonalGrassmannian class cho OG(1,6)
og = OrthogonalGrassmannian(1, 4)  # m=1, n=4 => OG(1,6) -> Type D
Input:  og.pieri(1, 'S[1]')
Output: S[1,1]
```

**Giải thích:**
- Tạo OrthogonalGrassmannian object cho OG(1,6)
- Even dimension tự động chọn Type D (vs odd → Type B)
- Type D specific behavior thông qua class
- Kết quả giống như gọi trực tiếp pieriD_inner

### 5.2. Quantum Pieri với quantum terms

```python
# Quantum Pieri với Type D behavior
Input:  og.qpieri(1, 'S[1]')
Output: S[1,1]
```

**Giải thích:**
- σ_[1] trong OG(1,6) với Type D quantum
- Quantum Pieri gives same result as classical
- Type D quantum behavior is often simpler than Type B
- No complex quantum corrections in this case

## Ví Dụ 6: So Sánh Classical vs Quantum

```python
# Classical vs Quantum trong cùng một trường hợp
Classical: og.pieri(1, 'S[1]')  →  S[1,1]
Quantum:   og.qpieri(1, 'S[1]') →  S[1,1]

# So sánh toàn bộ hệ thống (cùng input)
Type A: pieriA_inner(1, [1], 2, 4) → S[1,1] + S[2]
Type B: pieriB_inner(1, [1], 1, 2) → 0
Type C: pieriC_inner(1, [1], 1, 2) → S[2]
Type D: pieriD_inner(1, [1], 1, 2) → S[1,1]
```

**Giải thích:**
- **Type A**: Most predictable, clean results
- **Type B**: Often gives 0 due to complex constraints
- **Type C**: Non-zero due to `skipfirst=True`
- **Type D**: Clean result, different algorithm entirely

Đặc điểm riêng của Type D:
- **`_dcoef` function**: Unique coefficient calculation
- **`d=1` parameter**: In pieri_set and related functions
- **Even orthogonal**: Mathematical framework for even dimensions
- **Algorithm independence**: Completely different from Type A, B, C

## Tham Khảo

- **Tài liệu chính:** [Thuật Toán Pieri Type D](./pieri_typeD_algorithms.md)
- **Dependencies:** [Quan hệ các Algorithm](./pieri_typeD_algorithms.md#quan-h-c-c-algorithm-li-n-quan-n-pieri-d-dependencies-tree)
- **Quantum Theory:** [Phiên Bản Lượng Tử](./pieri_typeD_algorithms.md#phi-n-b-n-l-ng-t-qpieridinner-lam-k-n)
- **Orthogonal Theory:** [Helper Functions đặc biệt](./pieri_typeD_algorithms.md#thu-t-to-n-h-tr)

---

*Tất cả các ví dụ trên đều được test thực tế với SchubertPy version hiện tại và cho kết quả chính xác.* 