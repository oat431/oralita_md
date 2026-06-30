---
tags:
- design-patterns
- oop
- software-design
- software-engineering
---

> *Source: Dive Into Design Patterns by Alexander Shvets, "Design Principles" (pp. 37–50)*

## Core Principle

> **Identify the aspects of your application that vary and separate them from what stays the same.**

---

## Encapsulate What Varies

The main goal is to minimize the effect caused by changes.

**Ship & Mine Analogy:** Imagine your program is a ship and changes are underwater mines. If the hull is one undivided compartment, one mine sinks the entire ship. If the hull is divided into independent compartments that can be sealed, damage is contained and the ship stays afloat. Isolate the parts that vary into independent modules to protect the rest of the code from adverse effects. Less time fixing = more time building features.

### Method-Level Encapsulation

Extract volatile logic into its own method. When a method mixes stable logic with code likely to change (e.g., tax formulas), pull the volatile part out.

```pseudocode
❌ BEFORE: tax calculation mixed with order total logic
method getOrderTotal(order) is
    total = 0
    foreach item in order.lineItems
        total += item.price * item.quantity

    if (order.country == "US")
        total += total * 0.07    // US sales tax
    else if (order.country == "EU"):
        total += total * 0.20    // European VAT

    return total
```

```pseudocode
✅ AFTER: tax logic extracted into a dedicated method
method getOrderTotal(order) is
    total = 0
    foreach item in order.lineItems
        total += item.price * item.quantity

    total += total * getTaxRate(order.country)

    return total

method getTaxRate(country) is
    if (country == "US")
        return 0.07   // US sales tax
    else if (country == "EU")
        return 0.20   // European VAT
    else
        return 0
```

Tax-related changes are now isolated. If the logic grows complex, it's a small step to extract it into a separate class.

### Class-Level Encapsulation

Over time, a method accumulates responsibilities and helper fields that blur the primary responsibility of the containing class. Extract everything tax-related into a dedicated `TaxCalculator` class. Objects of the `Order` class delegate all tax work to that specialized object. The `Order` class no longer knows how tax is calculated—it just delegates.

---

## Program to an Interface, not an Implementation

> Program to an interface, not an implementation. Depend on abstractions, not on concrete classes.

A design is flexible if you can extend it without breaking existing code. A cat that eats *any food* is more flexible than a cat that eats only sausages—you can still feed it sausages (they are a subset), but the menu is open to extension.

### Steps to Set Up Interface-Based Collaboration

1. Determine what exactly one object needs from the other: which methods does it execute?
2. Describe those methods in a new **interface or abstract class**.
3. Make the dependency class **implement** that interface.
4. Make the collaborating class depend on the **interface**, not the concrete class.

The code becomes *more complicated* upfront, but if it's a sensible extension point—or if others will extend it—the cost pays off.

### Example: Software Company Simulator

A `Company` class works with various employee types. Initially it's tightly coupled to concrete classes like `Designer`, `Programmer`, and `Tester`.

```pseudocode
❌ BEFORE: Company tightly coupled to concrete employee classes
class Company is
    field employees: array of Designer, Programmer, Tester

    method createSoftware() is
        // Directly instantiates and calls concrete classes
        d = new Designer()
        p = new Programmer()
        t = new Tester()
        d.designArchitecture()
        p.writeCode()
        t.testSoftware()
```

Step 1 — Extract a common `Employee` interface and use polymorphism:

```pseudocode
🔶 BETTER: polymorphism via Employee interface, but still coupled
interface Employee is
    method doWork()

class Designer implements Employee is
    method doWork() is designArchitecture()

class Programmer implements Employee is
    method doWork() is writeCode()

class Tester implements Employee is
    method doWork() is testSoftware()

class Company is
    field employees: array of Employee

    method createSoftware() is
        foreach e in employees
            e.doWork()
```

The `Company` class still knows about concrete employee classes when *creating* them. If new company types need different employees, you'd override most of `Company` instead of reusing code.

Step 2 — Abstract employee creation (Factory Method pattern):

