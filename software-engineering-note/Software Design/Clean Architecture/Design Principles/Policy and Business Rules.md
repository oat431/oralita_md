# Policy and Business Rules

> *Source: Clean Architecture by Robert C. Martin, Chapters 19–20 (pp. 149–157)*

---

## Core Principle

> **Software systems are statements of policy. Higher-level policies are those farthest from inputs and outputs; they should never depend on lower-level details. Business rules—both entity-level and application-level—are the core of the system, and they must remain pristine, reusable, and independent of frameworks, databases, and UIs.**

Policy decomposition, level assignment by distance from I/O, and dependency direction are the fundamental architectural decisions. Entities encapsulate Critical Business Rules that exist independent of any system; use cases orchestrate those entities for a specific application. Every source code dependency must point from low-level toward high-level policy.

---

## The Rules / Key Concepts

### 1. Policy as the Essence of Software

A computer program is a detailed description of the policy by which inputs are transformed into outputs. In nontrivial systems, that policy breaks into many smaller policy statements—business rule calculations, report formatting, input validation, and so on. Architecture is the art of separating those policies and regrouping them based on the ways they change.

Policies that change for the same reasons and at the same times are at the same level and belong in the same component. Policies that change for different reasons or at different times are at different levels and must be separated. The regrouped components form a directed acyclic graph where edges are compile-time dependencies (`import`, `using`, `require`), and the direction of every edge follows level: low-level components depend on high-level components.

### 2. Level = Distance from Inputs and Outputs

Level has a strict definition: **the distance from the inputs and outputs of the system.** The farther a policy is from both input and output, the higher its level. Policies that manage I/O directly are the lowest level.

Consider a simple encryption program:

```
Input → Translate (table lookup) → Output
```

The `Translate` component is the highest-level element—it is farthest from both I/O endpoints. The data flow (curved solid arrows) and the source code dependencies (straight dashed lines) do **not** point in the same direction. The architect's job is to decouple dependencies from data flow and couple them to level.

**Wrong architecture** (data-flow direction drives dependencies):

```java
function encrypt() {
    while(true)
        writeChar(translate(readChar()));
}
```

Here the high-level `encrypt` function depends on low-level `readChar` and `writeChar`—a dependency inversion.

**Correct architecture** (dependencies point toward high-level policy):

```java
// High-level policy — knows nothing of IO
class Encrypt {
    private CharReader reader;
    private CharWriter writer;

    void execute() {
        while(true)
            writer.write(translate(reader.read()));
    }
}

// Interfaces owned by the high-level policy
interface CharReader { char read(); }
interface CharWriter { void write(char c); }

// Low-level plugins
class ConsoleReader implements CharReader { ... }
class ConsoleWriter implements CharWriter { ... }
```

All dependencies crossing the boundary around `Encrypt` point inward. The high-level encryption policy is decoupled from I/O—it can be reused in any context, and changes to I/O devices do not affect the encryption algorithm.

### 3. Why Level Matters for Change Management

Higher-level policies (those farthest from I/O) change less frequently and for more important reasons. Lower-level policies (those closest to I/O) change frequently, with more urgency, but for less important reasons.

In the encryption example, the I/O devices are far more likely to change than the encryption algorithm. If the algorithm does change, the reason will be more substantive than a device swap. When all source code dependencies point toward higher-level policy, trivial but urgent changes at the lowest levels have no impact on the higher, more important levels.

Lower-level components should be **plugins** to higher-level components. The higher-level component knows nothing of the plugin; the plugin depends on the higher-level component.

### 4. Critical Business Rules (Entities)

Strictly speaking, business rules are rules or procedures that **make or save the business money—irrespective of whether they are implemented on a computer.** They would make or save money even if executed manually.

A bank charging N% interest on a loan is a business rule. It makes the bank money whether calculated by a computer or by a clerk with an abacus. These are **Critical Business Rules**, and they require **Critical Business Data** (loan balance, interest rate, payment schedule)—data that would exist even without an automated system.

The critical rules and critical data are inextricably bound, making them a good candidate for an object: an **Entity**.

```java
class Loan {
    // Critical Business Data
    private double balance;
    private double interestRate;
    private PaymentSchedule schedule;

    // Critical Business Rules
    double calculateInterest() { ... }
    PaymentSchedule generateSchedule() { ... }
    boolean isDelinquent() { ... }
}
```

