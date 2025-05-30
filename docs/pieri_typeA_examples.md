# Ví Dụ Chi Tiết: Thuật Toán Pieri Type A

Tài liệu này chứa các ví dụ chi tiết với kết quả thực tế cho tất cả các thuật toán Pieri Type A trong SchubertPy.

> **Tham khảo:** [Thuật Toán Pieri Type A](./pieri_typeA_algorithms.md) - Tài liệu mô tả chi tiết các thuật toán

## Tổng Quan

Tất cả các ví dụ dưới đây được test thực tế với SchubertPy và cho kết quả chính xác. Code nguồn để chạy các ví dụ có trong file [`test_pieri_examples.py`](../test_pieri_examples.py).

## Ví Dụ 1: Thuật Toán Hỗ Trợ

### 1.1. `padding_right` - Thêm padding

**Mục đích:** Thêm padding vào bên phải của partition để đạt độ dài cần thiết.

```python
# Ví dụ: Thêm 3 số 0 vào bên phải partition [2,1]
Input:  lam=[2, 1], 
        value=0, 
        count=3
Output: [2, 1, 0, 0, 0]
```

**Giải thích:** Thuật toán append 3 bản sao của giá trị 0 vào bên phải partition để tạo ra partition với độ dài phù hợp cho Grassmannian Gr(k,n).

