---
tags:
- book-summary
- pragmatic-programmer
- professionalism
- software-engineering
---

# 04 Pragmatic Paranoia (Tips 30–35)

You can't write perfect software. Acknowledge that — and write code that survives when things go wrong.

---

## Tip 30: You Can't Write Perfect Software

> Accept this. It's liberating.

Once you accept that bugs WILL exist, you start designing defensively. You add checks. You write tests. You crash early rather than corrupting data. Paranoia is a virtue.

---

## Tip 31: Design by Contract

> Every function has a contract: preconditions (what it expects), postconditions (what it guarantees), and invariants (what stays true).

| Term | Meaning | Example |
|------|---------|---------|
| **Precondition** | What must be true before the function runs | "The account balance must be ≥ withdrawal amount" |
| **Postcondition** | What the function guarantees after running | "The account balance is reduced by exactly the withdrawal amount" |
| **Invariant** | What remains true throughout | "The sum of all account balances equals the bank's total deposits" |

> If clients fulfill all preconditions, the function guarantees all postconditions and invariants remain true.

### In Practice

Languages with built-in DBC (Eiffel) enforce contracts at runtime. In Java/JavaScript/Python, use assertions and validation:

```java
public void withdraw(BigDecimal amount) {
    assert amount.compareTo(BigDecimal.ZERO) > 0 : "Amount must be positive";  // Precondition
    assert balance.compareTo(amount) >= 0 : "Insufficient funds";               // Precondition
    
    balance = balance.subtract(amount);                                         // Implementation
    
    assert previousBalance.subtract(amount).equals(balance);                    // Postcondition
}
```

---

## Tip 32: Dead Programs Tell No Lies — Crash Early

> A dead program is better than a crippled one.

When something impossible happens, **crash.** Don't try to keep running with corrupted state. A program that crashes tells you exactly where the problem is. A program that silently corrupts data might not be detected for weeks.

```java
// ❌ DON'T: silently handle impossible case
if (account == null) {
    return new EmptyAccount();  // Data just got lost. Nobody knows.
}

// ✅ DO: crash with context
if (account == null) {
    throw new IllegalStateException(
        "Account cannot be null at this point. Transaction ID: " + txnId);
}
```

---

## Tip 33: Assertive Programming — If It Can't Happen, Use Assertions

> Assertions prove that "impossible" things stay impossible.

Assertions are different from error handling:
- **Errors**: expected problems (network down, invalid input) — handle with exceptions
- **Assertions**: things that should NEVER happen — crash if they do

```java
// Assertion: this should NEVER happen
assert list.size() > 0 : "Sort called on empty list";

// Error handling: this CAN happen
if (file == null || !file.exists()) {
    throw new FileNotFoundException("Configuration file not found");
}
```

> Turn assertions OFF in production? Only for performance-critical checks. Leave them ON for everything else. The cost of a crash is usually less than the cost of silent corruption.

---

## Tip 34: When to Use Exceptions

> Use exceptions for exceptional problems. Not for control flow.

```java
// ❌ Exception as control flow
try {
    record = database.lookup(key);
} catch (RecordNotFoundException e) {
    record = createNewRecord(key);
}

// ✅ Check first
if (database.contains(key)) {
    record = database.lookup(key);
} else {
    record = createNewRecord(key);
}
```

Exceptions should be reserved for truly unexpected situations — not for "file not found" when the file is user-specified and might legitimately not exist.

---

## Tip 35: How to Balance Resources — Finish What You Start

> The function that allocates a resource is responsible for deallocating it.

```java
// ❌ Manual resource management
Connection conn = getConnection();
try {
    // use conn
} finally {
    conn.close();  // Don't forget this!
}

// ✅ Try-with-resources (Java) / using (C#) / with (Python)
try (Connection conn = getConnection()) {
    // use conn
} // Automatically closed
```

### Nesting Resources
1. Deallocate in reverse order of allocation
2. When allocating the same resource set, allocate in the same order
3. If a subsequent allocation fails, release the earlier ones (exception safety)

---

## Sources

- Hunt & Thomas. *The Pragmatic Programmer*, Chapter 4.
