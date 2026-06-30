---
tags:
- algorithms
- data-structures
- programming
---

# 01 Heaps & Priority Queues

A heap is a complete binary tree where every parent is ordered relative to its children. Min-heap: parent ≤ children. Max-heap: parent ≥ children. The smallest/largest element is always at the root.

---

## Heap Operations

| Operation | Time |
|-----------|:----:|
| peek() — get min/max | O(1) |
| insert() — push + bubble up | O(log n) |
| poll() — remove root + bubble down | O(log n) |
| heapify() — build from array | O(n) |

```java
// Java PriorityQueue (min-heap by default)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5);
minHeap.offer(2);
minHeap.offer(8);
minHeap.peek();  // 2 (smallest)
minHeap.poll();  // removes 2

// Max-heap
PriorityQueue<Integer> maxHeap = 
    new PriorityQueue<>(Collections.reverseOrder());
```

---

## Heap Internals

Stored as an array (no pointers needed — complete tree property):

```
Array index:
  parent = (i - 1) / 2
  left child = 2 * i + 1
  right child = 2 * i + 2

        2           ← index 0
       / \
      5   8         ← index 1, 2
     /
    9               ← index 3
```

```java
// Custom heap (min-heap)
class MinHeap {
    private List<Integer> heap = new ArrayList<>();
    
    void insert(int val) {
        heap.add(val);
        bubbleUp(heap.size() - 1);
    }
    
    private void bubbleUp(int i) {
        while (i > 0) {
            int parent = (i - 1) / 2;
            if (heap.get(i) >= heap.get(parent)) break;
            Collections.swap(heap, i, parent);
            i = parent;
        }
    }
    
    int poll() {
        int min = heap.get(0);
        heap.set(0, heap.remove(heap.size() - 1));
        bubbleDown(0);
        return min;
    }
    
    private void bubbleDown(int i) {
        int size = heap.size();
        while (true) {
            int left = 2 * i + 1, right = 2 * i + 2;
            int smallest = i;
            if (left < size && heap.get(left) < heap.get(smallest)) smallest = left;
            if (right < size && heap.get(right) < heap.get(smallest)) smallest = right;
            if (smallest == i) break;
            Collections.swap(heap, i, smallest);
            i = smallest;
        }
    }
}
```

---

## Applications

| Problem | Pattern |
|---------|---------|
| **Top K elements** | Min-heap of size K. For each new element: if > heap.peek(), poll + insert. |
| **K-th largest/smallest** | Heap of size K |
| **Merge K sorted lists** | Min-heap of list heads |
| **Median of stream** | Two heaps: max-heap (lower half) + min-heap (upper half) |
| **Dijkstra's algorithm** | Min-heap for shortest path |
| **Task scheduler** | Max-heap by frequency + cooldown |

### Top K Elements

```java
// Find K largest elements in array — O(n log k)
int[] topK(int[] nums, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>(); // min-heap
    for (int n : nums) {
        heap.offer(n);
        if (heap.size() > k) heap.poll();
    }
    return heap.stream().mapToInt(i -> i).toArray();
}
```

---

## Heap Sort

Build heap O(n) + extract n times O(n log n) = **O(n log n)** total. In-place, not stable.

```java
void heapSort(int[] arr) {
    int n = arr.length;
    // Build max-heap
    for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
    // Extract one by one
    for (int i = n - 1; i > 0; i--) {
        swap(arr, 0, i);
        heapify(arr, i, 0);
    }
}
```

---

## Sources

- CLRS — Chapter 6
- LeetCode — Heap / Priority Queue problem sets
