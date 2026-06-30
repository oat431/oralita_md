---
tags:
- clean-code
- software-design
- software-engineering
---

# Objects vs Data Structures

> *Source: Clean Code — Chapter 6, Robert C. Martin*

> **"Objects hide their data behind abstractions and expose functions that operate on that data. Data structures expose their data and have no meaningful functions."**

---

## The Core Trade-Off

| | Objects | Data Structures |
|---|---|---|
| **What they expose** | Behavior (methods) | Data (public fields) |
| **What they hide** | Data (private state) | Behavior (none meaningful) |
| **Easy to add** | New types (without changing existing functions) | New functions (without changing existing types) |
| **Hard to add** | New functions (must change all classes) | New types (must change all functions) |

The things that are hard for OO are easy for procedures, and the things that are hard for procedures are easy for OO. Mature programmers know **"everything is an object" is a myth.**

---

### Rule 1: **Hiding Implementation Is About Abstractions, Not Getters**

A class does not simply push variables through getters and setters. It exposes abstract interfaces that allow users to manipulate the *essence* of the data without knowing its implementation.

```java
// BEFORE — Concrete: exposes implementation detail
public interface Vehicle {
    double getFuelTankCapacityInGallons();
    double getGallonsOfGasoline();
}
```

```java
// AFTER — Abstract: hides implementation completely
public interface Vehicle {
    double getPercentFuelRemaining();
}
```

The abstract version tells you nothing about the data form. The caller asks *what* they want to know, not *how* it's stored.

```java
// BEFORE — Concrete: forces rectangular coordinate usage
public class Point {
    public double x;
    public double y;
}
```

```java
// AFTER — Abstract: could be rectangular or polar; you can't tell
public interface Point {
    double getX();
    double getY();
    void setCartesian(double x, double y);
    double getR();
    double getTheta();
    void setPolar(double r, double theta);
}
```

Adding getters and setters to every field is **not** abstraction. It's the same exposure with a ceremony wrapper. Serious thought goes into *how* to represent the data, not just *what* the variables are.

---

### Rule 2: **Choose Object or Data Structure Deliberately — Not Both**

**Procedural code** (code that uses data structures) makes it easy to add new functions without changing existing data structures. Adding a new data type requires changing every function.

```java
// PROCEDURAL — Shapes are dumb data, Geometry has all the behavior
public class Square  { public Point topLeft; public double side; }
public class Rectangle { public Point topLeft; public double height, width; }
public class Circle    { public Point center; public double radius; }

public class Geometry {
    public double area(Object shape) throws NoSuchShapeException {
        if (shape instanceof Square s)      return s.side * s.side;
        else if (shape instanceof Rectangle r) return r.height * r.width;
        else if (shape instanceof Circle c)    return PI * c.radius * c.radius;
        throw new NoSuchShapeException();
    }
}
```

**OO code** makes it easy to add new classes without changing existing functions. Adding a new function requires changing every class.

```java
// OBJECT-ORIENTED — Each shape owns its behavior via polymorphism
public interface Shape { double area(); }

public class Square implements Shape {
    private Point topLeft; private double side;
    public double area() { return side * side; }
}
public class Rectangle implements Shape {
    private Point topLeft; private double height, width;
    public double area() { return height * width; }
}
public class Circle implements Shape {
    private Point center; private double radius;
    public double area() { return PI * radius * radius; }
}
```

Ask yourself: **Will this part of the system evolve with new types, or new behaviors?** Choose accordingly. Use OO where types proliferate; use procedural where functions proliferate.

---

### Rule 3: **Obey the Law of Demeter — Talk to Friends, Not Strangers**

A method `f` of a class `C` should only call methods of:
- **`C` itself**
- An object **created by `f`**
- An object passed as an **argument to `f`**
- An object held in an **instance variable of `C`**

Do **not** invoke methods on objects returned by allowed calls. In other words: **don't talk to strangers.**

---

### Rule 4: **Eliminate Train Wrecks**

Chained method calls on return values are called *train wrecks*. They look like coupled train cars and violate Demeter when the intermediate values are objects.

```java
// BEFORE — Train wreck: navigating deeply through internals
final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();
```

```java
// AFTER — If these are DATA STRUCTURES: split them up
Options opts = ctxt.getOptions();
File scratchDir = opts.getScratchDir();
final String outputDir = scratchDir.getAbsolutePath();
```

```java
// AFTER — If these are OBJECTS: tell, don't ask
BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
```

