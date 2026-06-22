# Object-Oriented Programming

> *Source: Clean Architecture by Robert C. Martin, Chapter 5 (pp. 46–55)*

---

## Core Principle

> **OO is the ability, through the use of polymorphism, to gain absolute control over every source code dependency in the system—enabling a plugin architecture where high-level policy modules are independent of low-level detail modules.**

Uncle Bob systematically dismantles the traditional "encapsulation + inheritance + polymorphism" definition. Encapsulation predates OO (C had it better), inheritance could be faked manually (C struct ordering trick), but **polymorphism**—specifically *safe, convenient* polymorphism via interface inheritance—is OO's real architectural superpower. It enables dependency inversion, which in turn enables independent deployability and the plugin architecture that Clean Architecture is built on.

---

## The Rules / Key Concepts

### 1. Encapsulation — OO Weakened It

OO languages did not invent encapsulation; they actually **broke** the perfect encapsulation C already had. In C, header files forward-declared opaque structs and function signatures—clients had zero knowledge of struct members or implementation details.

```c
// ❌ C: Perfect encapsulation — clients see nothing
// point.h
struct Point;
struct Point* makePoint(double x, double y);
double distance(struct Point* p1, struct Point* p2);
```

```cpp
// ❌ C++: Encapsulation broken — member variables exposed in header
// point.h
class Point {
public:
    Point(double x, double y);
    double distance(const Point& p) const;
private:
    double x;  // clients CAN see these
    double y;
};  // changing x/y forces recompile of all clients
```

```java
// ❌ Java/C#: Even worse — no header/implementation split at all
// Declaration and definition are inseparable
public class Point {
    private double x;  // fully visible in the same file
    private double y;
    public Point(double x, double y) { ... }
    public double distance(Point p) { ... }
}
```

✅ **The takeaway:** `public`/`private`/`protected` keywords are a hack to partially repair the encapsulation that C++ broke. Many OO languages (Smalltalk, Python, JavaScript, Ruby) have little or no enforced encapsulation. OO depends on programmer discipline, not language enforcement.

---

### 2. Inheritance — OO Made It Convenient, Not New

C programmers could fake single inheritance long before OO languages existed by exploiting struct member ordering. If a "derived" struct's first fields match the "base" struct's layout, you can cast between them.

```c
// ✅ C: Faking inheritance through struct member ordering
// namedPoint.h
struct NamedPoint;
struct NamedPoint* makeNamedPoint(double x, double y, char* name);

// namedPoint.c — first two fields match Point's layout
struct NamedPoint {
    double x, y;     // same order as Point
    char* name;      // extension
};

// main.c — manual upcast required
distance(
    (struct Point*) origin,       // explicit cast
    (struct Point*) upperRight);  // explicit cast
```

```java
// ✅ OO: Implicit upcasting, method override, cleaner syntax
class NamedPoint extends Point {
    private String name;
    public NamedPoint(double x, double y, String name) {
        super(x, y);
        this.name = name;
    }
}
// distance(origin, upperRight) works with no cast
```

✅ **The takeaway:** OO scores zero for encapsulation, half a point for inheritance. C++ itself implements single inheritance via the same struct-layout trick. Multiple inheritance is harder to fake manually, but the overall concept predates OO. The real contribution is **convenience and safety**.

---

### 3. Polymorphism — The Real Differentiator

Polymorphism existed before OO through **pointers to functions** (vtables in manual form). UNIX IO drivers used this pattern: a `FILE` struct holds function pointers, and `getchar()` / `putchar()` dispatch through them. But raw function pointers are dangerous—they rely on manual conventions that are easy to forget and produce devilishly hard bugs.

```c
// ❌ C: Polymorphism via function pointers — powerful but dangerous
struct FILE {
    void (*open)(char* name, int mode);
    void (*close)();
    int (*read)();
    void (*write)(char);
    void (*seek)(long index, int mode);
};

// Console driver loads function pointers manually
struct FILE console = {open, close, read, write, seek};

// getchar dispatches through the pointer
int getchar() {
    return STDIN->read();  // manual vtable dispatch
}
// Forgot to initialize a pointer? → nightmare bug.
// Called a function directly instead of through the pointer? → nightmare bug.
```

```java
// ✅ OO: Same mechanism, but safe and automatic
interface IODevice {
    void open(String name, int mode);
    void close();
    int read();
    void write(char c);
    void seek(long index, int mode);
}

class ConsoleDevice implements IODevice {
    // Compiler builds the vtable. No manual pointers. No forgotten conventions.
    public int read() { /* ... */ }
    public void write(char c) { /* ... */ }
}
```

✅ **The takeaway:** OO imposes **discipline on indirect transfer of control**. The mechanism is the same (vtables → function pointers), but the compiler enforces the conventions. Polymorphism becomes trivial and safe. This is what old C programmers could only dream of.

---

