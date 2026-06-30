---
tags:
- design-patterns
- oop
- software-design
- software-engineering
---

> *Source: Dive Into Design Patterns by Alexander Shvets, "Strategy" (pp. 369–381)*

## Intent

> Strategy is a behavioral design pattern that lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable.

## Problem

A **navigation app** starts simple: build road routes for cars. Then walking routes are added. Then public transport. Cyclists. Tourist attractions. With each new routing algorithm, the main navigator class **doubles in size**.

```java
class Navigator is
    method buildRoute(origin, destination, mode) is
        if (mode == "driving")
            // 200 lines of road-routing logic
        else if (mode == "walking")
            // 200 lines of pedestrian-routing logic
        else if (mode == "transit")
            // 200 lines of public-transport logic
        // ... more modes keep piling on
```

**The core weaknesses:**

- **Any change to one algorithm** — a bug fix, a tweak to street scoring — risks breaking already-working algorithms in the same class.
- **Merge conflicts multiply.** Multiple developers implementing different routing features all touch the same massive class simultaneously.
- **The class becomes unmaintainable.** At a certain size, no one fully understands it anymore.

The code doesn't just grow — it becomes a **brittle monolith** where fear of change stifles development.

## Solution

The Strategy pattern says: **extract each algorithm into its own class, called a strategy.**

1. Create a **strategy interface** that declares a single method — e.g., `buildRoute(origin, destination)` — common to all routing algorithms.
2. Implement each algorithm as a **concrete strategy class** (`RoadStrategy`, `WalkingStrategy`, `PublicTransportStrategy`).
3. The original class, now called the **context**, stores a **reference to one strategy** and delegates all algorithm work to it.
4. The **client** passes the desired strategy to the context. The context doesn't know *which* strategy it holds or *how* it works; it only knows the interface.

> **Real-world analogy:** Getting to the airport — you can catch a bus, order a cab, or ride a bicycle. Each is a transportation *strategy*. You pick one based on budget, time, or preference. The destination doesn't change; the *how* does.

In the navigation app, the main `Navigator` class no longer contains any routing logic. It simply calls `strategy.buildRoute(origin, destination)` and renders the returned checkpoints on the map. Swapping strategies becomes a one-liner: `navigator.setStrategy(new WalkingStrategy())`.

The context becomes **independent of concrete strategies**. Add a new algorithm? Write a new class implementing the interface — no changes to the context or other strategies. The **Open/Closed Principle** holds.

## Structure

```mermaid
classDiagram
    class Context {
        -strategy: Strategy
        +setStrategy(Strategy)
        +doSomething()
    }
    class Strategy {
        <<interface>>
        +execute(data)
    }
    class ConcreteStrategyA {
        +execute(data)
    }
    class ConcreteStrategyB {
        +execute(data)
    }
    class Client
    Context --> Strategy : delegates to
    Strategy <|.. ConcreteStrategyA
    Strategy <|.. ConcreteStrategyB
    Client --> ConcreteStrategyA : creates
    Client --> Context : configures
```

1. **Context** — Maintains a reference to a concrete strategy. Communicates with it *only* via the strategy interface. Exposes a setter to replace the strategy at runtime.
2. **Strategy interface** — Declares a method (or methods) common to all algorithm variants. The context uses this method to trigger the algorithm.
3. **Concrete Strategies** — Each implements a distinct variant of the algorithm. They share the same interface, making them interchangeable.
4. **Client** — Creates a specific strategy object and passes it to the context. Must be aware of the differences between strategies to select the right one.

## Pseudocode

```java
// The strategy interface declares operations common to all
// supported versions of some algorithm. The context uses this
// interface to call the algorithm defined by the concrete
// strategies.
interface Strategy is
    method execute(a, b)

// Concrete strategies implement the algorithm while following
// the base strategy interface. The interface makes them
// interchangeable in the context.
class ConcreteStrategyAdd implements Strategy is
    method execute(a, b) is
        return a + b

class ConcreteStrategySubtract implements Strategy is
    method execute(a, b) is
        return a - b

class ConcreteStrategyMultiply implements Strategy is
    method execute(a, b) is
        return a * b

// The context defines the interface of interest to clients.
class Context is
    // The context maintains a reference to one of the strategy
    // objects. The context doesn't know the concrete class of a
    // strategy. It should work with all strategies via the
    // strategy interface.
    private field strategy: Strategy

    // Usually the context accepts a strategy through the
    // constructor, and also provides a setter so that the
    // strategy can be switched at runtime.
    method setStrategy(Strategy strategy) is
        this.strategy = strategy

    // The context delegates some work to the strategy object
    // instead of implementing multiple versions of the
    // algorithm on its own.
    method executeStrategy(int a, int b) is
        return strategy.execute(a, b)

// The client code picks a concrete strategy and passes it to
// the context. The client should be aware of the differences
// between strategies in order to make the right choice.
class ExampleApplication is
    method main() is
        Create context object.

        Read first number.
        Read second number.
        Read the desired action from user input.

        if (action == addition) then
            context.setStrategy(new ConcreteStrategyAdd())

        if (action == subtraction) then
            context.setStrategy(new ConcreteStrategySubtract())

        if (action == multiplication) then
            context.setStrategy(new ConcreteStrategyMultiply())

        result = context.executeStrategy(First number, Second number)

        Print result.
```

