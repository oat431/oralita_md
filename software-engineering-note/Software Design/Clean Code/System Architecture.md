---
tags:
- clean-code
- software-design
- software-engineering
---

# System Architecture

**Source:** Robert C. Martin, *Clean Code*, Chapter 11 (pp. 153–170), by Dr. Kevin Dean Wampler

> "Complexity kills. It sucks the life out of developers, it makes products difficult to plan, build, and test."
> —Ray Ozzie, CTO, Microsoft Corporation

---

## The City Metaphor

Cities work because **no single person manages everything.** Separate teams own water, power, traffic, law enforcement — each with appropriate levels of abstraction and modularity. Software systems need the same: **clean separation of concerns at the system level,** not just at the module level.

---

## Rules

### 1. Separate Construction from Use

Construction and runtime are **different processes.** A hotel under construction — cranes, hard hats, bare concrete — looks nothing like the finished building with guests checking in. Software must separate the startup wiring phase from the runtime logic phase.

**The anti-pattern — Lazy Initialization mixed with business logic:**

```java
// BEFORE: Construction and use are entangled
public Service getService() {
    if (service == null)
        service = new MyServiceImpl(...); // Hard-coded dependency
    return service;
}
```

Problems with this idiom:
- **Hard-coded dependency** on `MyServiceImpl` — cannot compile without it.
- **Testing is harder** — requires test doubles before the method is called.
- **Violates SRP** — the method does construction AND business logic.
- **Hidden global context** — is `MyServiceImpl` really right for *all* contexts?

```java
// AFTER: Construction moved out; object receives its dependency
public class OrderProcessor {
    private final Service service;

    // Constructor injection — dependencies wired by main/container
    public OrderProcessor(Service service) {
        this.service = service;
    }

    public void process(Order order) {
        service.execute(order); // Pure runtime logic
    }
}
```

### 2. Separation of `main`

Move **all construction and wiring to `main`** (or modules `main` calls). The application itself simply *uses* objects that are already built.

**Rule:** All dependency arrows point **away from `main`** into the application. The application has **zero knowledge** of `main` or the construction process.

```
main ──creates──> Application
                 Application expects everything already wired.
                 Application NEVER imports or references main.
```

### 3. Use Factories When the Application Controls *When* to Create

When the application decides **when** to create an object (e.g., `Order` creates `LineItem`s at runtime) but should **not** know **how** to construct it, use the **Abstract Factory pattern.**

```
main ──> LineItemFactoryImplementation ──implements──> LineItemFactory
                                                         ↑
                                             Application uses factory interface only
```

- The **factory interface** lives on the application side.
- The **factory implementation** lives on the `main` side.
- The application **controls timing** and passes constructor arguments.
- The application is **decoupled** from construction details.

```java
// Factory interface — application knows only this
public interface LineItemFactory {
    LineItem create(Product product, int quantity);
}

// Concrete factory — on the main side, invisible to application
public class LineItemFactoryImpl implements LineItemFactory {
    private final PricingService pricing;

    public LineItemFactoryImpl(PricingService pricing) {
        this.pricing = pricing;
    }

    public LineItem create(Product product, int quantity) {
        return new LineItem(product, quantity, pricing.calculate(product, quantity));
    }
}

// Application code — uses factory, never knows implementation
public class OrderProcessor {
    private final LineItemFactory lineItemFactory;

    public OrderProcessor(LineItemFactory lineItemFactory) {
        this.lineItemFactory = lineItemFactory;
    }

    public void addItem(Order order, Product product, int qty) {
        order.add(lineItemFactory.create(product, qty));
    }
}
```

### 4. Dependency Injection (DI)

Dependency Injection is **Inversion of Control applied to dependency management.** An object should never instantiate its own dependencies. A dedicated mechanism (container or `main`) wires everything together.

**Three forms:**

| Form | How | When to use |
|------|-----|-------------|
| **Constructor injection** | Dependencies passed via constructor | Required dependencies, immutability preferred |
| **Setter injection** | Dependencies passed via setter methods | Optional or reconfigurable dependencies |
| **Interface injection** | Object implements interface that receives dependencies | Less common; framework-specific |

**JNDI lookups are a *partial* DI** — the object still *actively* resolves its dependency by name. True DI makes the class **completely passive.**

```java
// BEFORE: Active dependency resolution (JNDI — partial DI)
MyService myService = (MyService) jndiContext.lookup("NameOfMyService");

// AFTER: Passive — container injects via constructor or setter
public class Client {
    private final MyService myService;

    public Client(MyService myService) {   // Constructor injection
        this.myService = myService;
    }
}
```

