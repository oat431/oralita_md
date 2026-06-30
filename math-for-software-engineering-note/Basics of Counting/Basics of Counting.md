---
tags:
- combinatorics
- math
- probability
- software-engineering
---

# Topic 8: Basics of Counting

Counting principles answer "how many?" — essential for complexity analysis, combinatorial testing, and probability calculations. These are the foundations Big-O notation rests on.

---

## 1. The Sum Rule

If a task can be done in one of $m$ **mutually exclusive** ways, where way 1 has $n_1$ options, way 2 has $n_2$ options, etc., then the total number of ways is:
$$N = n_1 + n_2 + \dots + n_m$$

**Example:** Choosing lunch — 3 sandwich options OR 4 salad options = $3 + 4 = 7$ total choices.

**In code:** An `if-else if` chain where only one branch executes: total paths = sum of paths through each branch.

---

## 2. The Product Rule

If a task consists of $m$ **sequential** steps, where step 1 has $n_1$ options, step 2 has $n_2$ options, etc., then the total number of ways is:
$$N = n_1 \times n_2 \times \dots \times n_m$$

**Example:** Choosing a meal — 3 appetizers × 4 mains × 2 desserts = $3 \times 4 \times 2 = 24$ possible meals.

**In code:** Nested loops — the total iterations of a triple-nested loop is the product of loop bounds:
```python
for i in range(3):      # 3
    for j in range(4):  # × 4
        for k in range(2):  # × 2
            pass         # = 24 total iterations
```

---

## 3. The Inclusion-Exclusion Principle

When sets **overlap**, the sum rule double-counts. Fix it by subtracting overlaps:

For two sets: $|A \cup B| = |A| + |B| - |A \cap B|$

For three sets: $|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$

**Pattern:** Add singles, subtract pairs, add triples, etc. (alternating signs).

**Example:** How many numbers from 1–100 are divisible by 3 or 5?
- Divisible by 3: $\lfloor 100/3 \rfloor = 33$
- Divisible by 5: $\lfloor 100/5 \rfloor = 20$
- Divisible by both (15): $\lfloor 100/15 \rfloor = 6$
- Answer: $33 + 20 - 6 = 47$

---

## 4. Permutations

A **permutation** is an ordered arrangement of $r$ items from a set of $n$:
$$P(n, r) = \frac{n!}{(n-r)!}$$

**Special case:** Permutation of all $n$ items = $n!$

**Example:** Arranging 3 people from 5 in a line: $P(5,3) = \frac{5!}{2!} = \frac{120}{2} = 60$

**In code:** Generating all orderings — combinatorial algorithms for test case generation, brute-force search, traveling salesman.

---

## 5. Combinations

A **combination** is an unordered selection of $r$ items from $n$:
$$C(n, r) = \binom{n}{r} = \frac{n!}{r!(n-r)!}$$

**Example:** Choosing a 3-person committee from 5 candidates: $\binom{5}{3} = \frac{120}{6 \cdot 2} = 10$

**In code:** Binomial coefficients appear in:
- Pascal's triangle (dynamic programming)
- Binomial theorem: $(x + y)^n = \sum_{k=0}^n \binom{n}{k} x^{n-k} y^k$
- Combinatorial test selection (pairwise testing)

---

## 6. Recursion & Recurrence Relations

A **recurrence relation** defines a sequence in terms of previous terms.

**Classic examples:**

| Sequence | Recurrence | Base |
|----------|-----------|------|
| Factorial | $n! = n \cdot (n-1)!$ | $0! = 1$ |
| Fibonacci | $F_n = F_{n-1} + F_{n-2}$ | $F_0 = 0, F_1 = 1$ |
| Tower of Hanoi | $T_n = 2T_{n-1} + 1$ | $T_1 = 1$ |

**In code:** Recursive algorithms are direct implementations of recurrence relations. The recurrence defines the time complexity:
- Merge sort: $T(n) = 2T(n/2) + O(n) \implies O(n \log n)$
- Binary search: $T(n) = T(n/2) + O(1) \implies O(\log n)$

---

## Why Counting Matters in SE

| Concept | SE Application |
|---------|---------------|
| Product rule | Nested loop complexity, cartesian product test generation |
| Sum rule | Branch coverage analysis, cyclomatic complexity |
| Permutations | Brute-force search space, scheduling algorithms |
| Combinations | Combinatorial testing (pairwise/t-wise), feature flags combination testing |
| Inclusion-Exclusion | Union of test coverage sets, probability of overlapping events |
| Recurrence relations | Divide-and-conquer algorithm analysis, dynamic programming |

---

## Sources

- [1*] K. Rosen, *Discrete Mathematics and Its Applications*, 8th ed., McGraw-Hill, 2018.
- SWEBOK v4.0 — Chapter 17: Mathematical Foundations