The key insight: if `ctxt`, `Options`, and `ScratchDir` are **objects**, navigating through them violates Demeter because you're exposing internal structure. If they are **data structures** (public fields, no behavior), Demeter doesn't apply — but they should **have public fields**, not getter-chains that masquerade as objects.

If the data structures had public variables, the code would be:

```java
// This is clearly a data structure — no Demeter concern
final String outputDir = ctxt.options.scratchDir.absolutePath;
```

---

### Rule 5: **Avoid Hybrids — They Are the Worst of Both Worlds**

A **hybrid** is a class that is half object and half data structure. It has functions that do significant things *and* public variables (or getters/setters that, for all intents, make private variables public).

```java
// DANGER — Hybrid: has behavior AND exposes internals
public class BankAccount {
    private double balance;
    private String accountNumber;  // exposed via getter/setter

    public String getAccountNumber() { return accountNumber; }
    public void setAccountNumber(String n) { this.accountNumber = n; }

    // Real behavior mixing with exposed data
    public void deposit(double amount) { balance += amount; }
    public void withdraw(double amount) { balance -= amount; }
    public String formatAccountForReport() { /* ... */ }
}
```

Hybrids make it **hard to add new functions** (like objects) *and* **hard to add new data structures** (like data structures). They indicate a muddled design where the author didn't decide whether they needed protection from new types or new functions. Avoid them.

---

### Rule 6: **DTOs — The Quintessential Data Structure**

A **Data Transfer Object (DTO)** is a class with public variables and no functions. They shine at boundaries: database communication, socket message parsing, and translation stages between raw data and application objects.

```java
// Pure DTO — public fields, zero behavior
public class Address {
    public String street;
    public String streetExtra;
    public String city;
    public String state;
    public String zip;
}
```

The "bean" form (private fields + getters/setters) provides no real benefit over public fields for true data structures. It's ceremony that satisfies framework conventions without adding abstraction.

---

### Rule 7: **Active Records Are Data Structures, Not Objects**

An **Active Record** is a DTO with navigational methods like `save()` and `find()`. They are direct translations from database tables.

```java
// Active Record — DTO with persistence navigation, still a data structure
public class User extends ActiveRecord {
    public Long id;
    public String name;
    public String email;

    public User find(Long id) { /* ... */ }
    public void save() { /* ... */ }
}
```

**Do NOT** put business rules in Active Records. That creates a hybrid. Instead, keep the Active Record as a pure data structure and put business rules in separate objects that hide their internal data. Those objects may contain Active Record instances *as their data*, but the business logic lives in the object, not the record.

---

### Rule 8: **Tell, Don't Ask — Let Objects Do the Work**

When you find yourself pulling data out of an object to do something with it, you're treating an object like a data structure. Instead, tell the object to do the work for you.

```java
// BEFORE — Asking: pulling internals to compute externally
String outFile = ctxt.getOutputDir() + "/" + className.replace('.', '/') + ".class";
FileOutputStream fout = new FileOutputStream(outFile);
```

```java
// AFTER — Telling: let the object handle its own internals
BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
```

The caller shouldn't know about dots, slashes, file extensions, or directory paths. That's mixing levels of abstraction. The object owns that knowledge.

---

## Quick Decision Checklist

- [ ] Am I likely to add new **types** here? → Use **objects** (polymorphism, interfaces)
- [ ] Am I likely to add new **functions** here? → Use **data structures** (procedural code)
- [ ] Do I have behavior that acts on data from another class? → Move behavior to that class (**tell, don't ask**)
- [ ] Am I chaining method calls (`a.getB().getC()`) on objects? → **Violation of Demeter** — refactor
- [ ] Does my class have both real behavior AND exposed fields? → **Hybrid** — split into object + DTO
- [ ] Am I putting business rules in an Active Record? → Move rules to separate **business objects**
- [ ] Are my getters just exposing fields with no abstraction? → Either make fields **public** (data structure) or design real **abstract interfaces** (object)

---

## Related Notes

- [[Clean Code Principles]] — The foundation: meaningful names, small functions, minimal side effects
- [[Class Design & SOLID]] — SRP, OCP, LSP, ISP, DIP applied to class organization
- [[Code Smells Catalog]] — G36 (train wrecks), G34 (mixed levels of abstraction), Feature Envy from Refactoring
- [[Objects vs Data Structures]] — The principle that objects should be commanded, not interrogated
- [[Objects vs Data Structures]] — Deeper exploration of the "talk to friends" heuristic