An Entity is pure business and nothing else. It is unsullied with concerns about databases, user interfaces, or third-party frameworks. It could serve the business in any system, irrespective of how data is stored, presented, or distributed. You do not need an object-oriented language—all that is required is binding the Critical Business Data and Critical Business Rules together in a single, separate software module.

### 5. Use Cases (Application-Specific Business Rules)

Not all business rules are as pure as Entities. Some business rules make or save money by defining and constraining how an **automated system** operates. These rules make no sense in a manual environment—they exist only as part of an automated system.

A bank rule that "the system shall not proceed to the loan payment estimation screen until contact information is gathered and credit score ≥ 500" is a **use case**. A use case specifies:
- The input provided by the user
- The output returned to the user
- The processing steps involved in producing that output

A use case describes **application-specific** business rules, as opposed to the Critical Business Rules within the Entities. It controls the dance of the Entities—specifying when and how the Critical Business Rules are invoked.

Critically, a use case does **not** describe the user interface. It informally specifies data coming in and going out, but reveals nothing about web, thick client, console, or service delivery. How data gets in and out is irrelevant to the use case.

```java
// Application-specific business rule
class CreateLoanUseCase {
    private CustomerRepository customerRepo;
    private LoanRepository loanRepo;

    CreateLoanResponse execute(CreateLoanRequest request) {
        // 1. Validate contact info
        // 2. Verify credit score ≥ 500
        // 3. Delegate to Loan entity for interest calculation
        // 4. Return response
    }
}
```

### 6. Entity–Use Case Dependency Direction

Entities have **no knowledge** of the use cases that control them. Entities are high level (generalizations usable across many applications, farthest from I/O). Use cases are lower level (specific to a single application, closer to I/O).

Dependency direction follows the Dependency Inversion Principle:

```
Use Case → Entity   (correct)
Entity → Use Case   (wrong—violates level)
```

This is another manifestation of the policy-level principle: high-level concepts know nothing of lower-level concepts. The lower-level concepts know about the higher-level ones.

### 7. Request and Response Models (Simple, Independent Data Structures)

Use cases expect input data and produce output data, but a well-formed use case object should have **no inkling** about how data is communicated. The use case class must not know about HTML, SQL, `HttpRequest`, or `HttpResponse`.

Use cases accept **simple request data structures** for input and return **simple response data structures** for output:

```java
// Plain data — no framework dependencies
class CreateLoanRequest {
    String name;
    String email;
    double requestedAmount;
}

class CreateLoanResponse {
    long loanId;
    double monthlyPayment;
    PaymentSchedule schedule;
}
```

These structures are not dependent on anything. They do not derive from framework interfaces. They know nothing of the web or any user interface.

**Critical warning: Do not let request/response models contain references to Entity objects.** Even though they share much data, their purposes are different. Over time they will change for different reasons. Tying them together violates the Common Closure Principle and the Single Responsibility Principle, leading to tramp data and unnecessary conditionals.

### 8. Business Rules as the Heart of the System

Business rules are the reason a software system exists. They carry the code that makes or saves money. They are the family jewels. The business rules should remain pristine, with all lesser concerns—user interfaces, databases, frameworks—plugged in to them. The business rules should be the most independent and reusable code in the system.

---

## Summary Checklist

- [ ] Define level as "distance from inputs and outputs"—higher level = farther from I/O
- [ ] Group policies that change for the same reasons at the same times into the same component
- [ ] Ensure every source code dependency points from lower-level toward higher-level policy
- [ ] Decouple source code dependencies from data flow; couple them to level instead
- [ ] Design lower-level components as plugins to higher-level components
- [ ] Identify Critical Business Rules: rules that make/save money even without automation
- [ ] Encapsulate Critical Business Rules and Critical Business Data together as Entities
- [ ] Keep Entities pure—no dependencies on databases, UIs, or frameworks
- [ ] Capture application-specific business rules as Use Cases that orchestrate Entities
- [ ] Ensure Entities have zero knowledge of the use cases that control them
- [ ] Use plain request/response data structures with no framework dependencies for use case I/O
- [ ] Never include Entity references in request/response models—they change for different reasons
- [ ] Position business rules as the heart of the system; plug everything else into them

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[SOLID Design Principles]]
- [[Boundaries]]
- [[Architectural Independence]]
- [[Presenters and Humble Objects]]
- [[Case Study - Video Sales]]
