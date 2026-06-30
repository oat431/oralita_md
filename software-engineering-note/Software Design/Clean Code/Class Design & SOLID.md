---
tags:
- clean-code
- software-design
- software-engineering
---

# Class Design & SOLID

> *"We want our systems to be composed of many small classes, not a few large ones. Each small class encapsulates a single responsibility, has a single reason to change, and collaborates with a few others to achieve the desired system behaviors."*
>
> — Robert C. Martin, *Clean Code*, pp. 136–152

---

### Class Organization: The Stepdown Rule

**Order your class members so the program reads like a newspaper article.**

Java class member sequence:

1. **Public static constants** — exposed compile-time values
2. **Private static variables** — shared across instances, hidden
3. **Private instance variables** — per-object state
4. **Public functions** — the class API
5. **Private utility functions** — placed immediately after the public function that calls them

```java
// ❌ BEFORE — chaotic member order
public class ReportGenerator {
    public void generate() { ... }               // public mixed everywhere
    private String templatePath;                 // instance var in the middle
    public static final String DEFAULT_TYPE = "PDF";
    private static int reportCount;
    private void applyTemplate(String t) { ... } // utility far from caller
    public ReportGenerator(String path) { ... }
    private String outputDir;
}

// ✅ AFTER — stepdown order, reads like a story
public class ReportGenerator {
    // 1. Public static constants
    public static final String DEFAULT_TYPE = "PDF";

    // 2. Private static variables
    private static int reportCount;

    // 3. Private instance variables
    private String templatePath;
    private String outputDir;

    // 4. Constructor
    public ReportGenerator(String templatePath) {
        this.templatePath = templatePath;
    }

    // 5. Public functions
    public void generate() {
        applyTemplate(templatePath);
        outputToFile();
    }

    // 6. Private utilities — right after the caller
    private void applyTemplate(String template) {
        resolvePlaceholders(template);
    }

    private void resolvePlaceholders(String content) {
        // ...
    }

    private void outputToFile() {
        // ...
    }
}
```

**Encapsulation:** Keep variables and utilities private as the default. Loosen to `protected` or package-scope only as a *last resort* when a test in the same package genuinely needs access. Tests rule — but privacy rules first.

---

### Classes Should Be Small

**Measure size by responsibilities, not by lines of code.**

A class with 5 methods can still be too big. A class with 70 public methods is a *God class* — a clear sign of too many responsibilities.

**Two heuristics for gauging size:**

1. **The name test** — Can you derive a concise, unambiguous name for the class? If the name contains weasel words like `Processor`, `Manager`, `Super`, `Handler`, or `Utility`, the class aggregates too many responsibilities. A class name should describe *exactly* what it does.

2. **The 25-word test** — Describe the class in ~25 words *without* using "if," "and," "or," or "but." Every "and" is a hint that the class has multiple responsibilities.

> ❌ "The `SuperDashboard` provides access to the component that last held the focus, **and** it also allows us to track the version and build numbers."
>
> — Two responsibilities detected.

---

### Single Responsibility Principle (SRP)

**A class should have one, and only one, reason to change.**

Responsibility = reason to change. If you can think of more than one reason a class might need modification, the class has too many responsibilities.

```java
// ❌ BEFORE — two reasons to change (version tracking + Swing GUI management)
public class SuperDashboard extends JFrame implements MetaDataUser {
    public Component getLastFocusedComponent() { ... }
    public void setLastFocused(Component lastFocused) { ... }
    public int getMajorVersionNumber() { ... }
    public int getMinorVersionNumber() { ... }
    public int getBuildNumber() { ... }
}

// ✅ AFTER — each class has exactly one reason to change
public class Dashboard extends JFrame implements MetaDataUser {
    // Single responsibility: managing focused Swing components
    public Component getLastFocusedComponent() { ... }
    public void setLastFocused(Component lastFocused) { ... }
}

public class Version {
    // Single responsibility: tracking version/build numbers
    public int getMajorVersionNumber() { ... }
    public int getMinorVersionNumber() { ... }
    public int getBuildNumber() { ... }
}
```

**Why SRP gets violated (and how to fix it):**

- Most developers stop refactoring once the code *works*. Clean code requires a second pass: breaking overstuffed classes into decoupled, single-purpose units.
- *Fear:* "Many small classes make the big picture harder to understand."
- *Reality:* A toolbox with many small, well-labeled drawers is faster to navigate than a few drawers where everything is dumped together. A system with many small classes has *no more moving parts* than one with few large classes — it just organizes the complexity so you only need to understand the piece directly affected at any given time.

