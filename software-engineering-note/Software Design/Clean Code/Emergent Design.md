---
tags:
- clean-code
- software-design
- software-engineering
---

# Emergent Design

*Clean Code — Robert C. Martin (by Jeff Langr), pp. 171–176*

> "The fact that we have these tests eliminates the fear that cleaning up the code will break it!"

## Kent Beck's Four Rules of Simple Design

A design is "simple" if it satisfies these rules **in order of priority**:

1. **Runs all the tests** — the system must be verifiably correct.
2. **Contains no duplication** — the primary enemy of good design.
3. **Expresses the intent of the programmer** — code as communication.
4. **Minimizes the number of classes and methods** — avoid pointless dogmatism.

Following these rules in priority order creates pressure toward good object-oriented design—low coupling, high cohesion, SRP, and DIP—without requiring deep upfront expertise.

---

### 1. Runs All the Tests

A design is worthless if the system cannot be verified. A comprehensively tested system that passes all tests continuously is a **testable** system.

**Writing tests pushes design toward better structure:**

- Testable classes tend to be **small and single-purpose** (SRP).
- The more tests you write, the more you reach for **DIP**, dependency injection, interfaces, and abstraction to reduce coupling.
- Tests create a **safety net** that eliminates fear of refactoring.

> Tests are the enabler. Without them, refactoring is gambling. With them, refactoring is engineering.

**Key takeaway:** Write tests first and run them continuously. Tests don't just verify behaviour—they actively shape better design.

---

### 2. No Duplication

Duplication is the **primary enemy** of a well-designed system. It creates extra work, extra risk, and unnecessary complexity.

**Duplication takes many forms:**

- Identical lines of code.
- Similar lines that can be massaged to match, then unified.
- Duplication of **implementation** (e.g. `isEmpty()` implemented independently from `size()`).

#### Before — Duplication of Implementation

```java
int size() { return counter; }
boolean isEmpty() { return flag; }   // separate tracking — duplication
```

#### After — Tied to Canonical Definition

```java
int size() { return counter; }
boolean isEmpty() {
    return 0 == size();               // no duplication of logic
}
```

#### Before — Duplicated Cleanup Logic

```java
public void scaleToOneDimension(float desiredDimension, float imageDimension) {
    if (Math.abs(desiredDimension - imageDimension) < errorThreshold)
        return;
    float scalingFactor = desiredDimension / imageDimension;
    scalingFactor = (float)(Math.floor(scalingFactor * 100) * 0.01f);
    RenderedOp newImage = ImageUtilities.getScaledImage(
        image, scalingFactor, scalingFactor);
    image.dispose();
    System.gc();
    image = newImage;
}

public synchronized void rotate(int degrees) {
    RenderedOp newImage = ImageUtilities.getRotatedImage(
        image, degrees);
    image.dispose();                  // duplicated
    System.gc();                      // duplicated
    image = newImage;                 // duplicated
}
```

#### After — Extracted Commonality

```java
public void scaleToOneDimension(float desiredDimension, float imageDimension) {
    if (Math.abs(desiredDimension - imageDimension) < errorThreshold)
        return;
    float scalingFactor = desiredDimension / imageDimension;
    scalingFactor = (float)(Math.floor(scalingFactor * 100) * 0.01f);
    replaceImage(ImageUtilities.getScaledImage(
        image, scalingFactor, scalingFactor));
}

public synchronized void rotate(int degrees) {
    replaceImage(ImageUtilities.getRotatedImage(image, degrees));
}

private void replaceImage(RenderedOp newImage) {
    image.dispose();
    System.gc();
    image = newImage;
}
```

**Why tiny extractions matter:** As you extract commonality, you start noticing SRP violations. A new method can be moved to another class, elevating its visibility. Someone else may reuse it. "Reuse in the small" is the foundation of reuse in the large.

---

#### The TEMPLATE METHOD Pattern Emerges Naturally

When you eliminate duplication across methods that follow the same algorithm with one varying step, the **TEMPLATE METHOD** pattern surfaces naturally.

```java
// BEFORE — near-identical methods, differing only in legal-minimum logic
public class VacationPolicy {
    public void accrueUSDivisionVacation() {
        // calculate vacation based on hours worked
        // ensure vacation meets US minimums      ← only this differs
        // apply vacation to payroll record
    }
    public void accrueEUDivisionVacation() {
        // calculate vacation based on hours worked
        // ensure vacation meets EU minimums      ← only this differs
        // apply vacation to payroll record
    }
}
```