✅ *Pseudocode reproduced from source.*

## Applicability

- **Use when you need different algorithm variants and want to switch them at runtime.** The Strategy pattern lets you indirectly alter an object's behavior by associating it with different sub-objects that perform specific sub-tasks in different ways.
- **Use when you have many similar classes that differ only in how they execute some behavior.** Extract the varying behavior into a strategy hierarchy and collapse the original classes into one, reducing code duplication.
- **Use to isolate business logic from algorithm implementation details.** Various algorithms' code, internal data, and dependencies are hidden behind the strategy interface. Clients get a simple interface to execute and switch algorithms at runtime.
- **Use when a class has a massive conditional statement that switches between algorithm variants.** Extract each branch into a separate strategy class. The original object delegates to one of these objects instead of implementing all variants itself.

## How to Implement

1. **Identify the algorithm** in the context class that's prone to frequent changes or implemented as a massive conditional selecting variants at runtime.
2. **Declare the strategy interface** common to all variants of the algorithm.
3. **Extract each algorithm** into its own concrete strategy class implementing the interface.
4. **Add a strategy reference field** in the context, with a setter. The context must work with the strategy *only* via the interface. Optionally, define a data-access interface so strategies can pull data from the context.
5. **Clients associate the context** with a strategy that matches how they want the context to perform its primary job.

## Pros and Cons

| ✅ Pros | ❌ Cons |
|---|---|
| **Swap algorithms at runtime.** Replace behavior by swapping strategy objects. | **Overkill for few, rarely-changing algorithms.** Extra classes and interfaces add unnecessary complexity for trivial cases. |
| **Isolate algorithm implementation details** from the code that uses them. | **Clients must understand strategy differences** to select the right one. The abstraction leaks one layer up. |
| **Replace inheritance with composition.** Behavior varies by object reference, not by subclassing. | **Functional alternatives exist.** Modern languages support anonymous functions/lambdas that achieve the same effect without extra classes and interfaces. |
| **Open/Closed Principle.** New strategies can be introduced without modifying the context or existing strategies. | |

## Relations with Other Patterns

- **Bridge**, **State**, **Strategy** (and to some degree **Adapter**) share very similar structures — all are based on **composition** (delegating work to other objects). But they solve *different* problems. A pattern isn't just a code structure recipe; it communicates the problem being solved.
- **Command and Strategy** may look similar because both parameterize an object with some action. However:
  - **Command** converts *any* operation into an object. The operation's parameters become fields. This enables deferred execution, queuing, command history, and remote dispatch.
  - **Strategy** describes *different ways of doing the same thing*, letting you swap algorithms within a single context class.
- **Decorator** changes the **skin** of an object; **Strategy** changes the **guts**.
- **Template Method** is based on **inheritance**: it alters parts of an algorithm by extending those parts in subclasses. It works at the **class level**, so it's static. **Strategy** is based on **composition**: you alter parts of behavior by supplying different strategy objects. It works at the **object level**, letting you switch behaviors at **runtime**.
- **State** can be considered an **extension of Strategy**. Both change context behavior by delegating to helper objects via composition. **Strategy** makes helper objects completely **independent and unaware** of each other. **State** does *not* restrict dependencies between concrete states — it lets them alter the context's state at will.

## Summary Checklist

- [ ] Identify the **algorithm** in the context class prone to change or inflated with conditionals
- [ ] Declare a **strategy interface** with a method common to all algorithm variants
- [ ] Extract each algorithm variant into a **concrete strategy class**
- [ ] Add a **strategy reference field** and a **setter** in the context
- [ ] **Delegate** context work to the strategy via the interface only
- [ ] Client creates and injects the appropriate **concrete strategy**
- [ ] Verify strategies are **independent** of each other and the context
- [ ] New strategies can be added **without modifying** the context or existing strategies (OCP)
- [ ] Prefer Strategy over inheritance when algorithm variants need to change at runtime
- [ ] Consider **functional alternatives** (lambdas, first-class functions) when the language supports them and the number of strategies is small

## Related

- [[State]] — Shares the composition + delegation structure. Strategy keeps strategies independent; State allows concrete states to know and transition between each other.
- [[Bridge]] — Similar delegation structure, but Bridge separates orthogonal dimensions (abstraction vs. implementation); Strategy swaps interchangeable behaviors.
- [[Command]] — Both parameterize objects with actions. Command wraps operations for deferred execution and history; Strategy swaps algorithmic behavior at runtime.
- [[Template Method]] — Inheritance-based alternative: Template Method defines a skeleton at class level (static); Strategy uses composition at object level (runtime-swappable).
- [[Decorator]] — Strategy changes the "guts" (core behavior); Decorator changes the "skin" (adds wrapping layers without altering the core interface).
- [[SOLID Principles]] — Strategy directly embodies the Open/Closed Principle: new algorithms are added by creating classes, not by modifying the context.