**Spring Framework example (XML configuration):**

```xml
<!-- Spring 2.x configuration: beans are wired by the container -->
<beans>
    <bean id="appDataSource"
          class="org.apache.commons.dbcp.BasicDataSource"
          destroy-method="close"
          p:driverClassName="com.mysql.jdbc.Driver"
          p:url="jdbc:mysql://localhost:3306/mydb"
          p:username="me" />

    <bean id="bankDataAccessObject"
          class="com.example.banking.persistence.BankDataAccessObject"
          p:dataSource-ref="appDataSource" />

    <bean id="bank"
          class="com.example.banking.model.Bank"
          p:dataAccessObject-ref="bankDataAccessObject" />
</beans>
```

At runtime, the container assembles a **Russian-doll chain of decorators:** Bank ↔ DAO ↔ DataSource. The client thinks it's calling `getAccounts()` on a `Bank`, but it's talking to the outermost decorator of a nested, transparently-proxied chain.

```java
// Application code — nearly zero framework coupling
XmlBeanFactory bf = new XmlBeanFactory(new ClassPathResource("app.xml"));
Bank bank = (Bank) bf.getBean("bank");
```

**Lazy initialization is still possible with DI:** most containers don't construct objects until needed, and many provide proxy/factory mechanisms for lazy evaluation. But remember — lazy initialization is an *optimization* and may be premature.

### 5. Scale Incrementally — Don't Build a Highway Through a Village

> "It is a myth that we can get systems 'right the first time.'"

Cities grow: narrow paths → paved roads → widened streets → highways. Services (power, water, internet) are added as density increases. You don't build a six-lane highway through a small town "just in case."

**Software architectures CAN grow incrementally** — unlike physical buildings — because software is ephemeral and we can maintain proper separation of concerns.

**Counterexample — EJB2:** Did *not* separate concerns adequately.
- Required subclassing container types.
- Required empty lifecycle methods (`ejbActivate`, `ejbPassivate`, etc.).
- Tight coupling to heavyweight container made unit testing nearly impossible.
- Reuse outside EJB2 impossible.
- DTOs (Data Transfer Objects) created redundant types with boilerplate copying code.
- One bean couldn't inherit from another — undermined OOP itself.

**EJB2 before vs. EJB3 after:**

```java
// BEFORE: EJB2 — invasive, tightly coupled, verbose
public abstract class Bank implements javax.ejb.EntityBean {
    public abstract String getStreetAddr1();
    public abstract String getCity();
    // ... 10+ abstract getters/setters for every attribute

    public void addAccount(AccountDTO accountDTO) {
        InitialContext context = new InitialContext();
        AccountHomeLocal accountHome = context.lookup("AccountHomeLocal");
        AccountLocal account = accountHome.create(accountDTO);
        Collection accounts = getAccounts();
        accounts.add(account);
    }

    // Required empty lifecycle boilerplate
    public void ejbActivate() {}
    public void ejbPassivate() {}
    public void ejbLoad() {}
    public void ejbStore() {}
    public void ejbRemove() {}
    public void setEntityContext(EntityContext ctx) {}
    public void unsetEntityContext() {}
}

// AFTER: EJB3 — clean POJO with annotations, testable
@Entity
@Table(name = "BANKS")
public class Bank implements java.io.Serializable {
    @Id @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;

    @Embedded
    private Address address;

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER, mappedBy = "bank")
    private Collection<Account> accounts = new ArrayList<>();

    public void addAccount(Account account) {
        account.setBank(this);
        accounts.add(account);
    }

    public Collection<Account> getAccounts() { return accounts; }
}
```

### 6. Handle Cross-Cutting Concerns with Aspects

**Cross-cutting concerns** are concerns like persistence, transactions, security, caching, and logging that cut across natural domain object boundaries. You want a *consistent* persistence strategy, but the code implementing it ends up scattered across many objects.

**Aspect-Oriented Programming (AOP)** restores modularity for these concerns. An *aspect* declares: "at these points in the system, modify behavior in this consistent way to support this concern" — all done *noninvasively* (no manual editing of target source code).

Three aspect-like mechanisms in Java, in increasing power and complexity:

#### a. Java Dynamic Proxies

Suitable for simple method-wrapping on individual objects. Only works with **interfaces** (JDK proxies); for classes, you need byte-code libraries (CGLIB, ASM, Javassist).

