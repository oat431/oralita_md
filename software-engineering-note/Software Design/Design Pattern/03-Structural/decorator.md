---
tags:
- design-patterns
- oop
- software-design
- software-engineering
---

> *Source: Dive Into Design Patterns by Alexander Shvets, "Decorator" (pp. 193–210)*

## Intent

> Decorator is a structural design pattern that lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.

Also known as: **Wrapper**

## Problem

Imagine a notification library centered on a `Notifier` class with a single `send` method that emails a list of recipients. Users soon demand SMS, Facebook, and Slack notifications. The straightforward fix—subclassing `Notifier` for each channel—works until someone asks: *"Why can't I use several notification types at once?"*

Creating subclasses for every combination (Email+SMS, Email+Slack, SMS+Facebook, all three, etc.) causes a **combinatorial explosion of subclasses**. The library and client code both bloat. Inheritance alone cannot scale this.

Two deeper limitations of inheritance make it the wrong tool:

- **Static.** You cannot alter an existing object's behavior at runtime—only replace the whole object with a different subclass instance.
- **Single-parent.** Most languages forbid inheriting behaviors from multiple classes simultaneously.

## Solution

Replace inheritance with **Aggregation** (or **Composition**): one object holds a reference to another and delegates work to it. The linked "helper" object can be swapped at runtime, and many helpers can be composed.

A **wrapper** (the alternative name for Decorator) implements the same interface as the wrapped object and delegates all requests to it. The wrapper may *alter the result* by doing something either before or after the delegation.

When the wrapper's reference field accepts *any* object following that interface, you can nest wrappers. The decorated object becomes a **stack**: the outermost decorator is what the client interacts with, but all layers share the same interface, so the client doesn't know or care how deep the stack goes.

In the notification example:
- Keep basic email behavior in the base `Notifier`.
- Turn SMS, Facebook, Slack into decorators.
- The client wraps a base notifier in whatever decorators match its preferences.

### Real-World Analogy

Wearing clothes. When cold, you put on a sweater. Still cold? Add a jacket. Raining? Add a raincoat. Each garment "extends" your behavior without becoming part of you, and you can remove any piece anytime.

## Structure


```mermaid
classDiagram
    class Component {
        <<interface>>
        +execute()
    }
    class ConcreteComponent {
        +execute()
    }
    class BaseDecorator {
        -wrappee: Component
        +BaseDecorator(Component)
        +execute()
    }
    class ConcreteDecoratorA {
        -addedState
        +execute()
    }
    class ConcreteDecoratorB {
        +execute()
        +addedBehavior()
    }
    Component <|.. ConcreteComponent
    Component <|.. BaseDecorator
    BaseDecorator <|-- ConcreteDecoratorA
    BaseDecorator <|-- ConcreteDecoratorB
    BaseDecorator o-- Component : wrappee
```

1. **Component** — declares the common interface for both wrappers and wrapped objects.
2. **Concrete Component** — the class being wrapped; defines basic behavior that decorators can alter.
3. **Base Decorator** — holds a reference to a wrapped object (typed as `Component` so it accepts both concrete components and other decorators). Delegates all operations to the wrappee.
4. **Concrete Decorators** — override base decorator methods to execute extra behavior before or after the parent call.
5. **Client** — wraps components in multiple layers of decorators; works with all objects via the Component interface.

## Pseudocode

Data source with encryption and compression decorators. The application wraps a `FileDataSource` with `EncryptionDecorator` and `CompressionDecorator`. Both wrappers change how data is written to and read from disk:

- **On write:** decorators encrypt and compress before passing data down the chain. The original `FileDataSource` writes the transformed data without knowing about the change.
- **On read:** data passes back through the same decorators, which decompress and decrypt it.

All classes implement the same `DataSource` interface, making them interchangeable.

