# 01 Hash Tables

Hash tables give O(1) average-time insert, delete, and lookup. They're the most-used data structure in practice — dictionaries, caches, sets, database indexes all use hashing.

---

## How Hashing Works

```
key → hash function → index → bucket

"Alice" → hash("Alice") → 7 → bucket[7] contains ("Alice", value)
```

---

## Collision Resolution

Two keys hashing to the same index:

### Chaining (Java HashMap)

Each bucket is a linked list (or tree if > 8 collisions).

```
bucket[3]: ("Alice", 25) → ("Charlie", 30)  (same hash)
bucket[7]: ("Bob", 42)
```

```java
// Java HashMap uses chaining + red-black tree for large buckets
HashMap<String, Integer> map = new HashMap<>();
map.put("Alice", 25);
map.get("Alice");  // 25 — O(1) average
```

### Open Addressing

If bucket is taken, probe for next empty slot (linear probing, quadratic probing, double hashing).

---

## Key Concepts

| Concept | What It Means |
|---------|--------------|
| **Load factor** | entries / capacity. Default threshold = 0.75. When exceeded → resize (double capacity, rehash all). |
| **Hash function** | Maps key → integer. Must be deterministic, fast, uniform distribution. |
| **Rehashing** | When resizing, all entries are re-inserted. O(n) — but amortized over many inserts. |

```java
// Good hashCode() — uses all significant fields
@Override
public int hashCode() {
    return Objects.hash(name, email, age);
}

// Always override equals() when overriding hashCode()
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Person)) return false;
    Person p = (Person) o;
    return Objects.equals(name, p.name) 
        && Objects.equals(email, p.email)
        && age == p.age;
}
```

---

## Common Patterns

| Pattern | Data Structure | Example |
|---------|:-------------:|---------|
| **Count/frequency** | `Map<T, Integer>` | Character count, word frequency |
| **Two-sum** | `Map<value, index>` | `target - nums[i]` lookup |
| **Group by key** | `Map<K, List<V>>` | Group anagrams, group by category |
| **Cache / memoization** | `Map<input, output>` | Fibonacci memoization |
| **Duplicate detection** | `Set<T>` | Contains duplicate? First repeating? |
| **LRU Cache** | `LinkedHashMap` or `Map + DoublyLinkedList` | Evict least recently used |

```java
// Two Sum — O(n)
int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[]{map.get(complement), i};
        }
        map.put(nums[i], i);
    }
    return new int[]{};
}
```

---

## Hash Table vs Other Structures

| | Hash Table | Array | Tree (BST) |
|---|:---:|:---:|:---:|
| **Search** | O(1) avg | O(log n)* | O(log n) |
| **Insert** | O(1) avg | O(n) | O(log n) |
| **Ordered?** | ❌ | ✅ | ✅ |
| **Memory** | Extra (load factor) | Compact | Per-node overhead |

---

## Sources

- CLRS — Chapter 11
- Java HashMap source — https://github.com/openjdk/jdk