---

### Cohesion

**High cohesion means each method manipulates most of the instance variables.**

A maximally cohesive class is one where *every* method uses *every* instance variable. That extreme is rarely achievable, but aim high.

```java
// ✅ High cohesion — methods share the same fields
public class Stack {
    private int topOfStack = 0;
    private List<Integer> elements = new LinkedList<>();

    public int size() {              // uses topOfStack
        return topOfStack;
    }

    public void push(int element) {  // uses topOfStack + elements
        topOfStack++;
        elements.add(element);
    }

    public int pop() {               // uses topOfStack + elements
        if (topOfStack == 0)
            throw new EmptyStackException();
        int element = elements.get(--topOfStack);
        elements.remove(topOfStack);
        return element;
    }
}
```

**When cohesion drops, a new class is trying to get out.**

If you find a subset of methods that only use a subset of the instance variables, those methods and variables belong together — in their own class. Split them.

---

### Maintaining Cohesion Results in Many Small Classes

**Breaking large functions into smaller ones naturally produces more cohesive classes — if you follow through.**

The pattern:

1. You have a large function with many local variables.
2. You want to extract a small piece into its own method.
3. That piece uses 4 of the local variables.
4. Temptation: promote those 4 variables to instance variables so the extraction needs zero parameters.
5. Consequence: the class now has *more* instance variables, each used by only a *subset* of methods → **cohesion drops**.
6. **Solution:** those methods and their shared variables *are* a class in their own right. Extract them.

```java
// ❌ BEFORE — one monolithic function, all logic in main()
// PrintPrimes.java — deeply indented, tightly coupled, 50+ lines of procedural code
// (see Knuth's literate programming example, Clean Code pp. 141–143)

// ✅ AFTER — three small, cohesive classes
public class PrimePrinter {                          // Responsibility: execution environment
    public static void main(String[] args) {
        int[] primes = PrimeGenerator.generate(1000);
        RowColumnPagePrinter printer = new RowColumnPagePrinter(50, 4,
            "The First 1000 Prime Numbers");
        printer.print(primes);
    }
}

public class RowColumnPagePrinter {                   // Responsibility: output formatting
    private int rowsPerPage;
    private int columnsPerPage;
    private String pageHeader;
    private PrintStream printStream;
    // Methods: print(), printPage(), printRow(), printPageHeader() — all share the fields above
}

public class PrimeGenerator {                         // Responsibility: prime algorithm
    private static int[] primes;
    private static ArrayList<Integer> multiplesOfPrimeFactors;
    // Methods: generate(), isPrime(), isNotMultipleOfAnyPreviousPrimeFactor(), ...
    // All methods share primes + multiplesOfPrimeFactors → high cohesion
}
```

> *Note: the refactored version is longer in lines (descriptive names, class/function declarations as commentary, whitespace), but it is far easier to understand, test, and modify.*

---

### Open-Closed Principle (OCP)

**Classes should be open for extension but closed for modification.**

When a new feature requires you to *open up* an existing class and modify its internals, you risk breaking existing functionality. Organize so that new behavior is added via *extension* (new subclass), not *modification* (editing existing code).

```java
// ❌ BEFORE — must edit this class every time a new SQL statement type is added
public class Sql {
    public Sql(String table, Column[] columns) { ... }
    public String create() { ... }
    public String insert(Object[] fields) { ... }
    public String selectAll() { ... }
    public String findByKey(String keyColumn, String keyValue) { ... }
    public String select(Column column, String pattern) { ... }
    public String select(Criteria criteria) { ... }
    public String preparedInsert() { ... }
    // Private methods that relate only to SELECT — smell!
    private String selectWithCriteria(String criteria) { ... }
    // Adding "update" requires opening this class → risk
}

// ✅ AFTER — closed for modification, open for extension
public abstract class Sql {
    protected String table;
    protected Column[] columns;

    public Sql(String table, Column[] columns) {
        this.table = table;
        this.columns = columns;
    }

    public abstract String generate();
}

public class CreateSql extends Sql {
    public CreateSql(String table, Column[] columns) { super(table, columns); }
    @Override public String generate() { /* CREATE logic */ }
}

public class SelectSql extends Sql {
    public SelectSql(String table, Column[] columns) { super(table, columns); }
    @Override public String generate() { /* SELECT logic */ }
}

public class InsertSql extends Sql {
    private Object[] fields;
    public InsertSql(String table, Column[] columns, Object[] fields) {
        super(table, columns);
        this.fields = fields;
    }
    @Override public String generate() { /* INSERT logic */ }
}

// Adding UPDATE? Just drop in a new subclass. Nothing else changes.
public class UpdateSql extends Sql {
    public UpdateSql(String table, Column[] columns) { super(table, columns); }
    @Override public String generate() { /* UPDATE logic */ }
}
```

