# 01 Arrays & Linked Lists

The two most fundamental data structures. Arrays give O(1) random access. Linked lists give O(1) insertion/deletion at ends. Know both cold.

---

## Arrays

Contiguous memory. Fixed size (static) or resizable (dynamic).

| Operation | Time | Notes |
|-----------|:----:|-------|
| Access by index | O(1) | Direct memory address calculation |
| Search (unsorted) | O(n) | Linear scan |
| Insert at end | O(1)* | Amortized (dynamic array) |
| Insert at middle | O(n) | Shift elements right |
| Delete | O(n) | Shift elements left |

### Dynamic Array (ArrayList / Vector)

```java
ArrayList<Integer> list = new ArrayList<>();
list.add(10);         // [10]
list.add(20);         // [10, 20]
list.add(1, 15);      // [10, 15, 20]  — O(n) shift
list.remove(1);       // [10, 20]      — O(n) shift
int x = list.get(0);  // O(1)
```

### Common Patterns

| Pattern | When |
|---------|------|
| **Two pointers** | Sorted array, pair sum, remove duplicates |
| **Sliding window** | Subarray sum, longest substring |
| **Prefix sum** | Range sum queries in O(1) |
| **Binary search** | Sorted array search in O(log n) |

---

## Linked Lists

Nodes pointing to each other. No contiguous memory needed.

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}
```

| Operation | Singly | Doubly |
|-----------|:------:|:------:|
| Access by index | O(n) | O(n) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n) / O(1)* | O(1) |
| Delete at head | O(1) | O(1) |
| Delete at tail | O(n) | O(1) |

*O(1) with tail pointer.

```java
// Reverse a linked list (iterative) — O(n) time, O(1) space
ListNode reverse(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    while (curr != null) {
        ListNode next = curr.next;  // Save next
        curr.next = prev;           // Reverse link
        prev = curr;                // Move forward
        curr = next;
    }
    return prev;
}
```

### Common Patterns

| Pattern | Example |
|---------|---------|
| **Fast & slow pointers** | Cycle detection, middle of list |
| **Dummy head** | Simplify edge cases (empty list, delete head) |
| **Two pointers** | Merge sorted lists, intersection |

```java
// Detect cycle (Floyd's algorithm) — O(n) time, O(1) space
boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}
```

---

## Array vs Linked List

| | Array | Linked List |
|---|:---:|:---:|
| **Random access** | O(1) | O(n) |
| **Insert/delete at ends** | O(1) amortized | O(1) |
| **Insert/delete middle** | O(n) | O(1)* |
| **Memory** | Contiguous, fixed overhead | Per-node overhead (pointer) |
| **Cache friendly** | ✅ | ❌ (scattered in memory) |
| **Use when** | Random access, fixed size, cache matters | Frequent insert/delete at ends, unknown size |

---

## Sources

- CLRS — Chapters 10.1–10.2
- LeetCode — Array / Linked List problem sets
