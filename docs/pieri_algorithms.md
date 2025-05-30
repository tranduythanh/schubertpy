# Thuật Toán Pieri cho các Grassmannian

Tài liệu này cung cấp tổng quan về các thuật toán quy tắc Pieri được triển khai trong SchubertPy cho các loại Grassmannian khác nhau.

## Tổng Quan

Quy tắc Pieri là thuật toán cơ bản trong phép tính Schubert, mô tả cách nhân một lớp Schubert với một lớp Schubert đặc biệt (tương ứng với hàng đơn trong biểu đồ Young). 

### Cấu Trúc Chung

Tất cả thuật toán Pieri đều có cấu trúc tương tự:
1. **Sinh tập partitions hợp lệ**: Tìm tất cả các partition $\mu$ có thể thu được từ $\lambda$ bằng cách thêm $p$ boxes
2. **Tính hệ số**: Mỗi partition có hệ số riêng dựa trên connected components
3. **Trả về tổ hợp tuyến tính**: $\sum a_\mu \sigma_\mu$

## Các Loại Grassmannian

### Type A: Grassmannian Thông Thường Gr(k,n)
- **File chi tiết**: [`pieri_typeA_algorithms.md`](pieri_typeA_algorithms.md)
- **Thuật toán chính**: `pieriA`, `qpieriA`
  - **`pieriA_inner`**: [Type A Algorithm 1](pieri_typeA_algorithms.md#thuật-toán-chính-pieria_inneri-lam-k-n)
  - **`qpieriA_inner`**: [Type A Quantum](pieri_typeA_algorithms.md#phiên-bản-lượng-tử-qpieria_inneri-lam-k-n)
- **Đặc điểm**: Đơn giản nhất, không có connected components

### Type B: Grassmannian Trực Giao Lẻ OG(k,2n+1)
- **File chi tiết**: [`pieri_typeB_algorithms.md`](pieri_typeB_algorithms.md)  
- **Thuật toán chính**: `pieriB`, `qpieriB`
  - **`pieriB_inner`**: [Type B Algorithm 1](pieri_typeB_algorithms.md#thuật-toán-chính-pierib_innerp-lam-k-n)
  - **`qpieriB_inner`**: [Type B Quantum](pieri_typeB_algorithms.md#phiên-bản-lượng-tử-qpierib_innerp-lam-k-n)
- **Đặc điểm**: Hệ số dạng 2^(c-b), có offset b phụ thuộc vào p và k

### Type C: Grassmannian Symplectic IG(k,2n)
- **File chi tiết**: [`pieri_typeC_algorithms.md`](pieri_typeC_algorithms.md)
- **Thuật toán chính**: `pieriC`, `qpieriC`
  - **`pieriC_inner`**: [Type C Algorithm 1](pieri_typeC_algorithms.md#thuật-toán-chính-pieric_inneri-lam-k-n)
  - **`qpieriC_inner`**: [Type C Quantum](pieri_typeC_algorithms.md#phiên-bản-lượng-tử-qpieric_inneri-lam-k-n)
- **Đặc điểm**: Hệ số dạng 2^c, có skipfirst=true khi đếm components

### Type D: Grassmannian Trực Giao Chẵn OG(k,2n)
- **File chi tiết**: [`pieri_typeD_algorithms.md`](pieri_typeD_algorithms.md)
- **Thuật toán chính**: `pieriD`, `qpieriD`
  - **`pieriD_inner`**: [Type D Algorithm 1](pieri_typeD_algorithms.md#thuật-toán-chính-pierid_innerp-lam-k-n)
  - **`qpieriD_inner`**: [Type D Quantum](pieri_typeD_algorithms.md#phiên-bản-lượng-tử-qpierid_innerp-lam-k-n)
- **Đặc điểm**: Phức tạp nhất, hệ số phụ thuộc vào Schubert type và dấu của p

## Thuật Toán Hỗ Trợ Cốt Lõi

### 1. Sinh Tập Partition: `pieri_set(p, lam, k, n, d)`
Chuyển đổi partition thành cặp (top, bot), sinh các partition hợp lệ, rồi chuyển ngược lại.
- **Chi tiết**: [Type B Algorithm 1.1](pieri_typeB_algorithms.md#1-pieri_setp-lam-k-n-d)

### 2. Đếm Connected Components: `count_comps(lam1, lam2, skipfirst, k, d)`
Tính toán dựa trên phương pháp cặp partition và mảng components.
- **Chi tiết**: [Type B Algorithm 1.2](pieri_typeB_algorithms.md#2-count_compslam1-lam2-skipfirst-k-d)

### 3. Chuyển Đổi Partition-Pair: `part2pair`, `pair2part`
```
part2pair: $\lambda$ $\rightarrow$ (top, bot)
pair2part: (top, bot) $\rightarrow$ $\lambda$
```
Phép biến đổi cơ bản giữa partition và cặp partition.

### 4. Các Phép Toán Partition
- **`part_conj(lam)`**: Conjugate partition (phép đối xứng qua đường chéo)
  - **Chi tiết**: [Type B Algorithm 1.6](pieri_typeB_algorithms.md#6-part_conjlam)
- **`part_star(lam, cols)`**: Phép toán star $\lambda*$ = (cols-$\lambda_n$, ..., cols-$\lambda_1$)
  - **Chi tiết**: [Type A Algorithm 1.5](pieri_typeA_algorithms.md#5-_part_starlam-cols)
- **`part_tilde(lam, rows, cols)`**: Phép toán tilde phức tạp hơn
  - **Chi tiết**: [Type B Algorithm 1.8](pieri_typeB_algorithms.md#8-_part_tildelam-rows-cols)
- **`part_clip(lam)`**: Loại bỏ các số 0 ở cuối partition
  - **Chi tiết**: [Type A Algorithm 1.4](pieri_typeA_algorithms.md#4-part_cliplambda)
- **`remove_rim_hooks(lam, rim_size, acceptable_grid)`**: Loại bỏ các rim hook kích thước cố định khỏi partition để phù hợp với lưới cho trước, trả về partition mới, số rim hook đã loại và tổng chiều cao rim hook đã loại.
  - **Mô tả**: Xem chi tiết bên dưới.

### Thuật toán: remove_rim_hooks

```python
Input: λ = (λ₁, ..., λₗ) ∈ Partition, rim_size ∈ ℕ, acceptable_grid = (nrow, ncol)
Output: (λ', num_rim_hooks, total_height)

1: Nếu λ rỗng hoặc rim_size ≤ 0, trả về (λ, 0, 0)
2: Đặt current_partition ← λ, total_rim_hooks_removed ← 0
3: Lặp:
    a. Tìm rim hook kích thước rim_size có thể loại khỏi current_partition
    b. Nếu tìm được:
        - Loại rim hook đó khỏi current_partition
        - total_rim_hooks_removed += 1
        - Nếu partition mới phù hợp với acceptable_grid, trả về (partition mới, total_rim_hooks_removed, tổng chiều cao)
        - Nếu không còn thay đổi, trả về (∅, total_rim_hooks_removed, tổng chiều cao)
        - Cập nhật current_partition
    c. Nếu không tìm được rim hook phù hợp, trả về (0, 0, 0)
```

- **Ý nghĩa toán học:** Thuật toán này dùng trong các quy tắc quantum để đưa partition về dạng phù hợp với lưới (grid) cho trước bằng cách loại bỏ các rim hook kích thước cố định.
- **Ứng dụng:** Quantum Pieri, kiểm tra tính hợp lệ của partition sau khi loại rim hook.

### 5. Thuật Toán Điền và Lặp
- **`_pieri_fillA(lam, inner, outer, row_index, p)`**: Điền boxes cho Type A
  - **Chi tiết**: [Type A Algorithm 1.2](pieri_typeA_algorithms.md#2-_pieri_fillamlam-inner-outer-row_index-p)
- **`_pieri_itrA(lam, inner, outer)`**: Iterator cho Type A
  - **Chi tiết**: [Type A Algorithm 1.3](pieri_typeA_algorithms.md#3-_pieri_itraliam-inner-outer)
- **`_pieri_fill(lam, inner, outer, r, p)`**: Điền boxes cho Type B/C/D
  - **Chi tiết**: [Type B Algorithm 1.3](pieri_typeB_algorithms.md#3-_pieri_filllam-inner-outer-r-p)
- **`_pieri_itr(lam, inner, outer)`**: Iterator cho Type B/C/D
  - **Chi tiết**: [Type B Algorithm 1.4](pieri_typeB_algorithms.md#4-_pieri_itrlam-inner-outer)

### 6. Thuật Toán Đặc Biệt Type D
- **`_dcoef(p, lam, mu, tlam, k, n)`**: Hệ số phức tạp với tie-breaking
  - **Chi tiết**: [Type D Algorithm 1.1](pieri_typeD_algorithms.md#1-_dcoefp-lam-mu-tlam-k-n)
- **`dualize`**: Phép dualization (chỉ dùng trong quantum k=1)
  - **Chi tiết**: [Type D Algorithm 1.6](pieri_typeD_algorithms.md#6-dualizelc)
  - **Sử dụng**: [Line 23 trong Quantum Algorithm](pieri_typeD_algorithms.md#phiên-bản-lượng-tử-qpierid_innerp-lam-k-n)
- **`type_swap`**: Phép type swapping (chỉ dùng trong quantum k>1)  
  - **Chi tiết**: [Type D Algorithm 1.7](pieri_typeD_algorithms.md#7-type_swaplc-k)
  - **Sử dụng**: [Line 33 trong Quantum Algorithm](pieri_typeD_algorithms.md#phiên-bản-lượng-tử-qpierid_innerp-lam-k-n)
- **`_toSchurFromIntnMu`**: Transform với complement sets (chỉ dùng trong quantum k=1)
  - **Chi tiết**: [Type D Algorithm 1.8](pieri_typeD_algorithms.md#8-quantum-helper-_toschufromintnmu)

### 7. Phép Toán Common
- **`part_conj(lam)`**: Conjugate partition
  - **Sử dụng**: Trong `pieri_set` và `count_comps` của Type B/C/D

## Quantum Pieri Rules

Các quy tắc lượng tử mở rộng quy tắc cổ điển bằng cách thêm các số hạng có tham số q:

$$
QH*(X) = H*(X)[q] / \text{(quan hệ lượng tử)}
$$

Mỗi loại có điều kiện lượng tử riêng:
- **Type A**: Đơn giản nhất, chỉ một điều kiện
- **Type B**: Hai điều kiện phụ thuộc vào k=0 hay k>0  
- **Type C**: Một điều kiện với hệ số q/2
- **Type D**: Hai điều kiện phức tạp

## Ký Hiệu

- **$\sigma_\mu$**: Lớp Schubert cho partition $\mu$
- **q**: Tham số lượng tử
- **H*(X)**: Cohomology ring
- **QH*(X)**: Quantum cohomology ring
- **$\lambda \subseteq \mu$**: $\mu$ chứa $\lambda$ (componentwise $\leq$)
- **$|\lambda|$**: Số hàng của partition $\lambda$
- **$\lambda[i:]$**: Partition con từ phần tử thứ i
- **$\emptyset$**: Partition rỗng

## Tổng Kết Các Phép Toán và Link References

### Thuật Toán Chính theo Type
| Type | Classical | Quantum |
|------|-----------|---------|
| **A** | [`pieriA_inner`](pieri_typeA_algorithms.md#thuật-toán-chính-pieria_inneri-lam-k-n) | [`qpieriA_inner`](pieri_typeA_algorithms.md#phiên-bản-lượng-tử-qpieria_inneri-lam-k-n) |
| **B** | [`pieriB_inner`](pieri_typeB_algorithms.md#thuật-toán-chính-pierib_innerp-lam-k-n) | [`qpieriB_inner`](pieri_typeB_algorithms.md#phiên-bản-lượng-tử-qpierib_innerp-lam-k-n) |
| **C** | [`pieriC_inner`](pieri_typeC_algorithms.md#thuật-toán-chính-pieric_inneri-lam-k-n) | [`qpieriC_inner`](pieri_typeC_algorithms.md#phiên-bản-lượng-tử-qpieric_inneri-lam-k-n) |
| **D** | [`pieriD_inner`](pieri_typeD_algorithms.md#thuật-toán-chính-pierid_innerp-lam-k-n) | [`qpieriD_inner`](pieri_typeD_algorithms.md#phiên-bản-lượng-tử-qpierid_innerp-lam-k-n) |

### Phép Toán Partition cơ bản
| Operation | Link | Description |
|-----------|------|-------------|
| `part_conj` | [Type B Algorithm 1.6](pieri_typeB_algorithms.md#6-part_conjlam) | Conjugate partition |
| `part_star` | [Type A Algorithm 1.5](pieri_typeA_algorithms.md#5-_part_starlam-cols) | Star operation $\lambda*$ |
| `part_tilde` | [Type B Algorithm 1.8](pieri_typeB_algorithms.md#8-_part_tildelam-rows-cols) | Tilde operation |
| `part_clip` | [Type A Algorithm 1.4](pieri_typeA_algorithms.md#4-part_cliplambda) | Trim trailing zeros |

### Thuật Toán Hỗ Trợ Cốt Lõi
| Function | Link | Used in Types |
|----------|------|---------------|
| `pieri_set` | [Type B Algorithm 1.1](pieri_typeB_algorithms.md#1-pieri_setp-lam-k-n-d) | B, C, D |
| `count_comps` | [Type B Algorithm 1.2](pieri_typeB_algorithms.md#2-count_compslam1-lam2-skipfirst-k-d) | B, C, D |
| `_pieri_fillA` | [Type A Algorithm 1.2](pieri_typeA_algorithms.md#2-_pieri_fillamlam-inner-outer-row_index-p) | A only |
| `_pieri_itrA` | [Type A Algorithm 1.3](pieri_typeA_algorithms.md#3-_pieri_itraliam-inner-outer) | A only |
| `_pieri_fill` | [Type B Algorithm 1.3](pieri_typeB_algorithms.md#3-_pieri_filllam-inner-outer-r-p) | B, C, D |
| `_pieri_itr` | [Type B Algorithm 1.4](pieri_typeB_algorithms.md#4-_pieri_itrlam-inner-outer) | B, C, D |
| `_dcoef` | [Type D Algorithm 1.1](pieri_typeD_algorithms.md#1-_dcoefp-lam-mu-tlam-k-n) | D only |

### Helper Functions theo Type
| Type | Specific Functions | General Functions |
|------|-------------------|-------------------|
| **A** | `padding_right`, `_pieri_fillA`, `_pieri_itrA` | `part_conj`, `part_clip`, `part_star` |
| **B** | `_part_tilde` | `pieri_set`, `count_comps`, `_pieri_fill`, `_pieri_itr`, `part_conj` |
| **C** | *(none unique)* | Same as Type B |
| **D** | `_dcoef`, `dualize` (Q k=1), `type_swap` (Q k>1), `_toSchurFromIntnMu` (Q k=1) | Same as Type B |

**Ghi chú:**
- **Q k=1, Q k>1**: Chỉ sử dụng trong quantum algorithms với điều kiện k cụ thể
- **`part_conj`**: Được sử dụng trong `pieri_set` và `count_comps` của Type B/C/D
- **`dualize`, `type_swap`**: Là các operations đặc biệt chỉ có trong Type D quantum

## Tham Khảo

- **Lý thuyết**: Fulton & Pragacz, "Schubert varieties and degeneracy loci"
- **Giambelli Rules**: [`giambelli_algorithms.md`](giambelli_algorithms.md) - Thuật toán biểu diễn general Schubert classes
- **Triển khai**: Xem các file chi tiết cho từng type
- **Ví dụ**: Test cases trong thư mục `tests/`

## Ý Nghĩa Hình học

**Grassmannian Trực Giao Chẵn OG(k,2n+2):**
- Không gian các k-dimensional isotropic subspaces trong $\mathbb{C}^{2n+2}$
- Cấu trúc trực giao chẵn tạo ra complexity đặc biệt
- Type D có đặc điểm đặc biệt về spinor representations

## Giambelli Rules

Ngoài các quy tắc Pieri, SchubertPy còn triển khai quy tắc Giambelli - thuật toán để biểu diễn bất kỳ lớp Schubert nào dưới dạng polynomial của các lớp Schubert đặc biệt:

- **File chi tiết**: [`giambelli_algorithms.md`](giambelli_algorithms.md)
- **Thuật toán chính**: `giambelli`, `qgiambelli`
- **Đặc điểm**: Sử dụng các quy tắc Pieri làm building blocks cho thuật toán đệ quy
- **Ứng dụng**: Tính toán multiplication `mult(lc1, lc2)` và conversion `toS(lc)`

### Mối quan hệ với Pieri Rules

| Thuật toán | Input | Output | Sử dụng |
|------------|-------|--------|---------|
| **Pieri** | Partition + số | Linear combination | Multiplication với special classes |
| **Giambelli** | Bất kỳ Schubert class | Polynomial của special classes | Universal representation |

## Ký Hiệu

- **$\sigma_\mu$**: Lớp Schubert cho partition $\mu$
- **q, q1, q2**: Các tham số lượng tử
- **cc**: Connected components count
- **tlam**: Type parameter (0, 1, hoặc 2)
- **OG(k,2n+2)**: Grassmannian trực giao chẵn
- **QH*(OG(k,2n+2))**: Quantum cohomology ring của OG(k,2n+2)
- **h**: Tie-breaking value

## Quantum Schubert Class Calculation using `remove_rim_hooks`

**Python function:** `grassmannian.quantum_schubert_class`

**Pseudocode:**

```python
# Input: Partition lambda, quantum grid size n, quantum parameter q
# Output: Quantum Schubert class sigma_lambda in QH^*(Gr(k,n))
result = 0
for mu in all_partitions_fitting_in_k_by_n_minus_k_grid():
    nu, q_power, sign = remove_rim_hooks(lambda, n)
    if nu fits in k x (n-k) grid:
        result += sign * q**q_power * sigma_nu
return result
```

This algorithm computes the quantum Schubert class by reducing the partition using `remove_rim_hooks`, determining the quantum power and sign, and summing over all valid resulting partitions.