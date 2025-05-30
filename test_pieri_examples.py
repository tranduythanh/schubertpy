#!/usr/bin/env python3
"""
Test examples for Pieri Type A, Type B, Type C, and Type D algorithms in SchubertPy
This script demonstrates each algorithm with representative examples

Type A Examples:
- Helper functions (padding_right, part_clip, _part_star)
- Fill and iterator (_pieri_fillA, _pieri_itrA)  
- Main algorithms (pieriA_inner, qpieriA_inner)
- Grassmannian class interface

Type B Examples (from pieri_typeB_algorithms.md):
- Helper functions (part_conj, _part_tilde, _part_star)
- Set generation (pieri_set, count_comps)
- Fill and iterator (_pieri_fill, _pieri_itr) 
- Main algorithms (pieriB_inner, qpieriB_inner)
- OrthogonalGrassmannian class interface
- Comparison with Type A

Type C Examples (from pieri_typeC_algorithms.md):
- Helper functions (_part_star, count_comps with skipfirst=true)
- Set generation (pieri_set - same as Type B)
- Main algorithms (pieriC_inner, qpieriC_inner)
- IsotropicGrassmannian class interface
- Comparison with Type A and Type B

Type D Examples (from pieri_typeD_algorithms.md):
- Helper functions (_dcoef, pieri_set with d=1, count_comps with d=1)
- Special functions (dualize, type_swap, _toSchurFromIntnMu)
- Main algorithms (pieriD_inner, qpieriD_inner)
- OrthogonalGrassmannian class interface (even dimension)
- Comparison with Type A, Type B, and Type C
"""

# Add the schubertpy directory to path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'schubertpy'))

from schubertpy.grassmannian import Grassmannian
from schubertpy.qcalc import (
    pieriA_inner, qpieriA_inner, 
    _pieri_fillA, _pieri_itrA, 
    padding_right, part_clip, _part_star,
    # Adding Type B imports
    pieriB_inner, qpieriB_inner,
    pieri_set, count_comps,
    part_conj, _part_tilde, _pieri_fill, _pieri_itr,
    # Adding Type C imports
    pieriC_inner, qpieriC_inner,
    # Adding Type D imports  
    pieriD_inner, qpieriD_inner, _dcoef
)
from schubertpy.orthogonal_grassmannian import OrthogonalGrassmannian
from schubertpy.isotropic_grassmannian import IsotropicGrassmannian
from schubertpy.utils.mix import padding_right as padding_right_util

