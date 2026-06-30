---
tags:
- algorithms
- data-structures
- programming
---

# 01 Trees & BSTs

Trees are hierarchical data structures. Every node has a value and references to children. The most important tree variants: binary trees, BSTs, and tries.

---

## Binary Tree

Each node has at most 2 children.

```java
class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}
```

### Traversals

```
        1
       / \
      2   3
     / \
    4   5

Pre-order:  [1, 2, 4, 5, 3]   (node → left → right)
In-order:   [4, 2, 5, 1, 3]   (left → node → right)  ← BST sorted order
Post-order: [4, 5, 2, 3, 1]   (left → right → node)
Level-order:[1, 2, 3, 4, 5]   (BFS)
```

```java
// In-order (recursive)
void inorder(TreeNode root) {
    if (root == null) return;
    inorder(root.left);
    System.out.println(root.val);
    inorder(root.right);
}

// Level-order (BFS)
void levelOrder(TreeNode root) {
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    while (!q.isEmpty()) {
        TreeNode node = q.poll();
        System.out.println(node.val);
        if (node.left != null) q.offer(node.left);
        if (node.right != null) q.offer(node.right);
    }
}
```

---

## Binary Search Tree (BST)

Left subtree < node < right subtree. Enables O(log n) search, insert, delete (when balanced).

```java
TreeNode search(TreeNode root, int target) {
    if (root == null || root.val == target) return root;
    return target < root.val 
        ? search(root.left, target) 
        : search(root.right, target);
}
```

| Operation | Average | Worst (skewed) |
|-----------|:-------:|:-------------:|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

### Self-Balancing BSTs

| Tree | Balancing Rule | Use |
|------|---------------|-----|
| **AVL** | Height difference ≤ 1 | Fast lookups, frequent reads |
| **Red-Black** | Color rules + rotations | Balanced insert/delete, Java `TreeMap` |

---

## Trie (Prefix Tree)

Tree for strings. Each node represents a character. Root is empty.

```
Words: ["cat", "car", "dog"]

        root
       /    \
      c      d
      |      |
      a      o
     / \     |
    t   r    g
```

```java
class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    boolean isEndOfWord;
}

void insert(TrieNode root, String word) {
    TrieNode curr = root;
    for (char c : word.toCharArray()) {
        curr = curr.children.computeIfAbsent(c, k -> new TrieNode());
    }
    curr.isEndOfWord = true;
}
```

| Use Case | How |
|----------|-----|
| **Autocomplete** | Walk trie from prefix, collect all words |
| **Spell checker** | Edit distance + trie traversal |
| **IP routing** | Longest prefix match |

---

## Sources

- CLRS — Chapters 12, 13
- Sedgewick — Chapter 3 (Trees)
