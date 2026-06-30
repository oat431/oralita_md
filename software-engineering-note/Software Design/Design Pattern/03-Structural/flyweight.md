---
tags:
- design-patterns
- oop
- software-design
- software-engineering
---

> *Source: Dive Into Design Patterns by Alexander Shvets, "Flyweight" (pp. 221–234)*

## Intent

> Flyweight is a structural design pattern that lets you fit more objects into the available amount of RAM by sharing common parts of state between multiple objects instead of keeping all of the data in each object.

## Problem

Suppose you build a video game with a realistic particle system—bullets, missiles, and shrapnel flying everywhere. Each particle is a separate object holding coordinates, movement vectors, speed, **color**, and **sprite** data. On your powerful machine it runs fine. Your friend's weaker rig crashes after minutes: thousands of particle objects exhaust RAM.

The root cause: every particle duplicates the **same** color and sprite data. A hundred bullets each carry their own copy of identical texture bytes. This redundancy blows up memory when object counts climb into the thousands.

## Solution

The Flyweight pattern separates object state into two categories:

| State | Definition | Example (Particle) |
|---|---|---|
| **Intrinsic** | Constant, shared across many instances; never changes after creation | Color, sprite/texture |
| **Extrinsic** | Unique per instance; changes over time; supplied from outside | Coordinates, velocity, speed |

1. **Keep intrinsic state inside the flyweight object.** It initializes once via constructor and never exposes setters or mutable public fields.
2. **Move extrinsic state outside.** The client stores or calculates it and passes it as method parameters whenever the flyweight is used.
3. **Context class** bundles extrinsic state with a reference to its flyweight, so the container (e.g., `Game`) holds one array of small context objects instead of parallel arrays.
4. **Flyweight Factory** maintains a pool of existing flyweights. Clients request a flyweight by intrinsic state; the factory returns a cached match or creates one. This avoids duplicate flyweights for the same intrinsic data.

Result: where you once needed thousands of heavy particle objects, you now need only **one flyweight per type** (bullet, missile, shrapnel) plus thousands of tiny context objects carrying just coordinates and a flyweight reference.

## Structure

- **Flyweight** — stores intrinsic state (shared, immutable). Methods accept extrinsic state as parameters.
- **Context** — holds extrinsic state unique to each original object + a reference to the corresponding Flyweight. Together they represent the full original object.
- **Flyweight Factory** — manages a pool/cache of flyweights. Returns existing flyweight matching the requested intrinsic state or creates a new one.
- **Client** — calculates/stores extrinsic state and uses the factory to obtain flyweights. From the client's view, a flyweight is a template object configured at runtime via method parameters.

```mermaid
classDiagram
    class Flyweight {
        -intrinsicState
        +operation(extrinsicState)
    }
    class FlyweightFactory {
        -flyweights: Map
        +getFlyweight(key) Flyweight
    }
    class Context {
        -extrinsicState
        -flyweight: Flyweight
        +operation()
    }
    class Client
    FlyweightFactory --> Flyweight : creates/caches
    Context o-- Flyweight
    Client --> FlyweightFactory
    Client --> Context
```

## Pseudocode

This example renders millions of trees on a forest canvas. Without Flyweight, each `Tree` duplicates texture and color data. With Flyweight, the repeating data lives in shared `TreeType` objects.

```java
// Flyweight class — stores intrinsic state (shared, immutable)
class TreeType is
    field name
    field color
    field texture
    constructor TreeType(name, color, texture) { ... }
    method draw(canvas, x, y) is
        // 1. Create a bitmap of a given type, color & texture.
        // 2. Draw the bitmap on the canvas at X and Y coords.

// Flyweight factory — pool of existing tree types
class TreeFactory is
    static field treeTypes: collection of tree types
    static method getTreeType(name, color, texture) is
        type = treeTypes.find(name, color, texture)
        if (type == null)
            type = new TreeType(name, color, texture)
            treeTypes.add(type)
        return type

// Context — extrinsic state (coordinates) + flyweight reference
class Tree is
    field x, y
    field type: TreeType
    constructor Tree(x, y, type) { ... }
    method draw(canvas) is
        type.draw(canvas, this.x, this.y)

// Client — uses factory to plant trees, deferring type lookup/reuse
class Forest is
    field trees: collection of Trees

    method plantTree(x, y, name, color, texture) is
        type = TreeFactory.getTreeType(name, color, texture)
        tree = new Tree(x, y, type)
        trees.add(tree)

    method draw(canvas) is
        foreach (tree in trees) do
            tree.draw(canvas)
```

