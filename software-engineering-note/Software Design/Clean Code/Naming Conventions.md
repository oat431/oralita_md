---
tags:
- clean-code
- software-design
- software-engineering
---

# Naming Conventions

> *Source: Clean Code by Robert C. Martin, Chapter 2 (pp. 17–30), by Tim Ottinger*

---

## Core Principle

> **Names should reveal intent.** A variable, function, or class name should answer: why it exists, what it does, and how it's used.

Choosing good names takes time — but saves more than it costs. Change names when you find better ones. Everyone who reads your code (including future you) will be happier.

---

## The Rules

### 1. Use Intention-Revealing Names

If a name needs a comment, it fails.

```java
// ❌ Bad
int d; // elapsed time in days

// ✅ Good
int elapsedTimeInDays;
int daysSinceCreation;
int fileAgeInDays;
```

**The `getThem()` test:** If you can't understand a function in 10 seconds, the names are hiding intent:

```java
// ❌ What does this do?
public List<int[]> getThem() {
    List<int[]> list1 = new ArrayList<int[]>();
    for (int[] x : theList)
        if (x[0] == 4)
            list1.add(x);
    return list1;
}

// ✅ Same code, named for a minesweeper game:
public List<Cell> getFlaggedCells() {
    List<Cell> flaggedCells = new ArrayList<Cell>();
    for (Cell cell : gameBoard)
        if (cell.isFlagged())
            flaggedCells.add(cell);
    return flaggedCells;
}
```

### 2. Avoid Disinformation

Don't leave false clues. `accountList` should **actually be a `List`** — otherwise use `accountGroup` or `accounts`. Avoid `hp`, `aix`, `sco` (Unix platform names). Never use lowercase `l` or uppercase `O` as variable names — they look like `1` and `0`.

Spell similar concepts similarly. `XYZControllerForEfficientHandlingOfStrings` vs `XYZControllerForEfficientStorageOfStrings` is a bug waiting to happen.

### 3. Make Meaningful Distinctions

Don't satisfy the compiler with nonsense differences:

```java
// ❌ Number-series naming — zero intent
public static void copyChars(char a1[], char a2[]) { ... }

// ✅ Meaningful distinctions
public static void copyChars(char source[], char destination[]) { ... }
```

**Noise words are redundant:** `ProductInfo`, `ProductData`, `ProductObject` — what's the difference? `NameString` — would a name ever be a float? `moneyAmount` = `money`. `theMessage` = `message`.

```java
// ❌ Which one do I call?
getActiveAccount();
getActiveAccounts();
getActiveAccountInfo();
```

### 4. Use Pronounceable Names

Programming is a social activity. If you can't say it, you can't discuss it.

```java
// ❌ "gen-yah-mudda-hims"
class DtaRcrd102 {
    private Date genymdhms;
    private Date modymdhms;
    private final String pszqint = "102";
}

// ✅ "Hey, the generation timestamp is tomorrow's date!"
class Customer {
    private Date generationTimestamp;
    private Date modificationTimestamp;
    private final String recordId = "102";
}
```

### 5. Use Searchable Names

Single letters and magic numbers are impossible to grep for.

```java
// ❌ What does 5 mean? Where else is it used?
for (int j=0; j<34; j++) {
    s += (t[j]*4)/5;
}

// ✅ Searchable, self-documenting
int realDaysPerIdealDay = 4;
const int WORK_DAYS_PER_WEEK = 5;
int sum = 0;
for (int j=0; j < NUMBER_OF_TASKS; j++) {
    int realTaskDays = taskEstimate[j] * realDaysPerIdealDay;
    int realTaskWeeks = (realTaskDays / WORK_DAYS_PER_WEEK);
    sum += realTaskWeeks;
}
```

**Rule of thumb:** Name length should match scope size. Single-letter names are OK **only** as local variables inside short methods (e.g., loop counters `i`, `j`, `k`).

### 6. Avoid Encodings

No Hungarian notation. No `m_` member prefixes. Modern IDEs highlight types and members — encoding is visual debt.

```java
// ❌ Hungarian + member prefix
private String m_dsc;
void setName(String name) { m_dsc = name; }

// ✅ Clean
String description;
void setDescription(String description) { this.description = description; }
```

