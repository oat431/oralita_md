---
tags:
- algorithms
- data-structures
- programming
---

# 01 Stacks & Queues

Stack = LIFO (last in, first out). Queue = FIFO (first in, first out). Both are O(1) for core operations. Simple structures, powerful patterns.

---

## Stack

```
Push:  [    ] → [ 3  ] → [ 3, 7 ] → [ 3, 7, 2 ]
Pop:   [ 3,7,2 ] → 2 → [ 3,7 ]
Peek:  [ 3,7 ] → 7 (without removing)
```

| Operation | Time |
|-----------|:----:|
| push() | O(1) |
| pop() | O(1) |
| peek() | O(1) |
| isEmpty() | O(1) |

```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(10);
stack.push(20);
int top = stack.pop();  // 20
```

### Monotonic Stack

Maintains elements in increasing/decreasing order. Used when you need "next greater/smaller element."

```java
// Next Greater Element — O(n)
int[] nextGreater(int[] nums) {
    int[] result = new int[nums.length];
    Deque<Integer> stack = new ArrayDeque<>();
    
    for (int i = nums.length - 1; i >= 0; i--) {
        while (!stack.isEmpty() && stack.peek() <= nums[i]) {
            stack.pop();
        }
        result[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(nums[i]);
    }
    return result;
}
```

### Stack Applications

| Use Case | Pattern |
|----------|---------|
| **Balanced parentheses** | Push on '(', pop on ')' |
| **Undo/redo** | Push state on each action |
| **Function calls** | Call stack — recursion uses it implicitly |
| **Expression evaluation** | Infix → postfix, evaluate RPN |
| **DFS** | Stack-based traversal (or recursion) |

---

## Queue

```
Enqueue:  [    ] → [ A ] → [ A, B ] → [ A, B, C ]
Dequeue:  [ A,B,C ] → A → [ B, C ]
```

| Operation | Time |
|-----------|:----:|
| enqueue() | O(1) |
| dequeue() | O(1) |
| peek() | O(1) |

```java
Queue<String> queue = new LinkedList<>();
queue.offer("A");     // enqueue
queue.offer("B");
String first = queue.poll();  // dequeue → "A"
```

### Deque (Double-Ended Queue)

Insert/delete from both ends in O(1).

```java
Deque<Integer> deque = new ArrayDeque<>();
deque.addFirst(1);   // [1]
deque.addLast(2);    // [1, 2]
deque.addFirst(0);   // [0, 1, 2]
deque.removeLast();  // [0, 1]
```

### Queue Applications

| Use Case | Pattern |
|----------|---------|
| **BFS** | Level-order tree/ graph traversal |
| **Sliding window** | Deque for max/min in window |
| **Task scheduling** | Producer-consumer, thread pools |
| **LRU Cache** | Queue + Hash Map |
| **Message queues** | Kafka, RabbitMQ — at scale |

---

## Stack vs Queue

| | Stack | Queue |
|---|:---:|:---:|
| Order | LIFO | FIFO |
| DFS vs BFS | DFS | BFS |
| Backtracking | Implicit (call stack) | Not used |
| Java | `ArrayDeque` (push/pop) | `LinkedList` / `ArrayDeque` |

---

## Sources

- CLRS — Chapter 10.1
- LeetCode — Stack / Queue problem sets
