---
tags:
- design-patterns
- oop
- software-design
- software-engineering
---

> *Source: Dive Into Design Patterns by Alexander Shvets, "SOLID Principles" (pp. 51–70)*

## Core Principle

> **SOLID** is an acronym for five design principles intended to make software designs more understandable, flexible, and maintainable. Introduced by Robert Martin in *Agile Software Development, Principles, Patterns, and Practices*. Apply pragmatically—mindlessly applying all five at once can cause more harm than good.

---

### Single Responsibility Principle

**"A class should have only one reason to change."** Make every class responsible for a single part of the functionality, with that responsibility entirely encapsulated within the class. The goal is reducing complexity—when a class does too many things, you must change it every time *any* of those things changes, risking breakage of unrelated parts.

```java
// ❌ BEFORE: Employee handles both data and report formatting
class Employee {
    String name;
    String position;
    int hoursWorked;

    Employee(String name, String position, int hoursWorked) { ... }

    void calculatePay() { ... }
    void saveToDatabase() { ... }
    void printTimesheetReport() {
        // report formatting logic here
    }
    // Reason to change #1: employee data management
    // Reason to change #2: timesheet report format
}
```

```java
// ✅ AFTER: Report behavior extracted into its own class
class Employee {
    String name;
    String position;
    int hoursWorked;

    Employee(String name, String position, int hoursWorked) { ... }

    void calculatePay() { ... }
    void saveToDatabase() { ... }
    // Single reason to change: employee data management
}

class TimesheetReport {
    void print(Employee employee) {
        // report formatting logic
    }
    // Single reason to change: report format
}
```

---

### Open/Closed Principle

**"Classes should be open for extension but closed for modification."** Keep existing code from breaking when implementing new features. A class is *open* if you can extend it via subclassing; it is *closed* if its interface is clearly defined and won't be changed. Instead of modifying a tested, reviewed class directly, create a subclass and override only what needs to differ.

```java
// ❌ BEFORE: Shipping methods hard-coded → adding a new method forces Order change
class Order {
    double weight;
    String shippingMethod; // "ground", "air", ...

    double calculateShipping() {
        if (shippingMethod.equals("ground")) {
            return weight * 1.5;
        } else if (shippingMethod.equals("air")) {
            return weight * 3.0 * 0.5;
        } else if (shippingMethod.equals("sea")) {
            return weight * 0.5;
        }
        // Adding a new method → modify this class (risk!)
        return 0;
    }
}
```

```java
// ✅ AFTER: Shipping methods extracted via Strategy pattern
interface Shipping {
    double calculate(double weight);
}

class GroundShipping implements Shipping {
    public double calculate(double weight) { return weight * 1.5; }
}

class AirShipping implements Shipping {
    public double calculate(double weight) { return weight * 3.0 * 0.5; }
}

class SeaShipping implements Shipping {
    public double calculate(double weight) { return weight * 0.5; }
}

class Order {
    double weight;
    Shipping shipping;

    Order(double weight, Shipping shipping) {
        this.weight = weight;
        this.shipping = shipping;
    }

    double calculateShipping() {
        return shipping.calculate(weight);
    }
    // New shipping method → new class, Order unchanged
}
```

---

### Liskov Substitution Principle

**"Subclasses should be substitutable for their base classes."** When extending a class, you should be able to pass subclass objects in place of parent objects without breaking client code. The subclass must remain compatible with the behavior of the superclass—extend base behavior rather than replacing it with something entirely different.

The principle has formal requirements: (1) parameter types in overridden methods should match or be *more abstract*; (2) return types should match or be a *subtype*; (3) exception types thrown should match or be subtypes of what the base method throws; (4) pre-conditions must not be strengthened; (5) post-conditions must not be weakened; (6) invariants of the superclass must be preserved.

```java
// ❌ BEFORE: ReadOnlyDocument throws on save() → breaks client expectations
class Document {
    String content;

    Document(String content) { this.content = content; }

    void save(String filename) {
        // write content to file
    }

    void open(String filename) {
        // read content from file
    }
}

class ReadOnlyDocument extends Document {
    ReadOnlyDocument(String content) { super(content); }

    @Override
    void save(String filename) {
        throw new UnsupportedOperationException("Cannot save read-only document");
        // Client code that expects save() to work → breaks!
    }
    // Also violates Open/Closed: client must check document type before saving
}
```

```java
// ✅ AFTER: Read-only document becomes the base class of the hierarchy
class Document {
    String content;

    Document(String content) { this.content = content; }

    void open(String filename) {
        // read content from file
    }
    // No save() here—base class makes no promises it can't keep
}

class WritableDocument extends Document {
    WritableDocument(String content) { super(content); }

    void save(String filename) {
        // write content to file
    }
    // Extends base behavior by ADDING save capability
}

// Client code:
void processDocument(Document doc) {
    doc.open("file.txt");
    // No assumption about save() → substitution always safe
}
```

---

### Interface Segregation Principle

**"Clients shouldn't be forced to depend on interfaces they don't use."** Break down "fat" interfaces into granular, specific ones. A class can implement multiple interfaces, so there's no need to cram unrelated methods into one. A change to a fat interface breaks even clients that don't use the changed methods.

