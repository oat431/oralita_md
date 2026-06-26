# 02 Greedy Algorithms

Make the locally optimal choice at each step, hoping it leads to a globally optimal solution. Greedy algorithms are fast but don't always work — you must prove correctness.

---

## The Greedy Pattern

```java
Result greedy(Problem p) {
    Result result = new Result();
    while (/* not done */) {
        Choice c = makeBestLocalChoice(p);   // Greedy step
        if (isValid(c)) {
            result.add(c);
            p = updateProblem(p, c);
        }
    }
    return result;
}
```

---

## Classic Examples

### Activity Selection

Pick maximum number of non-overlapping activities.

```
Strategy: Always pick the activity that ENDS earliest

Activities sorted by end time:
[1,3] [2,5] [3,9] [5,8] [6,9] [8,10]
  ✓     ✗     ✗     ✓     ✗     ✓
→ Max: 3 activities
```

```java
int maxActivities(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);  // Sort by end time
    int count = 1;
    int lastEnd = intervals[0][1];
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] >= lastEnd) {
            count++;
            lastEnd = intervals[i][1];
        }
    }
    return count;
}
```

---

### Fractional Knapsack

Take fractions of items to maximize value within weight limit.

```
Strategy: Take items with highest value/weight ratio first

Items: [(60,10), (100,20), (120,30)]  — (value, weight)
Ratios: [6, 5, 4]
Capacity: 50

→ Take all of (60,10) + all of (100,20) + 2/3 of (120,30)
→ Total value: 60 + 100 + 80 = 240
```

> ⚠️ Greedy works for **fractional** knapsack. For **0/1 knapsack** (can't take fractions), use Dynamic Programming.

---

### Huffman Coding

Build optimal prefix-free binary codes for data compression.

```
Frequency:  a=45, b=13, c=12, d=16, e=9, f=5

Strategy: repeatedly merge two nodes with smallest frequency
```

---

### Dijkstra's Algorithm

Shortest path from source to all nodes (non-negative weights).

```
Strategy: always expand the unvisited node with smallest distance
```

---

## When Greedy Works

| Criteria | Why |
|----------|-----|
| **Optimal substructure** | Optimal solution contains optimal solutions to subproblems |
| **Greedy choice property** | Locally optimal choice leads to globally optimal solution |

> **You must PROVE the greedy choice property holds.** Not all problems with optimal substructure can be solved greedily — some require DP.

---

## Greedy vs DP

| | Greedy | Dynamic Programming |
|---|:---:|:---:|
| **Choices** | One choice, never reconsider | Consider all choices |
| **Speed** | O(n log n) typical | O(n²) or O(n·W) typical |
| **Proof needed?** | Yes (correctness) | No (exhaustive) |
| **Examples** | Activity selection, Dijkstra, Huffman | Knapsack 0/1, LCS, Edit distance |

---

## Sources

- CLRS — Chapter 16
- LeetCode — Greedy problem sets
