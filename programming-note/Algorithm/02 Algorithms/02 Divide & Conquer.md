# 02 Divide & Conquer

Split the problem into smaller subproblems, solve them recursively, combine the results. Three steps: **Divide → Conquer → Combine**.

---

## The Pattern

```java
Result divideAndConquer(Problem p) {
    if (p is small enough) {
        return solveDirectly(p);           // Base case
    }
    SubProblem[] subs = divide(p);          // Divide
    Result[] results = new Result[subs.length];
    for (int i = 0; i < subs.length; i++) {
        results[i] = divideAndConquer(subs[i]);  // Conquer (recursively)
    }
    return combine(results);                // Combine
}
```

---

## Classic Examples

### Merge Sort

```
Divide:  split array in half
Conquer: recursively sort each half
Combine: merge two sorted halves

[38,27,43,3,9,82,10]
       ↙           ↘
[38,27,43,3]   [9,82,10]
    ↙    ↘        ↙    ↘
[38,27] [43,3] [9,82] [10]
```

### Quick Sort

```
Divide:  partition around pivot
Conquer: recursively sort left and right of pivot
Combine: nothing — sorting happens in-place during partition
```

### Binary Search

```
Divide:  compare target with middle element
Conquer: search in left OR right half (only one!)
Combine: nothing — result propagates up
```

---

## Master Theorem

For recurrences of the form: $T(n) = a \cdot T(n/b) + f(n)$

| Case | Condition | Result |
|------|-----------|--------|
| 1 | $f(n) = O(n^{\log_b a - \epsilon})$ | $T(n) = \Theta(n^{\log_b a})$ |
| 2 | $f(n) = \Theta(n^{\log_b a})$ | $T(n) = \Theta(n^{\log_b a} \log n)$ |
| 3 | $f(n) = \Omega(n^{\log_b a + \epsilon})$ | $T(n) = \Theta(f(n))$ |

### Applying to Common Algorithms

| Algorithm | Recurrence | a | b | f(n) | Result |
|-----------|-----------|---|---|------|--------|
| Binary Search | T(n) = T(n/2) + O(1) | 1 | 2 | O(1) | O(log n) |
| Merge Sort | T(n) = 2T(n/2) + O(n) | 2 | 2 | O(n) | O(n log n) |
| Quick Sort (avg) | T(n) = 2T(n/2) + O(n) | 2 | 2 | O(n) | O(n log n) |
| Strassen Matrix | T(n) = 7T(n/2) + O(n²) | 7 | 2 | O(n²) | O(n^2.81) |

---

## When to Use Divide & Conquer

| ✅ Good Fit | ❌ Not a Good Fit |
|------------|------------------|
| Problem can be split into independent subproblems | Subproblems overlap (use DP instead) |
| Combining solutions is efficient | Splitting is more expensive than solving directly |
| Parallelizable | Subproblems must be solved sequentially |

---

## Sources

- CLRS — Chapter 4
- LeetCode — Divide & Conquer problem sets
