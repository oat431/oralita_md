---
tags:
- clean-code
- software-design
- software-engineering
---

# Error Handling

> *"Error handling is important, but if it obscures logic, it's wrong."*
> — Michael Feathers, *Clean Code* Chapter 7

**Source:** Robert C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship*, Chapter 7, by Michael Feathers.

---

## Core Principle

Clean code is readable **and** robust — these are not conflicting goals. Treat error handling as a **separate concern**, viewable independently of main logic. When error handling dominates and obscures what the code actually does, the code is wrong.

---

## Rules

### **Use Exceptions Rather Than Return Codes**

Return codes and error flags clutter the caller, force immediate error checking after every call, and are easy to forget. Exceptions separate the algorithm from error handling into two distinct concerns you can understand independently.

**Before (return codes):**

```java
public void sendShutDown() {
    DeviceHandle handle = getHandle(DEV1);
    if (handle != DeviceHandle.INVALID) {
        retrieveDeviceRecord(handle);
        if (record.getStatus() != DEVICE_SUSPENDED) {
            pauseDevice(handle);
            clearDeviceWorkQueue(handle);
            closeDevice(handle);
        } else {
            logger.log("Device suspended. Unable to shut down");
        }
    } else {
        logger.log("Invalid handle for: " + DEV1.toString());
    }
}
```

**After (exceptions):**

```java
public void sendShutDown() {
    try {
        tryToShutDown();
    } catch (DeviceShutDownError e) {
        logger.log(e);
    }
}

private void tryToShutDown() throws DeviceShutDownError {
    DeviceHandle handle = getHandle(DEV1);
    DeviceRecord record = retrieveDeviceRecord(handle);
    pauseDevice(handle);
    clearDeviceWorkQueue(handle);
    closeDevice(handle);
}
```

---

### **Write Your Try-Catch-Finally Statement First**

A `try` block defines a transaction-like scope: execution can abort at any point and resume at the `catch`. Start with the `try-catch-finally` structure to define what the caller should expect, then use TDD to build the logic inside.

```java
// 1. Write the test first
@Test(expected = StorageException.class)
public void retrieveSectionShouldThrowOnInvalidFileName() {
    sectionStore.retrieveSection("invalid-file");
}

// 2. Write the try-catch skeleton
public List<RecordedGrip> retrieveSection(String sectionName) {
    try {
        FileInputStream stream = new FileInputStream(sectionName);
        stream.close();
    } catch (FileNotFoundException e) {
        throw new StorageException("retrieval error", e);
    }
    return new ArrayList<RecordedGrip>();
}

// 3. Refactor: narrow exception types, add logic within the try block
```

The `catch` must leave the program in a **consistent state** no matter what happens in the `try`.

---

### **Use Unchecked Exceptions**

Checked exceptions violate the [[Open/Closed Principle]]: a new checked exception at a low level forces signature changes on every method in the call chain up to the handler. This breaks encapsulation — all intermediate methods must know about a low-level detail they don't care about.

- **Cost:** Cascading signature changes, forced rebuilds/redeploys, broken encapsulation.
- **Reality:** C#, C++, Python, and Ruby produce robust software without checked exceptions.
- **Verdict:** In general application development, the dependency cost outweighs the benefit. Reserve checked exceptions for critical libraries where callers truly *must* handle them.

---

### **Provide Context with Exceptions**

Every exception should carry enough information to determine the **source**, **location**, and **intent** of the failed operation. A stack trace alone is insufficient — it can't tell you what the code was *trying* to do.

- Mention the **operation that failed** and the **type of failure**.
- Pass enough information to log the error meaningfully in the `catch` block.

```java
throw new StorageException("retrieval error for section: " + sectionName, e);
```

---

### **Define Exception Classes in Terms of the Caller's Needs**

Classify exceptions by **how they are caught**, not by their source or type. Most handlers do the same thing regardless of the cause: log the error and move on. Wrapping third-party APIs into a common exception type eliminates duplication.

**Before (multiple catch blocks, duplicated handling):**

