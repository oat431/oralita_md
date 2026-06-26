# 03 Complexity Analysis & Problem-Solving Patterns

Most interview problems fit a known pattern. Recognizing the pattern unlocks the optimal solution. This file covers Big-O analysis and the 10 most common problem-solving patterns.

---

## Big-O Complexity

How runtime/space grows as input size grows.

| Notation | Name | Example |
|----------|------|---------|
| **O(1)** | Constant | Array access, hash table lookup |
| **O(log n)** | Logarithmic | Binary search |
| **O(n)** | Linear | Linear search, single loop |
| **O(n log n)** | Linearithmic | Merge sort, quick sort (avg) |
| **O(n²)** | Quadratic | Nested loops, bubble sort |
| **O(2ⁿ)** | Exponential | Subsets, brute-force combinatorics |
| **O(n!)** | Factorial | Permutations |

### Quick Estimation

```
n = 10        → O(n!), O(2ⁿ), O(n³) all fine
n = 100       → O(n³) max
n = 1,000     → O(n²) max
n = 10,000    → O(n²) borderline
n = 100,000   → O(n log n) target
n = 1,000,000 → O(n) or O(log n)
```

---

## 10 Essential Patterns

### 1. Two Pointers

Two indices moving through a sorted array. Opposite ends or same direction.

```java
// Pair sum in sorted array — O(n)
int[] pairSum(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) return new int[]{left, right};
        if (sum < target) left++;
        else right--;
    }
    return new int[]{-1, -1};
}
```

### 2. Sliding Window

Maintain a window that slides across the array.

```java
// Max sum subarray of size k — O(n)
int maxSum(int[] arr, int k) {
    int windowSum = 0, maxSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];
    maxSum = windowSum;
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}
```

### 3. Fast & Slow Pointers

One pointer moves twice as fast. Cycle detection, middle of list.

### 4. Merge Intervals

Sort by start, then merge overlapping.

```java
// Merge overlapping intervals — O(n log n)
int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> result = new ArrayList<>();
    int[] curr = intervals[0];
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] <= curr[1]) {
            curr[1] = Math.max(curr[1], intervals[i][1]);
        } else {
            result.add(curr);
            curr = intervals[i];
        }
    }
    result.add(curr);
    return result.toArray(new int[0][]);
}
```

### 5. Modified Binary Search

Search an answer space, not an array.

### 6. BFS / DFS on Matrix

Grid traversal. Number of islands, shortest path in maze.

### 7. Topological Sort

Dependency ordering. Course schedule, build systems.

### 8. Prefix Sum

Precompute cumulative sums for O(1) range queries.

```java
// Range sum queries — build O(n), query O(1)
int[] prefix = new int[nums.length + 1];
for (int i = 0; i < nums.length; i++) {
    prefix[i + 1] = prefix[i] + nums[i];
}
// Sum of nums[L..R] = prefix[R+1] - prefix[L]
```

### 9. Union-Find (Disjoint Set)

Dynamic connectivity. Friend circles, redundant connections.

```java
class UnionFind {
    int[] parent, rank;
    UnionFind(int n) {
        parent = new int[n]; rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);  // Path compression
        return parent[x];
    }
    void union(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return;
        if (rank[px] < rank[py]) parent[px] = py;
        else if (rank[px] > rank[py]) parent[py] = px;
        else { parent[py] = px; rank[px]++; }
    }
}
```

### 10. Trie (Prefix Tree)

Efficient string search. Autocomplete, spell checker.

---

## Problem-Solving Framework

```
1. Clarify the problem (inputs, outputs, constraints)
2. Brute force first (prove it works, establish baseline)
3. Identify the pattern (two pointers? DP? sliding window?)
4. Optimize (data structure choice, eliminate loops)
5. Code clean solution
6. Test edge cases (empty, single element, duplicates, overflow)
```

---

## Sources

- LeetCode Explore cards — Patterns
- Grokking the Coding Interview — https://www.educative.io/courses/grokking-the-coding-interview