✅ Pseudocode is directly from the source (Java-like). The `Forest` client calls `TreeFactory.getTreeType()` which caches `TreeType` flyweights. Each `Tree` context object is only two integers + one reference—millions can fit where a few thousand full objects would OOM.

## Applicability

Use Flyweight **only** when all of these hold:

- The application must spawn a **huge number** of similar objects.
- Available **RAM** on the target device is the bottleneck.
- The objects contain **duplicate state** that can be extracted and shared across multiple instances.

Do **not** reach for Flyweight preemptively—it trades simplicity for memory. Apply it only after profiling confirms a real RAM problem that can't be solved another way.

## Pros and Cons

| ✅ Pros | ❌ Cons |
|---|---|
| Saves enormous amounts of RAM when many similar objects exist | May trade RAM for CPU: extrinsic data may need recalculation each time a flyweight method is called |
| Centralizes shared state — one change to a flyweight type propagates to all users | Code becomes much more complicated; new team members will wonder why entity state was split this way |
| Factory ensures no duplicate flyweights for the same intrinsic state | Only pays off at scale; adds overhead for small object counts |

## How to Implement

1. **Divide fields** of the target class into intrinsic (unchanging, duplicated) and extrinsic (contextual, unique).
2. **Leave intrinsic fields** in the class; make them **immutable** (initialized only in constructor, no setters).
3. **Refactor methods** that use extrinsic fields: add parameters to inject extrinsic state from the caller instead of reading from fields.
4. **Create a Flyweight Factory** that caches flyweights by intrinsic state. Clients must request flyweights only through the factory.
5. **Store extrinsic state** in the client or a separate **Context** class that pairs extrinsic data with a flyweight reference.

## Relations with Other Patterns

- **[[Composite]]** — Shared leaf nodes of a Composite tree can be implemented as Flyweights to save RAM.
- **[[Facade]]** — Conceptual opposite: Flyweight creates many little shared objects; Facade creates one object representing an entire subsystem.
- **[[Singleton]]** — Flyweight would resemble Singleton if all shared state reduced to exactly one flyweight object. Key differences: (1) Singleton has one instance; Flyweight can have multiple instances with different intrinsic states. (2) Singleton *can* be mutable; Flyweight objects are **immutable**.
- **[[Command]]** — Flyweight can help reduce memory when storing many Command objects with shared parts.
- **[[State]]** and **[[Strategy]]** — Flyweight objects are natural fits for State/Strategy instances that appear in large numbers; the same state/strategy object can be shared across many contexts.

## Summary Checklist

- [x] Flyweight splits object state into **intrinsic** (shared, immutable) and **extrinsic** (unique, passed in)
- [x] **Flyweight Factory** caches and reuses flyweights by intrinsic state
- [x] **Context** bundles extrinsic state with a flyweight reference
- [x] Flyweight objects are **immutable** — no setters, no public mutable fields
- [x] Apply only when **RAM is proven bottleneck** from massive numbers of similar objects
- [x] Principal tradeoff: memory savings vs. code complexity + potential CPU overhead
- [x] Related: Composite (shared leaves), Singleton (one vs. many, mutable vs. immutable), State/Strategy (shared instances)

## Related

- [[Composite]]
- [[Singleton]]
- [[Proxy]]
- [[Command]]
- [[State]]
- [[Strategy]]
- [[SOLID Principles]]
