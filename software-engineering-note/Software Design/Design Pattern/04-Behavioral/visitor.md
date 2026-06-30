---
tags:
- design-patterns
- oop
- software-design
- software-engineering
---

> *Source: Dive Into Design Patterns by Alexander Shvets, "Visitor" (pp. 394–409)*

## Intent

> Visitor is a behavioral design pattern that lets you separate algorithms from the objects on which they operate.

---

## Problem

You maintain an app that models geographic data as a colossal graph. Nodes represent cities, industries, sightseeing areas — each node type is its own class, each specific node is an object.

A new requirement arrives: **export the entire graph to XML**. The naive solution is to add an `export()` method to every node class and recursively traverse the graph — polymorphism handles the dispatch cleanly.

**Three obstacles block this approach:**

1. **Production risk.** The system architect forbids altering existing node classes. The codebase is in production; any bug introduced by the new export logic could break the entire application.
2. **Misplaced responsibility.** XML export has nothing to do with the primary job of the node classes (geodata processing). Lodging export behavior there violates cohesion.
3. **Future churn.** After XML, marketing will demand JSON export, then CSV, then some unpredictable format. Every new behavior forces another change across all those fragile, production-critical classes.

The core tension: new behaviors need to be added to an existing class hierarchy, but modifying those classes is expensive, risky, or outright forbidden.

---

## Solution

The Visitor pattern moves new behavior into a **separate visitor class** rather than integrating it into existing element classes. The original object passes itself as an argument to a visitor method, giving that method access to all the object's data.

### The Dispatch Problem

A naive visitor needs one method per concrete element type (`doForCity`, `doForIndustry`, `doForSightSeeing`). But how do you call the *correct* method when iterating over a heterogeneous collection? Each method has a different signature — polymorphism can't help. Even method overloading (Java/C#) fails: the compiler resolves overloads at compile-time against the *declared* type, not the actual runtime class, so it always defaults to the base `Node` parameter.

### Double Dispatch

The Visitor pattern solves this with a technique called **Double Dispatch**:

1. The **client** calls `element.accept(visitor)` on any element, not knowing its concrete type.
2. Each **concrete element** implements `accept()` by calling the matching visitor method — e.g., `visitor.doForCity(this)`. Since the element knows its own class at compile time, the correct overload is resolved.
3. The **visitor** executes the appropriate behavior for that concrete element.

```
// Client — no type-checking required
foreach (Node node in graph)
    node.accept(exportVisitor)

// City element — redirects to the right visitor method
class City is
  method accept(Visitor v) is
    v.doForCity(this)

// Industry element
class Industry is
  method accept(Visitor v) is
    v.doForIndustry(this)
```

Yes, the element classes *are* modified — but the change is **trivial and one-time**: a single `accept()` method. From that point forward, any new behavior can be added by implementing a new visitor class, without touching the elements again.

> **Real-world analogy:** A seasoned insurance agent visits every building in a neighborhood. Depending on the type of organization occupying the building, he offers specialized policies: medical insurance for residential buildings, theft insurance for banks, fire/flood insurance for coffee shops. The agent (visitor) adapts his offer to each building type (element).

---

## Structure

| Role | Responsibility |
|---|---|
| **Visitor** | Interface declaring a set of visiting methods — one per concrete element class. Each method takes the corresponding concrete element as a parameter. |
| **Concrete Visitor** | Implements each visiting method with the actual algorithm tailored to each concrete element. Can accumulate internal state while traversing a complex structure (e.g., Composite tree). |
| **Element** | Interface declaring the `accept(visitor)` method. The parameter is typed to the Visitor interface. |
| **Concrete Element** | Implements `accept()` by calling `visitor.visitXxx(this)`. **Every subclass must override `accept()`**, even if the base class already implements it, to ensure the correct visitor method is dispatched. |
| **Client** | Holds a collection of elements (often a Composite tree). Iterates over elements and calls `element.accept(visitor)` without knowing the concrete element classes. |

```mermaid
classDiagram
    class Visitor {
        <<interface>>
        +visitDot(Dot)
        +visitCircle(Circle)
        +visitRectangle(Rectangle)
    }
    class ConcreteVisitor {
        +visitDot(Dot)
        +visitCircle(Circle)
        +visitRectangle(Rectangle)
    }
    class Element {
        <<interface>>
        +accept(Visitor)
    }
    class Dot {
        +accept(Visitor)
    }
    class Circle {
        +accept(Visitor)
    }
    class Rectangle {
        +accept(Visitor)
    }
    class Client
    Visitor <|.. ConcreteVisitor
    Element <|.. Dot
    Element <|.. Circle
    Element <|.. Rectangle
    Element --> Visitor : accept()
    Client --> Element
    Client --> ConcreteVisitor
```

---

## Pseudocode

> ✅ Pseudocode provided by source. XML export for geometric shapes using Visitor + Double Dispatch.