```java
ACMEPort port = new ACMEPort(12);
try {
    port.open();
} catch (DeviceResponseException e) {
    reportPortError(e);
    logger.log("Device response exception", e);
} catch (ATM1212UnlockedException e) {
    reportPortError(e);
    logger.log("Unlock exception", e);
} catch (GMXError e) {
    reportPortError(e);
    logger.log("Device response exception");
} finally {
    // ...
}
```

**After (wrapped API, single catch):**

```java
LocalPort port = new LocalPort(12);
try {
    port.open();
} catch (PortDeviceFailure e) {
    reportError(e);
    logger.log(e.getMessage(), e);
} finally {
    // ...
}

// Wrapper translates third-party exceptions into a single type
public class LocalPort {
    private ACMEPort innerPort;

    public LocalPort(int portNumber) {
        innerPort = new ACMEPort(portNumber);
    }

    public void open() {
        try {
            innerPort.open();
        } catch (DeviceResponseException e) {
            throw new PortDeviceFailure(e);
        } catch (ATM1212UnlockedException e) {
            throw new PortDeviceFailure(e);
        } catch (GMXError e) {
            throw new PortDeviceFailure(e);
        }
    }
}
```

**Wrapping third-party APIs is a best practice:** it minimizes coupling, simplifies mocking in tests, and frees you from vendor API design choices. Often a single exception class per area of code is sufficient — use different classes only when you need to catch one and let another pass through.

---

### **Define the Normal Flow — The Special Case Pattern**

When exceptional behavior can be handled with a sensible default rather than aborting, encapsulate the special case in an object. The client code stays clean and free of `try-catch` clutter.

**Before (exception clutters business logic):**

```java
try {
    MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
    m_total += expenses.getTotal();
} catch (MealExpensesNotFound e) {
    m_total += getMealPerDiem();
}
```

**After (Special Case object):**

```java
MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
m_total += expenses.getTotal();

// The DAO always returns a MealExpenses object:
public class PerDiemMealExpenses implements MealExpenses {
    public int getTotal() {
        return getMealPerDiem();  // the default
    }
}
```

[[Special Case Pattern]] encapsulates exceptional behavior so the client never has to deal with it.

---

### **Don't Return Null**

Returning `null` creates work for every caller and invites `NullPointerException`. One missing null check can crash the application. Instead, throw an exception or return a **Special Case object**.

**Before:**

```java
List<Employee> employees = getEmployees();
if (employees != null) {
    for (Employee e : employees) {
        totalPay += e.getPay();
    }
}
```

**After (empty list instead of null):**

```java
List<Employee> employees = getEmployees();
for (Employee e : employees) {
    totalPay += e.getPay();
}

public List<Employee> getEmployees() {
    if (/* no employees */) {
        return Collections.emptyList();
    }
    // ...
}
```

For third-party APIs that return null, **wrap them** with a method that either throws or returns a special case object.

---

### **Don't Pass Null**

Passing `null` is worse than returning it — most languages have no graceful way to handle a `null` argument from a careless caller. Forbid passing null by default: treat a null argument as an indication of a bug.

```java
public double xProjection(Point p1, Point p2) {
    if (p1 == null || p2 == null) {
        throw new IllegalArgumentException(
            "Invalid argument for MetricsCalculator.xProjection");
    }
    return (p2.x - p1.x) * 1.5;
}
```

Assertions (`assert p1 != null`) document intent but don't solve the runtime problem. The rational approach: **forbid null by default** and code with the confidence that null means a mistake.

---

## Checklist

- [ ] Exceptions used instead of return codes or error flags
- [ ] Try-catch-finally written first, defining the transaction scope before logic
- [ ] Checked exceptions avoided in general application code
- [ ] Every exception carries meaningful context (operation, failure type, relevant data)
- [ ] Exception classes defined by caller's needs, not by source or category
- [ ] Third-party APIs wrapped to translate exceptions into a common type
- [ ] Special Case objects used where defaults can replace exceptional flow
- [ ] Methods never return `null` — throw or return a Special Case / empty collection
- [ ] Methods never accept `null` — treat it as a programming error
- [ ] Error handling is a separate concern, independently viewable from business logic

---

## See Also

- [[Clean Code Principles]]
- [[Function Design]]
- [[Code Smells Catalog]]
- [[Open/Closed Principle]]
- [[Special Case Pattern]]
- [[Logging Best Practices]]