```java
// Interface the proxy wraps
public interface Bank {
    Collection<Account> getAccounts();
    void setAccounts(Collection<Account> accounts);
}

// POJO implementation — pure business logic
public class BankImpl implements Bank {
    private List<Account> accounts;

    public Collection<Account> getAccounts() { return accounts; }
    public void setAccounts(Collection<Account> accounts) {
        this.accounts = new ArrayList<>(accounts);
    }
}

// InvocationHandler — persistence cross-cutting via proxy
public class BankProxyHandler implements InvocationHandler {
    private Bank bank;

    public BankProxyHandler(Bank bank) { this.bank = bank; }

    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        String methodName = method.getName();
        if (methodName.equals("getAccounts")) {
            bank.setAccounts(getAccountsFromDatabase());
            return bank.getAccounts();
        } else if (methodName.equals("setAccounts")) {
            bank.setAccounts((Collection<Account>) args[0]);
            setAccountsToDatabase(bank.getAccounts());
            return null;
        }
        // ... delegate other methods
    }

    protected Collection<Account> getAccountsFromDatabase() { /* DB access */ }
    protected void setAccountsToDatabase(Collection<Account> accounts) { /* DB access */ }
}

// Wiring
Bank bank = (Bank) Proxy.newProxyInstance(
    Bank.class.getClassLoader(),
    new Class[] { Bank.class },
    new BankProxyHandler(new BankImpl()));
```

**Drawbacks:** Lots of boilerplate code, no mechanism for specifying *system-wide* join points, complexity even for simple cases. Hard to create clean code.

#### b. Pure Java AOP Frameworks (Spring AOP)

Handles **80–90% of aspect use cases.** Write plain POJOs focused purely on domain logic — no dependencies on enterprise frameworks. Declare infrastructure (persistence, transactions, security, caching) in configuration files or annotations. The framework transparently handles proxies/byte-code manipulation.

**Spring transaction management example:**

```java
// Pure POJO — no framework dependency
public class OrderService {
    private final OrderRepository repository;
    private final PaymentGateway payment;

    public OrderService(OrderRepository repository, PaymentGateway payment) {
        this.repository = repository;
        this.payment = payment;
    }

    @Transactional  // Declarative: Spring AOP handles begin/commit/rollback
    public void placeOrder(Order order) {
        payment.charge(order.getTotal());
        repository.save(order);
    }
}
```

Without any explicit transaction code, Spring's AOP framework wraps the method: opens a transaction before `placeOrder` executes, commits on success, rolls back on exception. The domain logic stays clean.

**EJB3 adopted this model** — declarative cross-cutting concerns via annotations/XML, leaving pure POJOs underneath.

#### c. AspectJ

The most **full-featured** AOP tool. An extension of Java providing first-class aspect constructs. Rich pointcut language for specifying *exactly* which join points to advise. **Drawback:** requires learning new tools, language constructs, and idioms. Mitigated by an annotation-based form of AspectJ (using Java 5 annotations).

| Approach | Power | Complexity | When |
|----------|-------|-----------|------|
| JDK Proxies | Low | Moderate | Simple single-object wrapping |
| Spring AOP / JBoss AOP | Medium–High | Low | 80–90% of cross-cutting needs |
| AspectJ | Very High | High | Remaining 10–20% of complex cases |

### 7. Test-Drive the Architecture

> "An optimal system architecture consists of modularized domains of concern, each implemented with Plain Old Java Objects. The different domains are integrated together with minimally invasive Aspects or Aspect-like tools. This architecture can be test-driven, just like the code."