```java
// AFTER — TEMPLATE METHOD: invariant steps in base class, variant in subclass
abstract public class VacationPolicy {
    public void accrueVacation() {                // template method
        calculateBaseVacationHours();
        alterForLegalMinimums();                  // "hole" filled by subclass
        applyToPayroll();
    }
    private void calculateBaseVacationHours() { /* ... */ }
    abstract protected void alterForLegalMinimums();
    private void applyToPayroll() { /* ... */ }
}

public class USVacationPolicy extends VacationPolicy {
    @Override protected void alterForLegalMinimums() {
        // US specific logic
    }
}

public class EUVacationPolicy extends VacationPolicy {
    @Override protected void alterForLegalMinimums() {
        // EU specific logic
    }
}
```

> Refactoring to eliminate duplication doesn't just clean code—it **reveals abstractions** that were hiding in plain sight.

---

### 3. Expressive

Code is read far more often than it is written. The majority of a software project's cost is in **long-term maintenance**. When you're deep in a problem, your own code seems obvious—but the next maintainer lacks that context.

**Make intent unmistakable:**

- **Good names** — a class or function name should never surprise the reader when they discover what it actually does.
- **Small functions and classes** — small things are easy to name, easy to write, and easy to understand.
- **Standard nomenclature** — use pattern names like COMMAND, VISITOR, or TEMPLATE METHOD in class names. They communicate design intent to anyone familiar with the Gang of Four.
- **Well-written unit tests** — tests are **documentation by example**. A reader should be able to understand what a class does by reading its tests.
- **Try.** The most important technique is simply to care. Choose better names, split large functions, and take pride in workmanship. The next person reading your code is probably you.

> "Care is a precious resource."

---

### 4. Minimal Classes and Methods

Even good principles—eliminating duplication, expressiveness, SRP—can be taken too far. Low priority doesn't mean unimportant; it means **don't sacrifice higher-priority rules for this one.**

**Avoid dogmatism:**

| Dogma | Pragmatic Alternative |
|---|---|
| Interface for every single class | Create interfaces only when there's a real abstraction or need for polymorphism |
| Always separate fields and behaviour into data classes + behaviour classes | Group data and the behaviour that operates on it together; that's encapsulation |
| Splitting every tiny concern into its own class | Ask whether the split improves clarity or just scatters related logic |

**The balancing act:** Keep the overall system small while keeping functions and classes small. But if you must choose between fewer classes and better expressiveness, **choose expressiveness.** If fewer classes means more duplication, **eliminate the duplication.**

This rule is last for a reason. A system with tests, no duplication, and clear intent is already well-designed. Obsessing over class counts at the expense of those three is counterproductive.

---

## How the Rules Work Together

```
   Rule 1: Runs All Tests
         │
         ▼
   Enables safe refactoring
         │
         ▼
   Rule 2: No Duplication ──▶ reveals abstractions, SRP violations, patterns
         │
         ▼
   Rule 3: Expressive ──▶ good names, small functions, tests as docs
         │
         ▼
   Rule 4: Minimal Classes/Methods ──▶ pragmatic restraint, avoid over-engineering
```

Each rule creates pressure toward the next. Tests enable fearless refactoring. Refactoring eliminates duplication. Eliminating duplication surfaces meaningful abstractions. Clear abstractions are easier to name and express. And all of this is done with pragmatic restraint—no more code than necessary.

---

## Checklist: Emergent Design

- [ ] All tests pass and run continuously—the system is verifiable.
- [ ] No duplicated code. Not even a few lines. Not even duplicated implementation logic (`isEmpty()` vs `size()`).
- [ ] No duplicated algorithm structure—TEMPLATE METHOD or STRATEGY used where appropriate.
- [ ] Class and function names clearly convey intent; no surprises on inspection.
- [ ] Functions and classes are small and single-purpose.
- [ ] Unit tests serve as readable documentation by example.
- [ ] Standard pattern names used in class names where patterns are applied.
- [ ] Every function and class has been reviewed for expressiveness before moving on.
- [ ] Class and method count is kept low **without** sacrificing tests, deduplication, or clarity.
- [ ] No interfaces-for-the-sake-of-interfaces, no gratuitous data/behaviour separation.

---

## Related Notes

- [[Clean Code Principles]] — overarching values and mindset
- [[Function Design]] — small functions, single responsibility, descriptive names
- [[Class Design & SOLID]] — SRP, DIP, dependency injection, interfaces
- [[Unit Testing]] — tests as safety net, documentation, and design pressure
- [[Code Smells Catalog]] — recognising duplication, rigidity, opacity before they metastasise
- [[Design Patterns]] — TEMPLATE METHOD, STRATEGY, and other patterns that emerge from refactoring