def print_separator(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def demonstrate_shared_helper_functions():
    """Demonstrate helper functions shared across multiple types"""
    print_separator("SHARED HELPER FUNCTIONS EXAMPLES")
    
    # 1. _part_star - Used by Type A, B, C, D quantum corrections
    print("\n1. _part_star(lam, cols) - Universal Quantum Correction Helper")
    print("   Purpose: Check first element equals cols, return rest if true")
    print("   Usage: Type A, B, C, D quantum algorithms")
    
    # Comprehensive example showing different behaviors
    lam1 = [3, 1, 1]
    cols1 = 3
    result1 = _part_star(lam1, cols1)
    print(f"   Example 1: lam={lam1}, cols={cols1} → {result1} (head matches)")
    
    lam2 = [2, 1, 1] 
    cols2 = 3
    result2 = _part_star(lam2, cols2)
    print(f"   Example 2: lam={lam2}, cols={cols2} → {result2} (head doesn't match)")
    print("   Algorithm: Return S[tail] if head equals cols, else 0")
    
    # 2. pieri_set with different d parameters 
    print("\n2. pieri_set(p, lam, k, n, d) - Partition Set Generation")
    print("   Purpose: Generate all valid partitions for Pieri rules")
    print("   Key difference: d parameter varies by type")
    
    p, lam, k, n = 1, [1], 1, 2
    
    # Type B, C use d=0
    result_BC = pieri_set(p, lam, k, n, 0)
    print(f"   Type B/C (d=0): pieri_set({p}, {lam}, {k}, {n}, 0) → {result_BC}")
    
    # Type D uses d=1 
    result_D = pieri_set(p, lam, k, n, 1)
    print(f"   Type D   (d=1): pieri_set({p}, {lam}, {k}, {n}, 1) → {result_D}")
    
    print("   Algorithm: PR pairs + complex bounds, d affects component counting")
    
    # 3. count_comps with different parameters
    print("\n3. count_comps(lam1, lam2, skipfirst, k, d) - Component Counting")
    print("   Purpose: Count connected components between partitions")
    print("   Key differences: skipfirst and d parameters vary by type")
    
    lam1, lam2 = [1], [2]
    k, d = 1, 0
    
    # Show all type variations
    result_B = count_comps(lam1, lam2, False, k, 0)  # Type B
    result_C = count_comps(lam1, lam2, True, k, 0)   # Type C  
    result_D = count_comps(lam1, lam2, False, k, 1)  # Type D
    
    print(f"   Type B (skipfirst=False, d=0): {result_B}")
    print(f"   Type C (skipfirst=True,  d=0): {result_C}")
    print(f"   Type D (skipfirst=False, d=1): {result_D}")
    print("   Result: Type C typically gives smaller counts due to skipfirst=True")

def demonstrate_helper_functions():
    """Demonstrate Type A specific helper functions"""
    print_separator("TYPE A SPECIFIC HELPER FUNCTIONS")
    
    # 1. padding_right example
    print("\n1. padding_right(lam, value, count)")
    print("   Purpose: Add padding to the right of a partition")
    
    lam = [2, 1]
    value = 0
    count = 3
    result = padding_right(lam, value, count)
    print(f"   Input:  lam={lam}, value={value}, count={count}")
    print(f"   Output: {result}")
    print(f"   Algorithm: Append {count} copies of {value} to the right")
    
    # 2. part_clip example  
    print("\n2. part_clip(lambda)")
    print("   Purpose: Remove trailing zeros from partition")
    
    lambda_list = [3, 2, 1, 0, 0]
    result = part_clip(lambda_list)
    print(f"   Input:  {lambda_list}")
    print(f"   Output: {result}")
    print("   Algorithm: Trim trailing zeros")

def demonstrate_pieri_fill_and_itr():
    """Demonstrate _pieri_fillA and _pieri_itrA with examples from testcases"""
    print_separator("PIERI FILL AND ITERATOR EXAMPLES")
    
    # Example from test_piery.py
    print("\n4. _pieri_fillA(lam, inner, outer, row_index, p)")
    print("   Purpose: Create first configuration for Pieri Type A")
    
    lam = [2, 1, 0, 0, 0]
    inner = [2, 1, 0, 0, 0]
    outer = [5, 2, 1, 0, 0]
    row_index = 0
    p = 1
    
    result = _pieri_fillA(lam, inner, outer, row_index, p)
    print(f"   Input:  lam={lam}")
    print(f"           inner={inner}")
    print(f"           outer={outer}")
    print(f"           row_index={row_index}, p={p}")
    print(f"   Output: {result}")
    print("   Algorithm: Fill boxes respecting outer bounds and row constraints")
    
    # Iterator example
    print("\n5. _pieri_itrA(lam, inner, outer)")
    print("   Purpose: Generate next configuration in iteration")
    
    current_config = [3, 1, 0, 0, 0]
    inner = [2, 1, 0, 0, 0]
    outer = [5, 2, 1, 0, 0, 0]
    
    result = _pieri_itrA(current_config, inner, outer)
    print(f"   Input:  current={current_config}")
    print(f"           inner={inner}")
    print(f"           outer={outer}")
    print(f"   Output: {result}")
    print("   Algorithm: Decrease rightmost possible box and refill")

def demonstrate_main_algorithms():
    """Demonstrate main pieriA_inner and qpieriA_inner algorithms"""
    print_separator("MAIN ALGORITHMS EXAMPLES")
    
    # Classical Pieri example from test cases
    print("\n6. pieriA_inner(i, lam, k, n) - Classical Pieri")
    print("   Purpose: Compute Pieri product in classical cohomology")
    
    i = 1
    lam = [2, 1]
    k = 2
    n = 5
    
    result = pieriA_inner(i, lam, k, n)
    print(f"   Input:  i={i}, λ={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print(f"   Meaning: σ_{lam} * σ_{{1}}^{i} in H*(Gr({k},{n}))")
    
    # Another classical example
    print("\n   Example 2:")
    i = 1
    lam = [1]
    k = 2
    n = 4
    
    result = pieriA_inner(i, lam, k, n)
    print(f"   Input:  i={i}, λ={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print(f"   Expected: σ_{{2}} + σ_{{1,1}} (from documentation)")
    
    # Quantum Pieri example
    print("\n7. qpieriA_inner(i, lam, k, n) - Quantum Pieri")
    print("   Purpose: Compute Pieri product in quantum cohomology")
    
    i = 1
    lam = [2, 2]  # Full length partition for quantum effects
    k = 2
    n = 4
    
    result = qpieriA_inner(i, lam, k, n)
    print(f"   Input:  i={i}, λ={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print(f"   Note: Should include quantum correction term q*something")
    
    # Quantum example with q term
    print("\n   Example 2 (quantum effects):")
    i = 2
    lam = [1, 1]
    k = 2  
    n = 4
    
    result = qpieriA_inner(i, lam, k, n)
    print(f"   Input:  i={i}, λ={lam}, k={k}, n={n}")
    print(f"   Output: {result}")

def demonstrate_grassmannian_interface():
    """Demonstrate using Grassmannian class interface"""
    print_separator("GRASSMANNIAN CLASS INTERFACE")
    
    # Create Grassmannian
    gr = Grassmannian(2, 5)  # Gr(2,5)
    print(f"Grassmannian: {gr}")
    
    # Classical pieri 
    print("\n8. Classical Pieri via Grassmannian class")
    result = gr.pieri(1, 'S[2,1]')
    print(f"   Input:  gr.pieri(1, 'S[2,1]')")
    print(f"   Output: {result}")
    
    # Quantum pieri
    print("\n9. Quantum Pieri via Grassmannian class")
    result = gr.qpieri(1, 'S[2,1]')
    print(f"   Input:  gr.qpieri(1, 'S[2,1]')")
    print(f"   Output: {result}")
    
    # Example with quantum term
    result = gr.qpieri(1, 'S[3,2]')
    print(f"   Input:  gr.qpieri(1, 'S[3,2]')")
    print(f"   Output: {result}")

def demonstrate_typeB_helper_functions():
    """Demonstrate Type B specific helper functions with examples from documentation"""
    print_separator("TYPE B SPECIFIC HELPER FUNCTIONS")
    
    # 1. part_conj example (Algorithm 1.6)
    print("\n1. part_conj(lam) - Partition Conjugate")
    print("   Purpose: Compute conjugate partition (transpose Young diagram)")
    
    lam = [4, 2, 1]
    result = part_conj(lam)
    print(f"   Input:  lam={lam}")
    print(f"   Output: {result}")
    print("   Algorithm: λ'[i] = number of parts in λ with value ≥ i")
    print("   Example: [4,2,1] → [3,2,1,1] (transpose diagram)")
    
    # 2. _part_tilde example (Algorithm 1.7)
    print("\n2. _part_tilde(lam, rows, cols) - Type B Specific Helper")
    print("   Purpose: Check and transform partition for Type B quantum corrections")
    
    lam = [2, 1]
    rows, cols = 3, 4
    result = _part_tilde(lam, rows, cols)
    print(f"   Input:  lam={lam}, rows={rows}, cols={cols}")
    print(f"   Output: {result}")
    print("   Algorithm: Complex conditions for Type B quantum terms")

def demonstrate_typeB_set_generation():
    """Demonstrate Type B set generation with unique characteristics"""
    print_separator("TYPE B SET GENERATION")
    
    # Focus on Type B specific behavior (skipfirst=False)
    print("\n3. count_comps with Type B characteristics")
    print("   Purpose: Type B specific component counting")
    
    lam1, lam2 = [1], [2]
    skipfirst, k, d = False, 1, 0  # Type B characteristics
    result = count_comps(lam1, lam2, skipfirst, k, d)
    print(f"   Type B: count_comps({lam1}, {lam2}, {skipfirst}, {k}, {d}) → {result}")
    print("   Note: Type B uses skipfirst=False, gives higher counts than Type C")

def demonstrate_typeB_fill_and_itr():
    """Demonstrate Type B _pieri_fill and _pieri_itr functions"""
    print_separator("TYPE B FILL AND ITERATOR EXAMPLES")
    
    # 1. _pieri_fill example (Algorithm 1.3)
    print("\n6. _pieri_fill(lam, inner, outer, r, p) - Type B Fill")
    print("   Purpose: Fill boxes into partition with Type B constraints")
    
    lam = [2, 1]
    inner = [2, 1] 
    outer = [4, 3]
    r, p = 1, 1
    result = _pieri_fill(lam, inner, outer, r, p)
    print(f"   Input:  lam={lam}, inner={inner}, outer={outer}, r={r}, p={p}")
    print(f"   Output: {result}")
    print("   Algorithm: Different from Type A - uses res[rr-2] - 1 constraint")
    
    # 2. _pieri_itr example (Algorithm 1.4)
    print("\n7. _pieri_itr(lam, inner, outer) - Type B Iterator")
    print("   Purpose: Generate next partition in Type B iteration")
    
    current = [3, 1]
    inner = [2, 1]
    outer = [4, 3]
    result = _pieri_itr(current, inner, outer)
    print(f"   Input:  current={current}, inner={inner}, outer={outer}")
    print(f"   Output: {result}")
    print("   Algorithm: Similar to Type A but uses Type B _pieri_fill")

def demonstrate_typeB_main_algorithms():
    """Demonstrate main Type B algorithms with examples from documentation"""
    print_separator("TYPE B MAIN ALGORITHMS")
    
    # 1. pieriB_inner example (Algorithm 1)
    print("\n8. pieriB_inner(p, lam, k, n) - Classical Pieri Type B")
    print("   Purpose: Compute classical Pieri product with 2^(c-b) coefficients")
    
    p, lam, k, n = 1, [2], 1, 2
    result = pieriB_inner(p, lam, k, n)
    print(f"   Input:  p={p}, lam={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print("   Algorithm: Use pieri_set + count_comps + 2^(c-b) coefficients")
    print("   Context: OG(1,5) - Orthogonal Grassmannian odd dimension")
    
    # 2. qpieriB_inner example (Algorithm 2)
    print("\n9. qpieriB_inner(p, lam, k, n) - Quantum Pieri Type B")
    print("   Purpose: Compute quantum Pieri with complex quantum corrections")
    
    p, lam, k, n = 1, [3], 1, 2
    result = qpieriB_inner(p, lam, k, n)
    print(f"   Input:  p={p}, lam={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print("   Algorithm: Classical + quantum corrections (k=0 vs k>0 cases)")
    print("   Note: Type B has most complex quantum behavior")

def demonstrate_typeB_grassmannian_interface():
    """Demonstrate OrthogonalGrassmannian class interface for Type B"""
    print_separator("TYPE B ORTHOGONAL GRASSMANNIAN INTERFACE")
    
    # Create OG for odd dimension (Type B)
    og = OrthogonalGrassmannian(1, 5)  # OG(1,5) -> Type B
    print(f"Grassmannian: {og}")
    print("Note: Odd dimension gives Type B")
    
    # Classical pieri via class
    print("\n10. Classical Pieri via OrthogonalGrassmannian class")
    result = og.pieri(1, 'S[2]')
    print(f"   Input:  og.pieri(1, 'S[2]')")
    print(f"   Output: {result}")
    
    # Quantum pieri via class
    print("\n11. Quantum Pieri via OrthogonalGrassmannian class")
    result = og.qpieri(1, 'S[2]')
    print(f"   Input:  og.qpieri(1, 'S[2]')")
    print(f"   Output: {result}")
    print("   Note: May include quantum terms with q or q² degrees")

def demonstrate_typeC_helper_functions():
    """Demonstrate Type C specific characteristics"""
    print_separator("TYPE C SPECIFIC CHARACTERISTICS")
    
    # Focus only on Type C unique characteristics (skipfirst=true)
    print("\n1. Type C Component Counting (skipfirst=True)")
    print("   Purpose: Type C specific component counting behavior")
    
    lam1, lam2 = [1], [2]
    skipfirst_C, k, d = True, 1, 0   # Type C uses skipfirst=True
    result_C = count_comps(lam1, lam2, skipfirst_C, k, d)
    print(f"   Type C: count_comps({lam1}, {lam2}, {skipfirst_C}, {k}, {d}) → {result_C}")
    print("   Characteristic: skipfirst=True typically gives lower coefficients")
    print("   Used in: pieriC_inner for 2^c coefficient calculation")

def demonstrate_typeC_set_generation():
    """Removed - consolidated into shared functions"""
    pass

def demonstrate_typeC_main_algorithms():
    """Demonstrate main Type C algorithms with examples from documentation"""
    print_separator("TYPE C MAIN ALGORITHMS")
    
    # 1. pieriC_inner example 
    print("\n4. pieriC_inner(i, lam, k, n) - Classical Pieri Type C")
    print("   Purpose: Compute classical Pieri product with 2^c coefficients and skipfirst=True")
    
    i, lam, k, n = 1, [1], 1, 2
    result = pieriC_inner(i, lam, k, n)
    print(f"   Input:  i={i}, lam={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print("   Algorithm: Use pieri_set + count_comps(skipfirst=True) + 2^c coefficients")
    print("   Context: IG(1,4) - Isotropic Grassmannian (symplectic)")
    
    # Show detailed coefficient calculation
    print("   Detailed calculation:")
    partitions = pieri_set(i, lam, k, n, 0)
    print(f"     Generated partitions: {partitions}")
    for mu in partitions:
        c = count_comps(lam, mu, True, k, 0)  # skipfirst=True for Type C
        coeff = 2**c
        print(f"     {lam} → {mu}: count_comps = {c}, coefficient = 2^{c} = {coeff}")
    
    # 2. qpieriC_inner example
    print("\n5. qpieriC_inner(i, lam, k, n) - Quantum Pieri Type C")
    print("   Purpose: Compute quantum Pieri with simple q/2 quantum correction")
    
    i, lam, k, n = 1, [1], 1, 2  # Using simpler example to show quantum effect
    result = qpieriC_inner(i, lam, k, n)
    print(f"   Input:  i={i}, lam={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print("   Algorithm: Classical + (q/2)*quantum_correction")
    print("   Note: Type C always has quantum term with q/2 coefficient")
    print("   Characteristic: Uses _part_star(μ, n+k+1) for quantum corrections")

def demonstrate_typeC_grassmannian_interface():
    """Demonstrate IsotropicGrassmannian class interface for Type C"""
    print_separator("TYPE C ISOTROPIC GRASSMANNIAN INTERFACE")
    
    # Create IG for even dimension (Type C)
    ig = IsotropicGrassmannian(1, 4)  # IG(1,4) -> Type C
    print(f"Grassmannian: {ig}")
    print("Note: Even dimension gives Type C (symplectic)")
    
    # Classical pieri via class
    print("\n6. Classical Pieri via IsotropicGrassmannian class")
    result = ig.pieri(1, 'S[1]')
    print(f"   Input:  ig.pieri(1, 'S[1]')")
    print(f"   Output: {result}")
    
    # Quantum pieri via class
    print("\n7. Quantum Pieri via IsotropicGrassmannian class")
    result = ig.qpieri(1, 'S[1]')
    print(f"   Input:  ig.qpieri(1, 'S[1]')")
    print(f"   Output: {result}")
    print("   Note: q/2 coefficient is characteristic of Type C (symplectic)")

def demonstrate_typeD_helper_functions():
    """Demonstrate Type D specific helper functions with examples from documentation"""
    print_separator("TYPE D SPECIFIC HELPER FUNCTIONS")
    
    # 1. _dcoef example - the most complex coefficient function
    print("\n1. _dcoef(p, lam, mu, tlam, k, n) - Complex Coefficient Calculation")
    print("   Purpose: Calculate coefficients with tie-breaking logic for Type D")
    
    # Simple example without tie-breaking
    p, lam, mu, k, n = 1, [1], [2], 1, 2
    # Calculate tlam (type parameter)
    tlam = 0 if k not in lam else (2 if lam and lam[-1] == 0 else 1)
    
    print(f"   Input:  p={p}, lam={lam}, mu={mu}, tlam={tlam}, k={k}, n={n}")
    try:
        result = _dcoef(p, lam, mu, tlam, k, n)
        print(f"   Output: {result}")
    except Exception as e:
        print(f"   Note: _dcoef may not be directly accessible: {e}")
    
    print("   Algorithm: count_comps(d=1) + offset + tie-breaking if cc<0")
    print("   Type parameter: 0(k∉λ), 1(k∈λ,no trailing 0), 2(k∈λ,has trailing 0)")
    
    # 2. Type D d=1 characteristic is now covered in shared functions

def demonstrate_typeD_special_functions():
    """Demonstrate Type D unique functions: dualize, type_swap, etc."""
    print_separator("TYPE D SPECIAL FUNCTIONS")
    
    # These functions are only available in Type D and very complex
    print("\n4. Type D Special Functions (Complex internal operations)")
    print("   Note: These functions are typically not exposed in public API")
    
    print("\n   • dualize(lc) - Dualization Operation")
    print("     Purpose: Perform dualization on linear combinations")
    print("     Usage: Only in quantum k=1 case")
    print("     Algorithm: Complex index transformation with Type D corrections")
    
    print("\n   • type_swap(lc, k) - Type Swapping Operation")  
    print("     Purpose: Swap between different Schubert types")
    print("     Usage: Only in quantum k>1 case")
    print("     Algorithm: Add/remove trailing zeros based on k membership")
    
    print("\n   • _toSchurFromIntnMu - Complement Set Transformation")
    print("     Purpose: Transform using complement sets")
    print("     Usage: Only in quantum k=1 case")
    print("     Algorithm: Complex combinatorial transformation")
    
    print("\n   These functions represent the most sophisticated algebraic")
    print("   operations in the entire SchubertPy library")

def demonstrate_typeD_main_algorithms():
    """Demonstrate main Type D algorithms with examples from documentation"""
    print_separator("TYPE D MAIN ALGORITHMS")
    
    # 1. pieriD_inner example
    print("\n5. pieriD_inner(p, lam, k, n) - Classical Pieri Type D")
    print("   Purpose: Most complex classical Pieri with _dcoef coefficients")
    
    p, lam, k, n = 1, [1], 1, 2
    result = pieriD_inner(p, lam, k, n)
    print(f"   Input:  p={p}, lam={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print("   Algorithm: Use pieri_set(d=1) + _dcoef + tie-breaking logic")
    print("   Context: OG(1,6) - Orthogonal Grassmannian even dimension")
    
    # Show Type D characteristics
    print("   Type D characteristics:")
    print("     • Allows negative p values")
    print("     • Uses d=1 parameter in pieri_set")
    print("     • Has tie-breaking logic for cc<0 cases")
    print("     • Type parameter tlam affects trailing zeros")
    
    # 2. qpieriD_inner example  
    print("\n6. qpieriD_inner(p, lam, k, n) - Quantum Pieri Type D")
    print("   Purpose: Most complex quantum Pieri with multiple k cases")
    
    p, lam, k, n = 1, [1], 1, 2
    result = qpieriD_inner(p, lam, k, n)
    print(f"   Input:  p={p}, lam={lam}, k={k}, n={n}")
    print(f"   Output: {result}")
    print("   Algorithm: Classical + complex quantum corrections based on k value")
    print("   Note: Type D has three different quantum cases: k=0, k=1, k>1")
    
    # Explain quantum complexity
    print("   Quantum complexity breakdown:")
    print("     • k=0: Simple case with _part_star")
    print("     • k=1: Most complex with dualize, complement sets")  
    print("     • k>1: Medium complexity with _part_tilde, type_swap")
    print("     • Uses multiple quantum parameters: q, q1, q2")

def demonstrate_typeD_grassmannian_interface():
    """Demonstrate OrthogonalGrassmannian class interface for Type D (even dimension)"""
    print_separator("TYPE D ORTHOGONAL GRASSMANNIAN INTERFACE")
    
    # Create OG for even dimension (Type D)
    # Note: Type D is for even-dimensional orthogonal Grassmannians
    og_even = OrthogonalGrassmannian(1, 6)  # OG(1,6) -> Type D  
    print(f"Grassmannian: {og_even}")
    print("Note: Even dimension gives Type D (most complex case)")
    
    # Classical pieri via class
    print("\n7. Classical Pieri via OrthogonalGrassmannian class (Type D)")
    result = og_even.pieri(1, 'S[1]')
    print(f"   Input:  og_even.pieri(1, 'S[1]')")
    print(f"   Output: {result}")
    
    # Quantum pieri via class
    print("\n8. Quantum Pieri via OrthogonalGrassmannian class (Type D)")
    result = og_even.qpieri(1, 'S[1]')
    print(f"   Input:  og_even.qpieri(1, 'S[1]')")
    print(f"   Output: {result}")
    print("   Note: May include quantum terms with q, q1, q2 parameters")
    print("   Complex: Three different quantum behaviors based on k")

def demonstrate_comprehensive_comparison():
    """Comprehensive comparison of all four types"""
    print_separator("COMPREHENSIVE TYPE COMPARISON")
    
    print("\nComplete comparison of Type A, B, C, and D:")
    print("┌─────────────────────┬──────────────┬─────────────────┬─────────────────┬─────────────────┐")
    print("│ Aspect              │ Type A       │ Type B          │ Type C          │ Type D          │")
    print("├─────────────────────┼──────────────┼─────────────────┼─────────────────┼─────────────────┤")
    print("│ Coefficients        │ 1            │ 2^(c-b)         │ 2^c             │ _dcoef (complex)│")
    print("│ skipfirst           │ N/A          │ false           │ true            │ false           │")
    print("│ d parameter         │ N/A          │ 0               │ 0               │ 1               │")
    print("│ Quantum cases       │ 1            │ 2 (k=0 vs k>0) │ 1 (always)      │ 3 (k=0,1,>1)   │")
    print("│ Quantum coefficient │ q            │ q, q²           │ q/2             │ q, q1, q2       │")
    print("│ Tie-breaking        │ No           │ No              │ No              │ Yes             │")
    print("│ Negative p          │ No           │ No              │ No              │ Yes             │")
    print("│ Special functions   │ none         │ _part_tilde     │ none            │ dualize, swap   │")
    print("│ Helper functions    │ _part_star   │ +part_conj      │ same as B       │ +_dcoef         │")
    print("│ Grassmannian        │ Gr(k,n)      │ OG(k,2n+1)      │ IG(k,2n)        │ OG(k,2n+2)      │")
    print("│ Geometry            │ Linear       │ Orthogonal odd  │ Symplectic      │ Orthogonal even │")
    print("│ Complexity          │ Low          │ High            │ Medium          │ Extreme         │")
    print("└─────────────────────┴──────────────┴─────────────────┴─────────────────┴─────────────────┘")
    
    print("\nKey insights:")
    print("• Type A: Foundation - simplest algorithms, prototype for others")
    print("• Type B: Introduces complexity - 2^(c-b) coefficients, _part_tilde")  
    print("• Type C: Symplectic variation - skipfirst=true, q/2 quantum coefficient")
    print("• Type D: Ultimate complexity - tie-breaking, multiple quantum cases")
    
    print("\nShared vs Unique functions:")
    print("• Shared: _part_star (all types), pieri_set (B,C,D), count_comps (B,C,D)")
    print("• Type A only: padding_right, _pieri_fillA, _pieri_itrA")
    print("• Type B only: _part_tilde, part_conj")
    print("• Type C only: None (uses Type B functions with different parameters)")
    print("• Type D only: _dcoef, dualize, type_swap, _toSchurFromIntnMu")
    
    print("\nComplexity progression: Type A → Type C → Type B → Type D")
    print("Each type builds upon previous concepts with additional sophistication")

def demonstrate_typeB_comparison():
    """Removed - consolidated into comprehensive comparison"""
    pass

def demonstrate_typeC_comparison():
    """Removed - consolidated into comprehensive comparison"""  
    pass

def demonstrate_typeD_comparison():
    """Removed - consolidated into comprehensive comparison"""
    pass

def main():
    """Run all demonstrations"""
    print("PIERI ALGORITHMS - TYPE A, TYPE B, TYPE C, AND TYPE D EXAMPLES")
    print("Based on documentation from all four pieri_type*_algorithms.md files")
    print("OPTIMIZED VERSION - Eliminated duplicates, focused on key differences")
    
    try:
        # Shared functions first
        demonstrate_shared_helper_functions()
        
        # Type A examples (streamlined)
        demonstrate_helper_functions()
        demonstrate_pieri_fill_and_itr()
        demonstrate_main_algorithms()
        demonstrate_grassmannian_interface()
        
        # Type B examples (focused on unique aspects)
        demonstrate_typeB_helper_functions()
        demonstrate_typeB_set_generation()
        demonstrate_typeB_fill_and_itr()
        demonstrate_typeB_main_algorithms()
        demonstrate_typeB_grassmannian_interface()
        
        # Type C examples (focused on differences from B)
        demonstrate_typeC_helper_functions()
        demonstrate_typeC_main_algorithms()
        demonstrate_typeC_grassmannian_interface()
        
        # Type D examples (focused on unique complexity)
        demonstrate_typeD_helper_functions()
        demonstrate_typeD_special_functions()
        demonstrate_typeD_main_algorithms()
        demonstrate_typeD_grassmannian_interface()
        
        # Unified comparison
        demonstrate_comprehensive_comparison()
        
        print("\n" + "="*80)
        print(" ALL TYPE EXAMPLES COMPLETED - OPTIMIZED VERSION")
        print("="*80)
        print("\nSummary (Consolidated):")
        print("• Eliminated duplicate _part_star, pieri_set, and comparison functions")
        print("• Focused on unique characteristics of each type")
        print("• Highlighted shared vs. type-specific functions")
        print("• Comprehensive comparison table covers all four types")
        print("• Streamlined demonstration while preserving educational value")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 