```
// The element interface declares an `accept` method
// that takes the base visitor interface as an argument.
interface Shape is
  method move(x, y)
  method draw()
  method accept(v: Visitor)

// Each concrete element class implements `accept`
// to call the visitor method matching its class.
class Dot implements Shape is
  // ...
  method accept(v: Visitor) is
    v.visitDot(this)

class Circle implements Shape is
  // ...
  method accept(v: Visitor) is
    v.visitCircle(this)

class Rectangle implements Shape is
  // ...
  method accept(v: Visitor) is
    v.visitRectangle(this)

class CompoundShape implements Shape is
  // ...
  method accept(v: Visitor) is
    v.visitCompoundShape(this)

// The Visitor interface declares a set of visiting methods
// corresponding to element classes.
interface Visitor is
  method visitDot(d: Dot)
  method visitCircle(c: Circle)
  method visitRectangle(r: Rectangle)
  method visitCompoundShape(cs: CompoundShape)

// Concrete visitor implements the same algorithm
// for each concrete element type.
class XMLExportVisitor implements Visitor is
  method visitDot(d: Dot) is
    // Export the dot's ID and center coordinates.

  method visitCircle(c: Circle) is
    // Export the circle's ID, center coordinates and radius.

  method visitRectangle(r: Rectangle) is
    // Export the rectangle's ID, left-top coordinates, width and height.

  method visitCompoundShape(cs: CompoundShape) is
    // Export the shape's ID as well as the list of its children's IDs.

// Client code — no type-checking, no conditionals
class Application is
  field allShapes: array of Shapes

  method export() is
    exportVisitor = new XMLExportVisitor()
    foreach (shape in allShapes) do
      shape.accept(exportVisitor)
```

**Key benefit with Composite:** When visiting a `CompoundShape`, the visitor can recursively call `accept()` on each child, leveraging the Composite tree. The visitor can also accumulate intermediate state (e.g., tracking nesting depth, building output buffer) across the traversal.

---

## Applicability

Use the Visitor pattern when:

- You need to **perform an operation on all elements of a complex object structure** (e.g., object tree, graph). The pattern gives you variants of the same operation for every target concrete class without iterative type-checking.
- You want to **clean up auxiliary behaviors** that don't belong in the primary classes. Extract reporting, exporting, validation, or formatting logic into visitors, keeping the element classes focused on their core responsibilities (**Single Responsibility Principle**).
- A behavior **makes sense only in some classes** of a hierarchy, not in others. You implement only the relevant `visitXxx` methods and leave the rest empty — no base-class pollution.

**Do not use when:**
- The element hierarchy is **unstable** — classes are frequently added or removed. Every change forces an update to *all* visitor interfaces and implementations.

---

## Pros and Cons

| ✅ Pros | ❌ Cons |
|---|---|
| **Open/Closed Principle.** Introduce new behavior that works with objects of different classes without modifying those classes. | You must **update all visitors** each time a class is added to or removed from the element hierarchy. |
| **Single Responsibility Principle.** Move multiple versions of the same behavior into a single visitor class. Element classes stay focused. | Visitors may lack **access to private fields and methods** of elements, forcing you to either break encapsulation or nest the visitor inside the element class (language-dependent). |
| Visitors can **accumulate state** while traversing a complex object structure — useful for collecting metrics, building output, or caching intermediate results. | The Double Dispatch mechanism requires adding `accept()` methods to all elements — a one-time invasive change, though trivial. |

---

## Relations with Other Patterns

| Pattern | Relationship |
|---|---|
| **Command** | Visitor is a more powerful version of Command. Visitor objects can execute operations over various objects of different classes, while Command typically wraps a single operation on a single receiver. |
| **Composite** | Use Visitor to execute an operation over an entire Composite tree. The visitor traverses children recursively and can accumulate state across the structure. |
| **Iterator** | Combine with Iterator to traverse a complex data structure and execute visitor operations over its elements, even when those elements have different classes. |

---

## Summary Checklist

- [ ] Can you define a stable set of concrete element classes that won't change frequently?
- [ ] Does the new behavior make sense across a heterogeneous collection of objects?
- [ ] Is the behavior unrelated to the primary responsibility of the element classes (export, validation, reporting)?
- [ ] Have you declared a `visitXxx()` method for **every** concrete element class in the Visitor interface?
- [ ] Does every concrete element implement `accept()` by calling the correct `visitXxx(this)` — including subclasses that must override their parent's `accept()`?
- [ ] Can the visitor accumulate intermediate state across the traversal (e.g., with a Composite tree)?
- [ ] Have you handled encapsulation — either by making necessary fields public or nesting the visitor inside the element?
- [ ] Is the client code free of `instanceof` checks and conditionals when dispatching to elements?

---

## Related

[[Iterator]] | [[Composite]] | [[Command]] | [[Strategy]] | [[State]] | [[SOLID Principles]]