**Big Design Up Front (BDUF) is harmful:**
- Inhibits adapting to change (psychological resistance to discarding prior effort).
- Architecture choices influence all subsequent design thinking — lock-in.
- Physical architects must do BDUF (can't radically change a skyscraper mid-construction), but software is *economically feasible* to change — **if** concerns are well-separated.

**Strategy:** Start with a "naively simple" but well-decoupled architecture. Deliver working user stories quickly. Add infrastructure (caching, security, virtualization) incrementally as you scale. The world's largest websites achieved high availability and performance this way — not through BDUF.

### 8. Defer Decisions to the Last Responsible Moment

> "It is best to postpone decisions until the last possible moment. This isn't lazy or irresponsible; it lets us make informed choices with the best possible information."

A **premature decision** is made with suboptimal knowledge: less customer feedback, less project reflection, less implementation experience.

The agility of a POJO system with modularized concerns *enables* just-in-time decision-making. Complexity of decisions is reduced because you have more information when you decide.

### 9. Use Standards Only When They Add Demonstrable Value

Standards can make it easier to reuse ideas, recruit experienced people, encapsulate good practices, and wire components together. But:

- **EJB2 was adopted because it was a standard** — even when lighter, simpler designs would have been sufficient.
- Standards creation can be too slow for the industry.
- Some standards lose touch with real adopter needs.

**Test:** Does this standard *demonstrably* help deliver customer value, or are we adopting it because it's hyped?

### 10. Build Domain-Specific Languages (DSLs)

DSLs minimize the **communication gap** between a domain concept and the code that implements it. A good DSL lets code read like structured prose that a domain expert would write — you're implementing domain logic in the *same language* the domain expert uses.

DSLs raise the abstraction level above code idioms and design patterns. They allow all levels of abstraction — from high-level policy to low-level details — to be expressed as POJOs.

```java
// Without DSL: low-level API, intent obscured
Order order = new Order();
order.setCustomerId(12345);
order.setStatus("PENDING");
order.addProduct(product, 2, Discounts.STANDARD);

// With DSL: reads like the domain
order.forCustomer(12345)
     .withStatus(PENDING)
     .addLine(product, quantity: 2, discount: standard);
```

---

## Java Code Examples Summary

### Before (Construction Mixed with Use)

```java
// Anti-pattern: LAZY INITIALIZATION entangled with business logic
public Service getService() {
    if (service == null)
        service = new MyServiceImpl(...); // Hard-coded, untestable, SRP violation
    return service;
}

// Anti-pattern: EJB2 Entity Bean — invasive, tightly coupled
public abstract class Bank implements javax.ejb.EntityBean {
    public abstract String getStreetAddr1();
    public abstract void setStreetAddr1(String s);
    public void addAccount(AccountDTO dto) {
        InitialContext ctx = new InitialContext();
        AccountHomeLocal home = ctx.lookup("AccountHomeLocal");
        // ... boilerplate, lifecycle methods, DTO copying
    }
    public void ejbActivate() {}
    public void ejbPassivate() {}
    // ... 5+ more empty lifecycle methods
}
```

### After (Clean Separation, DI + AOP + POJOs)

```java
// Constructor Injection — dependencies wired externally
public class OrderProcessor {
    private final Service service;

    public OrderProcessor(Service service) {
        this.service = service;
    }

    public void process(Order order) {
        service.execute(order);
    }
}

// Abstract Factory — app controls WHEN, main controls HOW
public interface LineItemFactory {
    LineItem create(Product product, int quantity);
}

// EJB3 / Spring POJO — clean, testable, annotated for cross-cutting concerns
@Entity
@Table(name = "BANKS")
public class Bank implements Serializable {
    @Id @GeneratedValue
    private int id;

    @Embedded private Address address;

    @OneToMany(cascade = ALL, fetch = EAGER, mappedBy = "bank")
    private Collection<Account> accounts = new ArrayList<>();

    public void addAccount(Account account) {
        account.setBank(this);
        accounts.add(account);
    }
}

// Declarative transaction management via Spring AOP
@Service
public class OrderService {
    @Transactional
    public void placeOrder(Order order) {
        payment.charge(order.getTotal());
        repository.save(order);  // No transaction code — AOP handles it
    }
}
```

---

## Checklist: System Architecture Design

- [ ] **Startup wiring is separated from runtime logic** — no lazy initialization in business methods
- [ ] **`main` (or DI container) owns all construction** — dependency arrows point one way, away from main
- [ ] **Abstract Factory is used** when the application controls *when* but not *how* to create objects
- [ ] **Dependencies are injected** (constructor/setter), never looked up — classes are passive
- [ ] **All domain logic lives in POJOs** — zero dependencies on frameworks or containers
- [ ] **Cross-cutting concerns** (persistence, transactions, security, caching) are handled via AOP or declarative configuration
- [ ] **Architecture can be test-driven** — domain logic testable without mocking containers
- [ ] **System grows incrementally** — no Big Design Up Front; start simple, scale as needed
- [ ] **Decisions are deferred** to the last responsible moment — maximum information before commitment
- [ ] **Standards are adopted only when they add demonstrable value** — not because they're trendy
- [ ] **DSLs are used** where they reduce the communication gap between domain and code
- [ ] **Simplest thing that can possibly work** is chosen at every level of abstraction

---

## Related Notes

- [[Clean Code Principles]]
- [[Class Design & SOLID]]
- [[Boundaries & Dependencies]]
- [[Code Smells Catalog]]
- [[System Architecture]]
- [[System Architecture]]
- [[Unit Testing]]
- [[System Architecture]]