### 4. Plugin Architecture — Polymorphism Enables Device Independence

With safe polymorphism, modules that define interfaces don't depend on the modules that implement them. The classic example: a `copy()` program that reads from STDIN and writes to STDOUT.

```java
// ✅ The copy program depends only on the IO interface — never on specific devices
void copy(Reader in, Writer out) {
    int c;
    while ((c = in.read()) != -1)
        out.write(c);
}
// Works with: keyboard→screen, file→file, handwriting→speech, network→disk...
// No recompilation. No changes. The IO devices are PLUGINS.
```

✅ **The takeaway:** The UNIX operating system pioneered this for IO devices in the late 1950s. OO makes plugin architecture available **anywhere, for anything**—not just IO. This is the foundation of Clean Architecture's boundary enforcement.

---

### 5. Dependency Inversion — OO's Architectural Superpower

Before safe polymorphism, source code dependencies inexorably followed the flow of control. `main()` calls high-level functions → which call mid-level → which call low-level. Every caller had to `#include` or `import` the callee's module. **The architect had no options.**

```java
// ❌ Before dependency inversion: dependencies follow flow of control
// main → HighLevel → MidLevel → LowLevel
// Every arrow is BOTH a runtime call AND a compile-time dependency
class HighLevelPolicy {
    void execute() {
        LowLevelDetail detail = new LowLevelDetail(); // hard dependency ↓
        detail.doWork();
    }
}
```

```java
// ✅ With polymorphism: dependencies can be INVERTED
// HighLevelPolicy → Interface ← LowLevelDetail
// Flow of control: HighLevel → LowLevel (down at runtime)
// Source dependency: LowLevel → Interface ← HighLevel (dependency points UP)

interface IWorker {
    void doWork();
}

class HighLevelPolicy {
    private IWorker worker;
    public HighLevelPolicy(IWorker worker) { this.worker = worker; }
    void execute() {
        worker.doWork();  // calls down at runtime, depends UP at compile time
    }
}

class LowLevelDetail implements IWorker {
    public void doWork() { /* ... */ }
    // LowLevelDetail depends on IWorker (and thus on HighLevelPolicy's domain)
}
```

✅ **The takeaway:** Any source code dependency **anywhere in the system** can be inverted. The architect has absolute control over dependency direction. This is what makes the **Open-Closed Principle (OCP)** and **Dependency Inversion Principle (DIP)** practically achievable.

---

### 6. Independent Deployability — The Endgame

When business rules own the interfaces and low-level details implement them, the dependency arrows point **inward** toward policy:

```
         ┌─────────────────┐
         │  Business Rules  │  ← owns interfaces, depends on NOTHING external
         └────────┬────────┘
                  │
        ┌─────────┼─────────┐
        ▼                   ▼
   ┌─────────┐         ┌─────────┐
   │   UI    │         │Database │    ← plugins; depend ON business rules
   └─────────┘         └─────────┘
```

```java
// ✅ Business rules define the interface — never import UI or DB
interface CustomerRepository {
    Customer findById(String id);
    void save(Customer customer);
}

class PlaceOrderUseCase {
    private CustomerRepository repo;  // depends on interface, NOT on MySQL
    public void execute(Order order) {
        Customer c = repo.findById(order.getCustomerId());
        // business logic...
    }
}

// MySQL implementation is a plugin — can be swapped without touching business rules
class MySqlCustomerRepository implements CustomerRepository {
    // database-specific code lives here
}
```

✅ **The takeaway:** Business rules, UI, and database can be compiled into **separate deployment units** (JARs, DLLs, gems) with dependencies matching source code. Changing the database requires redeploying only the database plugin—not the business rules. This is **independent deployability**, which enables **independent developability** by separate teams.

---

## Summary Checklist

- [ ] OO did **not** invent encapsulation — C had better encapsulation before OO languages broke it
- [ ] OO did **not** invent inheritance — C programmers faked it with struct member ordering tricks
- [ ] OO **did** make polymorphism **safe and convenient** — the compiler enforces conventions that were previously manual and error-prone
- [ ] Polymorphism is fundamentally pointers to functions (vtables); OO imposes discipline on indirect transfer of control
- [ ] Safe polymorphism enables **plugin architecture** — modules that own interfaces don't depend on implementers
- [ ] Dependency inversion means source code dependencies can point **opposite** to the flow of control
- [ ] With dependency inversion, **business rules never mention the UI or database** — they become plugins
- [ ] Independent deployability: only the changed component needs redeployment
- [ ] Independent developability: separate teams can work on separate deployable components
- [ ] To the architect, OO = the ability to gain **absolute control over every source code dependency**

---

## Related

- [[Clean Architecture Overview]]
- [[Programming Paradigms]]
- [[SOLID Design Principles]]
- [[Component Cohesion]]
- [[Boundaries]]
- [[Policy and Business Rules]]
