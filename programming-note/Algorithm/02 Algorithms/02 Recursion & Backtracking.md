---
tags:
- algorithms
- data-structures
- programming
---

# 02 Recursion & Backtracking

Recursion: a function that calls itself. Backtracking: systematically trying possibilities and abandoning dead ends. Together they solve combinatorial problems that iteration can't express cleanly.

---

## Recursion Fundamentals

Every recursive function needs:

1. **Base case** — when to stop
2. **Recursive case** — call itself with a smaller/simpler input

```java
// Factorial — classic recursion
int factorial(int n) {
    if (n <= 1) return 1;           // Base case
    return n * factorial(n - 1);    // Recursive case
}

// Fibonacci with memoization — O(n)
Map<Integer, Long> memo = new HashMap<>();
long fib(int n) {
    if (n <= 1) return n;
    if (memo.containsKey(n)) return memo.get(n);
    long result = fib(n - 1) + fib(n - 2);
    memo.put(n, result);
    return result;
}
```

---

## Recursion vs Iteration

| | Recursion | Iteration |
|---|:---:|:---:|
| **Tree/graph traversal** | ✅ Natural | ❌ Need explicit stack |
| **Stack overflow risk** | ❌ Deep recursion | ✅ Safe |
| **Space** | O(n) call stack | O(1) |
| **Readability** | ✅ Clean for divide & conquer | Better for simple loops |

---

## Backtracking

Try → fail → undo → try next. The "systematic trial and error" approach.

### Template

```java
void backtrack(List<List<Integer>> result, List<Integer> current, 
               int[] nums, boolean[] used) {
    if (/* solution found */) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (/* each choice */) {
        if (/* invalid choice */) continue;
        // Choose
        current.add(choice);
        used[i] = true;
        // Explore
        backtrack(result, current, nums, used);
        // Un-choose (backtrack)
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```

### Permutations

```java
List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(result, new ArrayList<>(), nums, new boolean[nums.length]);
    return result;
}
// All permutations of [1,2,3]:
// [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

### N-Queens

Place N queens on an N×N board so no two attack each other.

```java
void solve(int row, int n, List<Integer> cols, List<List<String>> result) {
    if (row == n) {
        result.add(buildBoard(cols, n));
        return;
    }
    for (int col = 0; col < n; col++) {
        if (isValid(cols, row, col)) {
            cols.add(col);
            solve(row + 1, n, cols, result);
            cols.remove(cols.size() - 1);  // Backtrack
        }
    }
}
```

---

## Common Backtracking Problems

| Problem | Pattern |
|---------|---------|
| **Permutations** | Track used elements |
| **Combinations** | Forbid revisiting by passing start index |
| **Subsets** | Include/exclude each element |
| **Sudoku** | Try 1-9, backtrack on conflict |
| **Word search** | DFS on grid, mark visited |

---

## Pruning — Cut Dead Branches Early

Don't explore paths that can never lead to a solution.

```java
// Combination sum with pruning
if (remaining < 0) return;           // Dead branch
if (remaining < nums[start]) return; // Remaining too small
```

---

## Sources

- CLRS — Chapter 4 (Divide and Conquer)
- LeetCode — Backtracking problem sets
