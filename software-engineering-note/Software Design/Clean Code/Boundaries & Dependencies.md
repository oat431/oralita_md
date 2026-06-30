---
tags:
- clean-code
- software-design
- software-engineering
---

# Boundaries & Dependencies

**Source:** *Clean Code* — Robert C. Martin, Chapter 8 by James Grenning  
**Domain:** [[Clean Code Principles]] · [[Class Design & SOLID]] · [[System Architecture]] · [[Code Smells Catalog]]

---

> "It's better to depend on something you control than on something you don't control, lest it end up controlling you."

---

## Key Insight

We seldom control all the software in our systems. Third-party packages, open-source libraries, and subsystems built by other teams all create **boundaries** between foreign code and our own. The practices below keep those boundaries clean, testable, and cheap to maintain.

---

## Principles

### **Encapsulate Third-Party APIs** — Never pass boundary interfaces around your system

Third-party interfaces (like `java.util.Map`) are designed for **broad applicability**, not for your specific needs. They expose far more surface area than you need — `clear()`, `putAll()`, untyped entries — and their signatures change across versions (as `Map` did when Java 5 added generics).

**Smell — raw Map leaking through the codebase:**

```java
// BAD: Map exposed everywhere; every caller must cast
Map sensors = new HashMap();
Sensor s = (Sensor) sensors.get(sensorId);

// Still bad: generics don't solve the surface-area problem
Map<Sensor> sensors = new HashMap<Sensor>();
Sensor s = sensors.get(sensorId);
```

**Clean — boundary hidden inside one class:**

```java
// GOOD: Map is an implementation detail; casting lives in one place
public class Sensors {
    private Map<String, Sensor> sensors = new HashMap<>();

    public Sensor getById(String id) {
        return sensors.get(id);
    }

    // Business rules enforced here — no caller can clear(), putAll(), etc.
}
```

**Rule:** Keep boundary interfaces like `Map` inside the class or close family of classes where they're used. **Never** return them from or accept them as arguments to public APIs.

---

### **Write Learning Tests** — Explore third-party code through tests, not production code

When you don't know how a library works, the worst thing you can do is experiment inside your production code — mixing "learning" with "building." Instead, write isolated unit tests that call the API the way your application intends to use it.

**Jim Newkirk's learning test approach — progressive exploration of log4j:**

| Attempt | What we learned |
|---------|-----------------|
| `Logger.getLogger("x").info("hello")` | We need an `Appender` |
| `new ConsoleAppender()` — added | Appender has no output stream yet |
| `new ConsoleAppender(new PatternLayout(...), SYSTEM_OUT)` | Works! But `SYSTEM_OUT` is optional — odd behaviour |
| `BasicConfigurator.configure()` | Simplest one-liner for console logging |

```java
// Learning tests encode discovered API knowledge
public class LogTest {
    private Logger logger;

    @Before
    public void initialize() {
        logger = Logger.getLogger("logger");
        logger.removeAllAppenders();
        Logger.getRootLogger().removeAllAppenders();
    }

    @Test
    public void basicLogger() {
        BasicConfigurator.configure();
        logger.info("basicLogger");
    }

    @Test
    public void addAppenderWithStream() {
        logger.addAppender(new ConsoleAppender(
            new PatternLayout("%p %t %m%n"),
            ConsoleAppender.SYSTEM_OUT));
        logger.info("addAppenderWithStream");
    }

    @Test
    public void addAppenderWithoutStream() {
        logger.addAppender(new ConsoleAppender(
            new PatternLayout("%p %t %m%n")));
        logger.info("addAppenderWithoutStream");
    }
}
```

**Value:** You had to learn the API anyway. Tests give you an **easy, isolated** way to get that knowledge — plus a regression suite that flags breaking changes when you upgrade the library.

---

### **Learning Tests Are Better Than Free** — They have positive ROI

Learning tests cost nothing because the time was already spent learning the API. But they also pay dividends:

1. **Upgrade safety.** Run learning tests against new releases to detect behavioural differences *immediately*.
2. **Migration confidence.** Without boundary tests, you'll be tempted to stay on old versions longer than you should — accumulating technical debt.
3. **Living documentation.** The tests document *exactly* how your application expects the API to behave.

> A clean boundary should be supported by a set of **outbound tests** that exercise the interface the same way the production code does.

---

### **Define the Interface You Wish You Had** — Use the Adapter pattern for code that doesn't exist yet

When a subsystem you depend on hasn't been built yet (or its API is undefined), don't wait. **Define your own interface** — the one you *wish* you had — and code against that. Later, when the real API arrives, bridge the gap with an **Adapter**.

**The Transmitter example:**

```java
// 1. Define the interface YOU control — the one you wish existed
public interface Transmitter {
    void transmit(Frequency frequency, DataStream stream);
}

// 2. Code against your own interface; stays clean and expressive
public class CommunicationsController {
    private final Transmitter transmitter;

    public CommunicationsController(Transmitter transmitter) {
        this.transmitter = transmitter;
    }

    public void send(Frequency freq, DataStream data) {
        transmitter.transmit(freq, data);
    }
}

// 3. When the real API finally arrives, bridge with ONE adapter
public class TransmitterAdapter implements Transmitter {
    private final TransmitterAPI realApi;   // the third-party / external API

    public TransmitterAdapter(TransmitterAPI realApi) {
        this.realApi = realApi;
    }

    @Override
    public void transmit(Frequency frequency, DataStream stream) {
        realApi.keyOn(frequency);
        realApi.emitAnalog(stream);
    }
}
```

**Why this wins:**
- Your code stays **readable** and **focused** on what it's trying to accomplish.
- `CommunicationsController` never knows about the real API.
- You can test with a **FakeTransmitter** right away — no waiting.
- When the real API changes, only the **one** Adapter needs updating.

---

### **Clean Boundaries** — Fewer touch-points, stronger separation

Change happens at boundaries. Good designs absorb it without huge rework.

| Strategy | When to use |
|----------|-------------|
| **Wrap** the library in your own class | The API is simple and you only need a subset (like `Map` → `Sensors`) |
| **Adapter** from your ideal interface to the real one | The external system is complex or doesn't exist yet |
| **Learning tests + outbound tests** | Always — for every third-party integration |

**The invariant:** Have **very few places** in the code that refer to third-party details. Whether wrapping or adapting, your code should speak in *your* domain language, promote **internally consistent usage**, and have **fewer maintenance points** when the third-party code changes.

---

## Checklist

- [ ] No third-party interface (`Map`, `HttpClient`, etc.) is returned from or accepted by a public method.
- [ ] Every third-party integration has at least one learning test that exercises the API the way production code does.
- [ ] Learning tests are re-run against every library upgrade before merging.
- [ ] Subsystems that don't exist yet have a clean, self-defined interface coded against using an Adapter shim.
- [ ] Boundary-wrapping classes enforce business rules (types, invariants, access control).
- [ ] The word count of "third-party imports" in domain logic classes is zero or near-zero.

---

## Related

- [[Clean Code Principles]] — the chapter's parent discipline
- [[Class Design & SOLID]] — Dependency Inversion: depend on abstractions you own
- [[System Architecture]] — boundaries as architectural seams
- [[Code Smells Catalog]] — *Inappropriate Intimacy* (with foreign code), *Shotgun Surgery* (Map signature changes)
- [[Clean Code Overview]] — Adapter, Facade (wrapping), Seam (testing)
- *Test-Driven Development* — Kent Beck (learning tests origin)
- *Working Effectively with Legacy Code* — Michael Feathers (seams)
