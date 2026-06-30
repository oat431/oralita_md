---
tags:
- algorithms
- data-structures
- programming
---

# 02 Searching

Finding an element in a collection. From simple linear scan to binary search and beyond.

---

## Linear Search

Check every element. Works on unsorted data. O(n).

```java
int linearSearch(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) return i;
    }
    return -1;
}
```

---

## Binary Search

Divide and conquer on **sorted** data. O(log n).

```java
int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;  // Avoid overflow
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

### Binary Search Patterns

| Pattern | What It Finds | Condition |
|---------|--------------|-----------|
| **Exact match** | `arr[mid] == target` | Standard |
| **First occurrence** | `arr[mid] >= target`, then `right = mid - 1` | Lower bound |
| **Last occurrence** | `arr[mid] <= target`, then `left = mid + 1` | Upper bound |
| **Insertion point** | `left` after loop | Where target should go |

```java
// Find first position ≥ target (lower bound)
int lowerBound(int[] arr, int target) {
    int left = 0, right = arr.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] >= target) right = mid;
        else left = mid + 1;
    }
    return left;  // First index where arr[i] >= target
}
```

---

## Binary Search on Answer

Not searching an array — searching a **value range** for the answer that satisfies a condition.

```java
// Find square root (floor) — O(log n)
int sqrt(int x) {
    if (x < 2) return x;
    int left = 1, right = x / 2;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        long sq = (long) mid * mid;
        if (sq == x) return mid;
        if (sq < x) left = mid + 1;
        else right = mid - 1;
    }
    return right;
}
```

### When to Use

| Problem Pattern | Example |
|----------------|---------|
| "Find the minimum/maximum X such that..." | Min capacity to ship packages |
| Monotonic condition | "If X works, X+1 also works" |
| K-th smallest/largest | K-th smallest in matrix |

---

## Search in Rotated Sorted Array

```java
int searchRotated(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        
        // Left half is sorted
        if (nums[left] <= nums[mid]) {
            if (nums[left] <= target && target < nums[mid]) right = mid - 1;
            else left = mid + 1;
        }
        // Right half is sorted
        else {
            if (nums[mid] < target && target <= nums[right]) left = mid + 1;
            else right = mid - 1;
        }
    }
    return -1;
}
```

---

## Search Complexity

| Algorithm | Time (Worst) | Space | Precondition |
|-----------|:----------:|:-----:|-------------|
| Linear | O(n) | O(1) | None |
| Binary | O(log n) | O(1) | Sorted |
| BFS | O(V + E) | O(V) | Graph |
| DFS | O(V + E) | O(V) | Graph |

---

## Sources

- CLRS — Chapter 2, 12
- LeetCode — Binary Search problem sets