```java
// ❌ BEFORE: Monolithic cloud provider interface forces all clients to implement everything
interface CloudProvider {
    void storeFile(String name, byte[] data);
    byte[] getFile(String name);
    void createVirtualMachine(String region, String specs);
    void listVirtualMachines(String region);
    void sendNotification(String text, String recipient);
    void configureCDN(String domain);
    // ... many more methods
}

// DropboxProvider can't do VMs or notifications → forced to stub
class DropboxProvider implements CloudProvider {
    void storeFile(String name, byte[] data) { /* actual implementation */ }
    byte[] getFile(String name) { /* actual implementation */ }
    void createVirtualMachine(String region, String specs) { /* stub */ }
    void listVirtualMachines(String region) { /* stub */ }
    void sendNotification(String text, String r) { /* stub */ }
    void configureCDN(String domain) { /* stub */ }
    // Ugly stubs everywhere
}

// AWSProvider can do everything → but bloated interface still a maintenance burden
```

```java
// ✅ AFTER: One fat interface split into granular, role-specific interfaces
interface CloudStorage {
    void storeFile(String name, byte[] data);
    byte[] getFile(String name);
}

interface CloudCompute {
    void createVirtualMachine(String region, String specs);
    void listVirtualMachines(String region);
}

interface CloudNotifications {
    void sendNotification(String text, String recipient);
}

interface CloudCDN {
    void configureCDN(String domain);
}

// DropboxProvider implements only what it actually supports
class DropboxProvider implements CloudStorage {
    public void storeFile(String name, byte[] data) { /* real impl */ }
    public byte[] getFile(String name) { /* real impl */ }
}

// AWSProvider implements all the granular interfaces it needs
class AWSProvider implements CloudStorage, CloudCompute, CloudNotifications, CloudCDN {
    // All real implementations—no stubs
}
```

---

### Dependency Inversion Principle

**"Depend upon abstractions, not concretions. High-level classes shouldn't depend on low-level classes—both should depend on abstractions. Abstractions shouldn't depend on details; details should depend on abstractions."**

- **Low-level classes:** implement basic operations (disk I/O, network, database connections).
- **High-level classes:** contain complex business logic that directs low-level classes.

When business logic depends directly on low-level classes, any change to a low-level class (e.g., a database upgrade) can ripple into high-level code that shouldn't care about storage details.

```java
// ❌ BEFORE: High-level reporting class directly depends on concrete low-level database
class MySQLDatabase {
    void connect(String connectionString) { ... }
    void disconnect() { ... }
    String[] query(String sql) { ... }
    void execute(String sql) { ... }
}

class BudgetReport {
    MySQLDatabase database;

    BudgetReport(MySQLDatabase database) {
        this.database = database;
    }

    void generate() {
        database.connect("server=prod;db=finance");
        String[] rows = database.query("SELECT * FROM budgets");
        // ... complex budget calculations
        database.execute("INSERT INTO reports VALUES (...)");
        database.disconnect();
    }
    // Tightly coupled to MySQLDatabase—can't switch to Postgres, flat files, or API
    // Any change in MySQLDatabase may break BudgetReport
}
```

```java
// ✅ AFTER: Dependency inverted—both depend on a high-level abstraction
interface DataStore {
    String[] readData(String query);
    void writeData(String command);
}

class MySQLDatabase implements DataStore {
    void connect(String connectionString) { ... }
    void disconnect() { ... }

    public String[] readData(String query) {
        connect("server=prod;db=finance");
        String[] result = /* execute query */;
        disconnect();
        return result;
    }

    public void writeData(String command) {
        connect("server=prod;db=finance");
        /* execute command */;
        disconnect();
    }
    // Low-level class now depends on the high-level DataStore abstraction
}

class BudgetReport {
    DataStore store;  // Depends on abstraction, not concrete class

    BudgetReport(DataStore store) {
        this.store = store;
    }

    void generate() {
        String[] rows = store.readData("SELECT * FROM budgets");
        // ... complex budget calculations
        store.writeData("INSERT INTO reports VALUES (...)");
    }
    // Works with any DataStore implementation—MySQL, Postgres, flat files, mock
}
```

The direction of the original dependency has been **inverted**: low-level classes now depend on high-level abstractions, not the other way around. This principle often pairs with the Open/Closed Principle—you can extend low-level classes for different business logic without breaking existing code.

---

## Summary Checklist

- [ ] **Single Responsibility** — Each class has exactly one reason to change
- [ ] **Open/Closed** — Classes are open for extension, closed for modification
- [ ] **Liskov Substitution** — Subclasses are substitutable for their base classes without breaking clients
- [ ] **Interface Segregation** — Interfaces are narrow; clients aren't forced to depend on methods they don't use
- [ ] **Dependency Inversion** — Both high- and low-level classes depend on abstractions; details depend on abstractions

---

## Related

- [[Design Principles]]
- [[Features of Good Design]]
- [[Introduction to OOP]]
- [[Strategy]]
- [[Factory Method]]
- [[Decorator]]