**Key insight:** Private methods that serve only a subset of the public API are a heuristic — they hint that responsibilities are tangled and the class should be split along SRP/OCP lines.

**But don't pre-optimize.** If the class is logically complete and you won't need to extend it for the foreseeable future, leave it alone. Refactor only when change forces you to open the class.

---

### Dependency Inversion Principle (DIP)

**Depend on abstractions, not on concrete details.**

Concrete implementation details change. Interfaces and abstract classes change far less often. When a class depends directly on a concrete class, it is vulnerable to every change in that concrete class. Flip the dependency: both should depend on an abstraction.

```java
// ❌ BEFORE — Portfolio depends directly on a volatile concrete implementation
public class Portfolio {
    private TokyoStockExchange exchange;  // concrete dependency

    public Portfolio() {
        this.exchange = new TokyoStockExchange();  // tightly coupled
    }

    public Money value() {
        // Calls TokyoStockExchange.currentPrice() — hard to test,
        // value changes every 5 minutes!
    }
}

// ✅ AFTER — depends on an abstraction (interface)
public interface StockExchange {
    Money currentPrice(String symbol);
}

public class TokyoStockExchange implements StockExchange {
    @Override
    public Money currentPrice(String symbol) {
        // real API call
    }
}

public class Portfolio {
    private StockExchange exchange;  // depends on abstraction

    public Portfolio(StockExchange exchange) {  // injected
        this.exchange = exchange;
    }

    public Money value() {
        // Uses exchange.currentPrice() — testable, decoupled
    }
}

// Testing is now trivial — use a stub
public class PortfolioTest {
    @Test
    public void GivenFiveMSFT_TotalShouldBe500() {
        FixedStockExchangeStub exchange = new FixedStockExchangeStub();
        exchange.fix("MSFT", 100);                         // hard-code $100/share
        Portfolio portfolio = new Portfolio(exchange);
        portfolio.add(5, "MSFT");
        assertEquals(500, portfolio.value());              // deterministic
    }
}
```

**Benefits of DIP:**

- **Testability** — swap in stubs/mocks with fixed values; no network, no volatility
- **Flexibility** — swap `TokyoStockExchange` for `LondonStockExchange` without touching `Portfolio`
- **Isolation from change** — when the concrete implementation changes, dependents are unaffected
- **Comprehension** — each element is understood in isolation

---

### Design Checklist

- [ ] **Member order** follows stepdown: constants → statics → instance variables → public functions → private utilities
- [ ] **Class name** is concise and unambiguous — no weasel words (`Manager`, `Processor`, `Super`, `Handler`)
- [ ] **25-word description** passes without "if," "and," "or," or "but"
- [ ] **Single Responsibility** — exactly one reason to change; any private methods serving only a subset of the API are extracted
- [ ] **Class is small** — measured by responsibilities, not line count; no God classes
- [ ] **High cohesion** — each method uses most instance variables; subset-of-fields-used-by-subset-of-methods is a split signal
- [ ] **Open for extension, closed for modification** — new features added via subclassing, not by opening existing classes
- [ ] **Depends on abstractions** — concrete dependencies are injected; interfaces/abstract classes isolate volatile details
- [ ] **Encapsulation** — variables/utilities are private by default; package-scope only as a last resort for tests
- [ ] **System is composed of many small classes** collaborating, not a few large classes doing everything

---

### Related Notes

- [[Clean Code Principles]]
- [[Function Design]]
- [[Naming Conventions]]
- [[Objects vs Data Structures]]
- [[Code Smells Catalog]]

---

*Source: Robert C. Martin with Jeff Langr, Clean Code: A Handbook of Agile Software Craftsmanship, Chapter 10: "Classes," pp. 136–152. Prentice Hall, 2008. Principles cross-referenced with [PPP]: Agile Software Development: Principles, Patterns, and Practices (Martin, 2002) and [RDD]: Object Design: Roles, Responsibilities, and Collaborations (Wirfs-Brock et al., 2002).*