```
// Component interface
interface DataSource is
    method writeData(data)
    method readData():data

// Concrete component
class FileDataSource implements DataSource is
    constructor FileDataSource(filename) { ... }
    method writeData(data) is
        // Write data to file.
    method readData():data is
        // Read data from file.

// Base decorator
class DataSourceDecorator implements DataSource is
    protected field wrappee: DataSource
    constructor DataSourceDecorator(source: DataSource) is
        wrappee = source
    method writeData(data) is
        wrappee.writeData(data)
    method readData():data is
        return wrappee.readData()

// Concrete decorator: Encryption
class EncryptionDecorator extends DataSourceDecorator is
    method writeData(data) is
        // 1. Encrypt passed data.
        // 2. Pass encrypted data to wrappee.writeData.
    method readData():data is
        // 1. Get data from wrappee.readData.
        // 2. Try to decrypt it if it's encrypted.
        // 3. Return the result.

// Concrete decorator: Compression
class CompressionDecorator extends DataSourceDecorator is
    method writeData(data) is
        // 1. Compress passed data.
        // 2. Pass compressed data to wrappee.writeData.
    method readData():data is
        // 1. Get data from wrappee.readData.
        // 2. Try to decompress it if it's compressed.
        // 3. Return the result.

// Client assembly — decorator stack built at runtime
class ApplicationConfigurator is
    method configurationExample() is
        source = new FileDataSource("salary.dat")
        if (enabledEncryption)
            source = new EncryptionDecorator(source)
        if (enabledCompression)
            source = new CompressionDecorator(source)

        logger = new SalaryManager(source)
        salary = logger.load()

// SalaryManager neither knows nor cares about data storage specifics
class SalaryManager is
    field source: DataSource
    constructor SalaryManager(source: DataSource) { ... }
    method load() is
        return source.readData()
    method save() is
        source.writeData(salaryRecords)
```

✅ Pseudocode from source.

## Applicability

| When | Why |
|------|-----|
| You need to **assign extra behaviors at runtime** without breaking existing client code | Decorator layers business logic into composable layers. Client code treats all objects uniformly via a common interface. |
| **Inheritance is awkward or impossible** (e.g., `final` classes) | Wrapping with a decorator is the only way to reuse behavior of a sealed class. |

## How to Implement

1. Model your domain as a primary component with multiple optional layers.
2. Identify methods common to all layers; declare them in a **component interface**.
3. Create a **concrete component** with the base behavior.
4. Create a **base decorator** with a `wrappee` field typed as the component interface; delegate all work to it.
5. Ensure **all classes implement the component interface**.
6. Create **concrete decorators** extending the base decorator; execute added behavior before or after calling the parent method.
7. **Client code** is responsible for creating and composing decorators.

## Pros and Cons

### ✅ Pros
- Extend an object's behavior **without making a new subclass**.
- **Add or remove responsibilities at runtime**.
- **Combine multiple behaviors** by wrapping an object in several decorators.
- **Single Responsibility Principle** — divide a monolithic class that implements many behavior variants into smaller, focused classes.

### ❌ Cons
- Hard to **remove a specific wrapper** from the middle of a stack.
- Hard to implement a decorator whose **behavior doesn't depend on order** in the stack.
- **Initial configuration code** for assembling layers can look ugly.

## Relations with Other Patterns

| Pattern | Relationship |
|---------|-------------|
| **Adapter** | Adapter provides a *different* interface to an existing object. Decorator keeps the same interface (or extends it) and supports recursive composition—which Adapter cannot do. |
| **Proxy** | Both share similar structure built on composition. Difference: Proxy *manages the lifecycle* of its service object; Decorator's composition is *always controlled by the client*. Proxy keeps the same interface; Decorator may enhance it. |
| **Chain of Responsibility** | Very similar class structures (recursive composition passing execution through a series of objects). Key difference: CoR handlers can execute *independent* operations and can *stop* the chain at any point. Decorators extend behavior *consistently* with the base interface and must **never break the request flow**. |
| **Composite** | Similar structure diagrams (recursive composition of open-ended objects). Decorator is like a Composite with only *one child*. Composite "sums up" children's results; Decorator *adds extra responsibilities*. They can cooperate: use Decorator to extend a specific object inside a Composite tree. |
| **Prototype** | Designs heavy on Composite and Decorator benefit from Prototype to clone complex structures instead of rebuilding them from scratch. |
| **Strategy** | Decorator changes the *skin* of an object; Strategy changes the *guts*. Decorator wraps from the outside; Strategy swaps internal algorithms. |

## Summary Checklist

- [ ] Business domain can be modeled as a **primary component + optional layers**.
- [ ] Defined a **Component interface** with methods common to all layers.
- [ ] **Concrete Component** implements base behavior.
- [ ] **Base Decorator** holds a wrappee reference (typed as Component) and delegates all calls.
- [ ] **Concrete Decorators** override methods, adding behavior before/after delegating.
- [ ] Client assembles decorators **at runtime** via the component interface.
- [ ] Inheritance-driven subclass explosion averted; behavior is now composable.

## Related

[[Composite]], [[Adapter]], [[Proxy]], [[chain-of-responsibility]], [[Strategy]], [[solid-principles]]
