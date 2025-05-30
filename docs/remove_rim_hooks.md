# Thuật toán Remove Rim Hooks (`remove_rim_hooks`)

## Mô tả
Thuật toán loại bỏ các rim hook kích thước cố định khỏi một partition để phù hợp với lưới cho trước. Được sử dụng trong tính toán lớp Schubert lượng tử.

### Đầu vào
- `lambda`: Partition $(\lambda_1, ..., \lambda_l)$
- `rim_size`: Kích thước rim hook (số nguyên dương)
- `acceptable_grid`: Lưới hợp lệ $(nrow, ncol)$

### Đầu ra
- Partition mới $\lambda'$
- Số rim hook đã loại $num\_rim\_hooks$
- Tổng chiều cao rim hook đã loại $total\_height$

### Thuật toán
```
Algorithm: Remove Rim Hooks (remove_rim_hooks)
Input: λ = (λ₁, ..., λₗ), rim_size ∈ ℕ, acceptable_grid = (nrow, ncol)
Output: (λ', num_rim_hooks, total_height)

1: if λ = ∅ or rim_size ≤ 0 then
2:     return (λ, 0, 0)
3: end if
4: current_partition ← λ
5: num_rim_hooks ← 0
6: total_height ← 0
7: while True do
8:     rim_hook ← tìm rim hook kích thước rim_size có thể loại khỏi current_partition
9:     if rim_hook tồn tại then
10:        current_partition ← loại rim hook khỏi current_partition
11:        num_rim_hooks ← num_rim_hooks + 1
12:        total_height ← total_height + chiều cao rim_hook
13:        if current_partition phù hợp với acceptable_grid then
14:            return (current_partition, num_rim_hooks, total_height)
15:        end if
16:        if không còn thay đổi then
17:            return (∅, num_rim_hooks, total_height)
18:        end if
19:    else
20:        return (0, 0, 0)
21:    end if
22: end while
```

---

# Thuật toán Quantum Schubert với Rim Hook Removal

## Mô tả
Tính lớp Schubert lượng tử bằng cách loại bỏ rim hook khỏi partition cho đến khi phù hợp với lưới quantum.

### Đầu vào
- `lambda`: Partition
- `n, k`: Tham số Grassmannian

### Đầu ra
- Biểu thức Schubert lượng tử $QH^*(Gr(k,n))$

### Thuật toán
```
Algorithm: Quantum Schubert Class Calculation via Rim Hook Removal
Input: λ, n, k
Output: Quantum Schubert class in QH^*(Gr(k,n))

1: acceptable_grid ← (n-k, k)
2: rim_size ← n
3: if λ nằm trong acceptable_grid then
4:     return σ_λ
5: end if
6: (λ', q_num, height) ← remove_rim_hooks(λ, rim_size, acceptable_grid)
7: sign ← (−1)^{height−kq_num}
8: if q_num > 0 then
9:     return σ_{λ'} · q^{q_num} · sign
10: elif λ' = ∅ then
11:     return 0
12: else
13:     return σ_{λ'} · sign
14: end if
```