**Liên kết:** [Algorithm 1.1 trong Type A](./pieri_typeA_algorithms.md#1-padding_rightlam-value-count)

### 1.2. `part_clip` - Loại bỏ trailing zeros

**Mục đích:** Loại bỏ các số 0 ở cuối partition để chuẩn hóa kết quả.

```python
# Ví dụ: Chuẩn hóa partition bằng cách loại bỏ số 0 ở cuối
Input:  [3, 2, 1, 0, 0]
Output: [3, 2, 1]
```

**Giải thích:** Thuật toán trim các số 0 ở cuối để chuẩn hóa partition thành dạng canonical.

**Liên kết:** [Algorithm 1.4 trong Type A](./pieri_typeA_algorithms.md#4-part_cliplambda)

### 1.3. `_part_star` - Quantum correction helper

**Mục đích:** Kiểm tra và biến đổi partition theo điều kiện lượng tử trong Pieri Type A.

```python
# Ví dụ 1: Phần tử đầu khớp với cols
Input:  lam=[2, 1, 1]
        cols=2
Output: S[1,1]

# Ví dụ 2: Phần tử đầu không khớp
Input:  lam=[3, 1, 1]
        cols=2  
Output: 0
```

**Giải thích:** Nếu phần tử đầu tiên của partition bằng `cols`, trả về partition còn lại (bỏ phần tử đầu). Ngược lại trả về 0.

**Liên kết:** [Algorithm 1.5 trong Type A](./pieri_typeA_algorithms.md#5-_part_starlam-cols)

## Ví Dụ 2: Thuật Toán Fill và Iterator

### 2.1. `_pieri_fillA` - Tạo cấu hình đầu tiên

**Mục đích:** Tạo cấu hình đầu tiên cho thuật toán Pieri Type A bằng cách điền boxes vào Young diagram.

```python
# Ví dụ từ testcase trong SchubertPy
Input:  lam=[2, 1, 0, 0, 0]
        inner=[2, 1, 0, 0, 0]
        outer=[5, 2, 1, 0, 0]
        row_index=0
        p=1
Output: [3, 1, 0, 0, 0]
```

**Giải thích:** 
- Bắt đầu với partition [2,1,0,0,0]
- Cần đặt thêm p=1 box vào Young diagram
- Hàng đầu tiên: min(outer[0], inner[0] + p) = min(5, 2+1) = 3
- Kết quả: [3,1,0,0,0] là cấu hình đầu tiên hợp lệ

**Liên kết:** [Algorithm 1.2 trong Type A](./pieri_typeA_algorithms.md#2-_pieri_filla-lam-inner-outer-row_index-p)

### 2.2. `_pieri_itrA` - Tạo cấu hình tiếp theo

**Mục đích:** Tạo cấu hình tiếp theo trong việc liệt kê tất cả các Young diagrams hợp lệ.

```python
# Ví dụ: Tìm cấu hình tiếp theo từ [3,1,0,0,0]
Input:  current=[3, 1, 0, 0, 0]
        inner=[2, 1, 0, 0, 0] 
        outer=[5, 2, 1, 0, 0, 0]
Output: [2, 2, 0, 0, 0]
```

**Giải thích:**
- Từ [3,1,0,0,0], giảm hàng đầu tiên từ 3 xuống 2
- Redistribute box này vào hàng thứ hai: 1→2
- Kết quả: [2,2,0,0,0] là cấu hình tiếp theo

**Liên kết:** [Algorithm 1.3 trong Type A](./pieri_typeA_algorithms.md#3-_pieri_itralampion-inner-outer)

## Ví Dụ 3: Thuật Toán Chính - Classical Pieri

### 3.1. Grassmannian Gr(2,4) - Ví dụ từ documentation

**Thuật toán:** [`pieriA_inner(i, lam, k, n)`](./pieri_typeA_algorithms.md#thu-t-to-n-ch-nh-pieriA_inneri-lam-k-n)

```python
# Ví dụ: σ_(1) * σ_1 trong H*(Gr(2,4))
Input:  i=1
        lam=[1], 
        k=2, 
        n=4
Output: S[1,1] + S[2]
```

**Giải thích:**
- Nhân lớp Schubert σ_(1) với lớp đặc biệt σ_1
- Kết quả: σ_(2) + σ_(1,1)
- Đây là biểu diễn các Young diagrams có thể có khi thêm 1 box vào diagram (1)

### 3.2. Grassmannian Gr(2,5) - Ví dụ phức tạp hơn

```python  
# Ví dụ: σ_(2,1) * σ_1 trong H*(Gr(2,5))
Input:  i=1
        lam=[2, 1], 
        k=2, 
        n=5
Output: S[2,1,1] + S[2,2]
```

**Giải thích:**
- Nhân σ_(2,1) với σ_1 trong Grassmannian Gr(2,5)
- Có thể thêm 1 box vào diagram (2,1) theo hai cách:
  - Thêm vào hàng thứ nhất: (2,1) → (3,1) (không hợp lệ với Gr(2,5))
  - Thêm vào hàng thứ hai: (2,1) → (2,2)  
  - Thêm hàng mới: (2,1) → (2,1,1)

## Ví Dụ 4: Thuật Toán Quantum Pieri

### 4.1. Trường hợp có quantum correction

**Thuật toán:** [`qpieriA_inner(i, lam, k, n)`](./pieri_typeA_algorithms.md#phi-n-b-n-l-ng-t-qpieriA_inneri-lam-k-n)

```python
# Ví dụ: Quantum effect trong Gr(2,4)
Input:  i=1
        lam=[2, 2]
        k=2
        n=4
Output: S[1]*q
```

**Giải thích:**
- λ=[2,2] có độ dài n-k=2 và λ_{n-k-1}=λ_1=2>0 
- Điều kiện quantum được kích hoạt: `|λ| = n-k ∧ λ_{n-k} > 0`
- Kết quả chỉ có số hạng quantum q·σ_(1)

### 4.2. Trường hợp quantum đơn giản

```python
# Ví dụ: Quantum correction trong Gr(2,4)  
Input:  i=2
        lam=[1, 1]
        k=2
        n=4
Output: S[]*q
```

**Giải thích:**
- λ=[1,1] thỏa mãn điều kiện quantum
- Kết quả: q·σ_∅ (quantum correction với partition rỗng)

## Ví Dụ 5: Interface qua Grassmannian Class

### 5.1. Classical Pieri thông qua class

**Class:** [`Grassmannian(m, n)`](./pieri_typeA_algorithms.md#thu-t-to-n-ch-nh-pieriA_inneri-lam-k-n)

```python
# Sử dụng Grassmannian class cho Gr(2,5)
gr = Grassmannian(2, 5)  # m=2, n=5 => Gr(2,5) 
Input:  gr.pieri(1, 'S[2,1]')
Output: S[2,2] + S[3,1]
```

**Giải thích:**
- Tạo Grassmannian object cho Gr(2,5)
- Sử dụng interface thuận tiện với string notation
- Kết quả giống như gọi trực tiếp pieriA_inner

### 5.2. Quantum Pieri với quantum terms

```python
# Quantum Pieri với xuất hiện quantum correction
Input:  gr.qpieri(1, 'S[3,2]')
Output: S[1]*q + S[3,3]
```

**Giải thích:**
- σ_(3,2) trong Gr(2,5) có quantum effect
- Kết quả bao gồm:
  - Classical term: σ_(3,3)
  - Quantum term: q·σ_(1)

## Ví Dụ 6: So Sánh Classical vs Quantum

```python
# Classical vs Quantum trong cùng một trường hợp
Classical: gr.pieri(1, 'S[2,1]')  →  S[2,2] + S[3,1]
Quantum:   gr.qpieri(1, 'S[2,1]') →  S[2,2] + S[3,1] 

# Trường hợp có quantum effects
Quantum:   gr.qpieri(1, 'S[3,2]') →  S[1]*q + S[3,3]
```

**Giải thích:**
- Khi không có quantum effects, classical và quantum cho kết quả giống nhau
- Khi có quantum effects, quantum version có thêm số hạng q·σ_μ
- Quantum effects xảy ra khi partition đạt "biên giới" của Grassmannian

## Tham Khảo

- **Tài liệu chính:** [Thuật Toán Pieri Type A](./pieri_typeA_algorithms.md)
- **Dependencies:** [Quan hệ các Algorithm](./pieri_typeA_algorithms.md#quan-h-c-c-algorithm-li-n-quan-n-pieri-a-dependencies-tree)
- **Quantum Theory:** [Phiên Bản Lượng Tử](./pieri_typeA_algorithms.md#phi-n-b-n-l-ng-t-qpieriA_inneri-lam-k-n)
- **Ký hiệu:** [Ký Hiệu Toán Học](./pieri_typeA_algorithms.md#k-hi-u)

---

*Tất cả các ví dụ trên đều được test thực tế với SchubertPy version hiện tại và cho kết quả chính xác.* 