```pseudocode
✅ AFTER: Company independent from concrete employee classes
abstract class Company is
    field employees: array of Employee

    // Factory Method — subclasses decide which employees to create
    abstract method getEmployees(): array of Employee

    method createSoftware() is
        employees = getEmployees()
        foreach e in employees
            e.doWork()

class GameDevCompany extends Company is
    method getEmployees() is
        return [new Designer(), new Programmer(), new Tester()]
```

Now `Company` is independent from concrete employee classes. You can introduce new company and employee types while reusing the base class logic. Existing code that relies on `Company` won't break.

---

## Favor Composition Over Inheritance

Inheritance is the most obvious way to reuse code, but it comes with serious caveats:

| Problem | Description |
|---|---|
| **Can't reduce interface** | Subclasses must implement all abstract methods of the parent, even unused ones |
| **Fragile base class** | Overriding methods must remain compatible with the base behavior—any code expecting the superclass may receive the subclass |
| **Breaks encapsulation** | Internal details of the parent become available to the subclass; superclass may become aware of subclass details |
| **Tight coupling** | Any change in the superclass may break subclass functionality |
| **Parallel hierarchies** | Reusing code across two or more dimensions explodes the class hierarchy into a combinatorial mess |

Inheritance = **"is a"** relationship (a car *is a* transport).  
Composition = **"has a"** relationship (a car *has an* engine).

> This principle also applies to **aggregation** — a relaxed variant of composition where one object references another but doesn't manage its lifecycle (a car *has a* driver, who may use another car or walk).

### Example: Car Manufacturer Catalog

A catalog app needs to represent cars and trucks, electric or gas, with manual or autopilot controls. Three dimensions: cargo type × engine type × navigation type.

```pseudocode
❌ INHERITANCE: combinatorial explosion of subclasses

class Transport is abstract
class Car extends Transport
class Truck extends Transport

// Two engine types × two vehicle types = 4 classes
class ElectricCar extends Car
class GasCar extends Car
class ElectricTruck extends Truck
class GasTruck extends Truck

// Add navigation dimension → 8 classes
class ManualElectricCar extends ElectricCar
class AutoElectricCar extends ElectricCar
class ManualGasCar extends GasCar
class AutoGasCar extends GasCar
class ManualElectricTruck extends ElectricTruck
// ... and so on. Each new dimension multiplies the hierarchy.
```

```pseudocode
✅ COMPOSITION: delegates behavior to interchangeable objects

interface Engine is
    method move()

class ElectricEngine implements Engine is
    method move() is // electric propulsion

class GasEngine implements Engine is
    method move() is // combustion propulsion

interface Navigation is
    method navigate()

class ManualControl implements Navigation is
    method navigate() is // driver steers

class Autopilot implements Navigation is
    method navigate() is // AI steers

class Transport is
    field engine: Engine
    field navigation: Navigation

    method setEngine(e: Engine) is
        engine = e          // swap at runtime

    method drive() is
        engine.move()
        navigation.navigate()
```

Instead of multiplying subclasses, `Transport` objects delegate to `Engine` and `Navigation` objects. Behaviors can be swapped at runtime by assigning a different engine or navigation object. This structure resembles the **Strategy** pattern.

---

## Summary Checklist

- [ ] **Encapsulate What Varies:** Is volatile logic isolated from stable code (method-level, class-level, or module-level)?
- [ ] **Program to an Interface:** Do collaborators depend on abstractions (interfaces/abstract classes) rather than concrete implementations?
- [ ] **Favor Composition Over Inheritance:** Are behaviors delegated to composable objects instead of locked into rigid inheritance hierarchies?
- [ ] Can you extend the design with new behavior without modifying existing code?
- [ ] Can you swap behaviors at runtime where needed?
- [ ] Are class hierarchies shallow and focused on a single dimension of variation?

---

## Related

- [[SOLID Principles]]
- [[Features of Good Design]]
- [[Introduction to OOP]]
- [[Strategy]]
- [[Decorator]]
- [[Adapter]]