**Interfaces vs Implementations:** Don't prefix interfaces with `I`. Encode the *implementation* if you must (`ShapeFactoryImp`), not the interface. Users shouldn't care whether they're getting an interface.

### 7. Avoid Mental Mapping

Readers shouldn't mentally translate your names. A professional uses clarity, not clever mnemonics.

```java
// ❌ "r" = "lowercased URL with host and scheme removed"
// The reader must keep this mapping in their head
```

Smart programmers sometimes show off mental juggling. **Professional programmers use their powers for good** and write obvious code.

### 8. Class Names

- **Noun or noun phrase:** `Customer`, `WikiPage`, `Account`, `AddressParser`
- **Not a verb:** Don't name a class `Process`, `Manage`, `Handle`
- **Avoid:** `Manager`, `Processor`, `Data`, `Info` — these are noise words

### 9. Method Names

- **Verb or verb phrase:** `postPayment`, `deletePage`, `save`
- **Accessors/mutators/predicates:** `getName`, `setName`, `isPosted` (JavaBean standard)
- **Static factory methods over overloaded constructors:**

```java
// ❌ What does this constructor do?
Complex fulcrumPoint = new Complex(23.0);

// ✅ Descriptive factory method
Complex fulcrumPoint = Complex.FromRealNumber(23.0);
```

### 10. Don't Be Cute

```java
// ❌ Cute but opaque
HolyHandGrenade()    // DeleteItems?
eatMyShorts()        // abort?
whack()              // kill?

// ✅ Say what you mean
deleteItems()
abort()
kill()
```

Clarity over entertainment. Cultural jokes don't age well.

### 11. Pick One Word Per Concept

One lexicon, consistently applied:

| Concept | Stick to ONE |
|---------|--------------|
| Get data | `get` (not `fetch`, `retrieve`, `pull`) |
| Remove | `delete` (not `remove`, `destroy`, `kill`) |
| Add to collection | `add` or `append` or `insert` — pick one |

Same for class roles: don't have `DeviceManager`, `ProtocolController`, and `DataDriver` in the same codebase unless they're genuinely different.

### 12. Don't Pun

Using the same word for two different meanings is worse than using different words.

```java
// ❌ "add" means "concatenate two values" in 10 classes,
//    but "insert into collection" in this one
// → Use "insert" or "append" instead
```

### 13. Use Solution Domain Names

Your readers are programmers. Use CS terms, pattern names, algorithm names:
- `AccountVisitor` (VISITOR pattern) ✅
- `JobQueue` (every programmer knows what this is) ✅

### 14. Use Problem Domain Names

When there's no CS term, draw from the business domain. At least a domain expert can explain it later.

### 15. Add Meaningful Context

Bare variables without context are opaque:

```java
// ❌ firstName, lastName, street, city, state, zipcode
//    — are these part of something bigger?

// ✅ Wrap in a class
class Address {
    String firstName;
    String lastName;
    String street;
    String city;
    String state;
    String zipcode;
}
```

### 16. Don't Add Gratuitous Context

Shorter is better when the context is already clear:

```java
// ❌ In "Gas Station Deluxe" app
GSDAccountAddress  // 10 of 17 chars are redundant

// ✅
Address            // Clear enough within the module
PostalAddress      // If you need to distinguish from MAC, URI, etc.
```

---

## Summary Checklist

- [ ] Does the name reveal intent without needing a comment?
- [ ] Is it pronounceable? Can I discuss it in a meeting?
- [ ] Is it searchable? Can I grep for it?
- [ ] No encodings (Hungarian, `m_`, `I`-prefix)?
- [ ] No mental mapping required?
- [ ] Consistent with the rest of the codebase's lexicon?
- [ ] Right scope-to-length ratio (short for locals, longer for globals)?
- [ ] No cute names or culture-specific jokes?

---

## Related

- [[Function Design]] — Small functions reduce naming scope, making good names easier
- [[Comment Patterns]] — A comment is a failure to express yourself in code
- [[Class Design & SOLID]] — SRP keeps classes small, making class names more precise
- [[Code Smells Catalog]] — N1–N7 (naming-related heuristics)
