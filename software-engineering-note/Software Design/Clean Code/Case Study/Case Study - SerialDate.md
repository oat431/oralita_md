# Case Study: Refactoring SerialDate

**Source:** Robert C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship*, Chapter 16, pp. 267–284
**Context:** JCommon library — `org.jfree.date.SerialDate`, authored by David Gilbert.

> *"SerialDate is a class that represents a date in Java … This is not an activity of malice. Nor do I think that I am so much better than David that I somehow have a right to pass judgment on his code. … What I am about to do is nothing more and nothing less than a professional review. It is something that we should all be comfortable doing. And it is something we should welcome when it is done for us. It is only through critiques like these that we will learn."*

---

## 1. The Approach: First Make It Work, Then Make It Right

The refactoring of SerialDate is a textbook demonstration of the Boy Scout Rule in action—leave the code cleaner than you found it. But before any cleaning begins, the code must *work*. Uncle Bob approaches this in two distinct phases:

| Phase | Goal | Key Technique |
|-------|------|---------------|
| **Make It Work** | Achieve high test coverage and fix known bugs | Write independent unit tests; use coverage tools (Clover) |
| **Make It Right** | Improve design, readability, and structure | Top-to-bottom refinement; run all tests after every change |

**Why this order matters:** You cannot safely refactor without a safety net. If you refactor broken code, you risk introducing new bugs with no way to detect them. Test coverage is the prerequisite, not the afterthought.

---

## 2. Phase 1 — Make It Work: Test Coverage & Bug Fixing

### 2.1 The Starting State

- **185 executable statements** in SerialDate.
- Original tests cover only **91 statements (~50%)**—the coverage map looks "like a patchwork quilt."
- Several dead functions have zero coverage (e.g., `MonthCodeToQuarter` is never called—[[Code Smells Catalog#Dead Code]]).

**Key Insight:** *You cannot refactor what you cannot test.* The first step isn't cleaning code—it's writing tests that exercise the code.

### 2.2 Writing Independent Unit Tests

Uncle Bob writes a brand-new suite (`Listing B-4`) that achieves **170/185 statements (92%)**. Some tests are commented out because they represent *desired* behavior that the code doesn't yet support. As he refactors, he uncomments and makes these pass.

```java
// Before — tests reveal missing behavior
// Commented out because the method is case-sensitive
// testWeekdayCodeToString() expects "Monday" == "monday"

// Fix — two-line change
// Original (line 259, 263):
if (s.equals(shortWeekdayNames[i])) { ... }
if (s.equals(weekDayNames[i])) { ... }

// After:
if (s.equalsIgnoreCase(shortWeekdayNames[i])) { ... }
if (s.equalsIgnoreCase(weekDayNames[i])) { ... }
```

*Lesson:* Trivial fixes are fine when tests reveal them. Don't overthink—just fix and verify.

### 2.3 Bugs Discovered Through Testing

**Bug 1: `getFollowingDayOfWeek` boundary error (line 685)**

```java
// Before — returns Dec 25 as the Saturday following Dec 25 (wrong!)
// Dec 25, 2004 is Saturday. Next Saturday should be Jan 1, 2005.
if (baseDOW >= targetWeekday) {  // BUG: should be >
    ...
}

// After
if (baseDOW > targetWeekday) {   // FIX: boundary condition
    ...
}
```

**Bug 2: `getNearestDayOfWeek` algorithm is simply wrong**

```java
// Before — dead branch at line 719; adjust is always negative,
// so adjust >= 4 is never true. The algorithm fails when the
// nearest day is in the future.
if (adjust >= 4) { ... }  // NEVER executed — dead code

// After — correct algorithm
int delta = targetDOW - base.getDayOfWeek();
int positiveDelta = delta + 7;
int adjust = positiveDelta % 7;
if (adjust > 3)
    adjust -= 7;
return SerialDate.addDays(adjust, base);
```

*Lesson:* Code coverage tools don't just measure quantity—**they reveal dead branches** that are genuine bugs in disguise. A line that never executes is either dead code or a logic error. In this case, it was both.

**Bug 3: Exception handling vs. error strings**

```java
// Before — returning error strings masks failures
public static String weekInMonthToString(int week) {
    switch (week) {
        case 1: return "First";
        // ...
        default: return "SerialDate.weekInMonthToString(): invalid code.";
    }
}

// After — throw an exception the caller can actually handle
public static String weekInMonthToString(int week) {
    switch (week) {
        case 1: return "First";
        // ...
        default: throw new IllegalArgumentException("Invalid week code: " + week);
    }
}
```

*Lesson:* Returning error strings is a silent failure mode. Callers can ignore strings; they cannot ignore exceptions. Fail loudly, fail early. See [[Clean Code Principles#Fail Fast]].

---

## 3. Phase 2 — Make It Right: Systematic Refactoring

With tests passing and coverage high, the real work begins. The approach is **top-to-bottom, one change at a time, running all tests after every single change**. No batch refactoring—you break one thing, you know exactly which change broke it.

### 3.1 Name the Class for What It Is, Not How It Works

**The Problem:** The name `SerialDate` leaks implementation. The class is named after its *serial number* representation (days since Dec 30, 1899). An abstract class should not imply anything about its implementation—it should describe its *abstraction*.

```java
// Before
public abstract class SerialDate implements Comparable, Serializable { ... }

// After — name at the correct level of abstraction
public abstract class DayDate implements Comparable, Serializable { ... }
```

The word "serial" is a clue about *how* dates are stored, not *what* the class represents. DayDate says "I represent a day on the calendar"—nothing more, nothing less.

**Principle:** [[Naming Conventions#Abstraction Level]] — Class names should reveal the abstraction, not the implementation.

---

### 3.2 Replace Constant Inheritance with Enums

**The Problem:** `MonthConstants` (Listing B-3) is a class full of `public static final int` constants. `SerialDate` *inherits* from it—an old Java trick to avoid typing `MonthConstants.January`. This is the **Constant Interface Antipattern** applied to inheritance. It violates [[Class Design & SOLID#Interface Segregation Principle]] by forcing every subclass to "be" a bag of month constants.

```java
// Before — inheriting from a bag of constants
public abstract class SerialDate extends MonthConstants { ... }

// where MonthConstants contains:
public class MonthConstants {
    public static final int JANUARY = 1;
    public static final int FEBRUARY = 2;
    // ...
}
```

```java
// After — a proper enum with behavior
public enum Month {
    JANUARY(1), FEBRUARY(2), MARCH(3), APRIL(4),
    MAY(5), JUNE(6), JULY(7), AUGUST(8),
    SEPTEMBER(9), OCTOBER(10), NOVEMBER(11), DECEMBER(12);

    public final int index;

    Month(int index) { this.index = index; }

    public static Month fromInt(int monthIndex) {
        for (Month m : Month.values())
            if (m.index == monthIndex)
                return m;
        throw new IllegalArgumentException("Invalid month index " + monthIndex);
    }

    public int toInt() { return index; }
}
```

**Immediate payoff:**

- **Eliminates `isValidMonthCode()`** — the type system now guarantees validity.
- **Eliminates error-checking boilerplate** everywhere a month integer was passed.
- **Methods that took `int month` now take `Month month`** — the compiler catches errors, not the developer.

```java
// Before — fragile, error-prone
public static int monthCodeToQuarter(int monthCode) {
    if (monthCode < 1 || monthCode > 12) { ... }  // guard clause
    // ...
}

// After — guard clause eliminated; type system guarantees correctness
public int quarter() {
    return 1 + (index - 1) / 3;
}
```

*Lesson:* Replace primitive obsession with types. When a function takes `int month`, it really wants a `Month`. Let the type system do the validation for you. See [[Code Smells Catalog#Primitive Obsession]].

### 3.3 Same Pattern: Day Enum, WeekInMonth Enum, DateInterval Enum

The pattern repeats for every set of integer constants:

```java
// Before — integer constants for day-of-week
public static final int MONDAY = Calendar.MONDAY;
public static final int TUESDAY = Calendar.TUESDAY;
// ... scattered across the class

// After — Day enum with parsing built in
public enum Day {
    MONDAY(Calendar.MONDAY), TUESDAY(Calendar.TUESDAY),
    WEDNESDAY(Calendar.WEDNESDAY), THURSDAY(Calendar.THURSDAY),
    FRIDAY(Calendar.FRIDAY), SATURDAY(Calendar.SATURDAY),
    SUNDAY(Calendar.SUNDAY);

    public static Day fromInt(int index) { ... }
    public static Day parse(String s) { ... }
    public String toString() { ... }
}
```

**WeekInMonth enum** replaces numeric constants `FIRST=1, SECOND=2, THIRD=3, FOURTH=4, LAST=0`.

**DateInterval enum** replaces cryptic `INCLUDE_NONE, INCLUDE_FIRST, INCLUDE_SECOND, INCLUDE_BOTH` with mathematically precise `OPEN, CLOSED_LEFT, CLOSED_RIGHT, CLOSED`. *Better naming communicates intent without documentation.*

**WeekdayRange enum** replaces `LAST, NEXT, NEAREST` integer flags.

**Why enums matter for refactoring:** The names are now changeable with IDE rename refactoring. You can't accidentally pass `-1` where a month is expected. The compiler will not let you. [[Class Design & SOLID#Make Invalid States Unrepresentable]].

### 3.4 Eliminate Inheritance Knowledge: The DayDateFactory

**The Problem:** `DayDate` (the abstract base class) contains constants like `MINIMUM_YEAR_SUPPORTED` and `MAXIMUM_YEAR_SUPPORTED` that are implementation-specific. Even worse, the code in `RelativeDayOfWeekRule` needs these values—but an abstract class shouldn't expose implementation details. This is a [[Code Smells Catalog#Inappropriate Intimacy]] between base and derived classes.

**The Pattern:** Abstract Factory + Singleton + Static Delegation

```java
// Before — base class knows about implementation limits
public abstract class DayDate {
    public static final int MINIMUM_YEAR_SUPPORTED = 1900;
    public static final int MAXIMUM_YEAR_SUPPORTED = 9999;
    // ... these belong in SpreadsheetDate, not here
}

// After — factory encapsulates implementation knowledge
public abstract class DayDateFactory {
    private static DayDateFactory factory = new SpreadsheetDateFactory();

    public static void setInstance(DayDateFactory factory) {
        DayDateFactory.factory = factory;
    }

    // Abstract methods — each implementation provides its own
    protected abstract DayDate _makeDate(int ordinal);
    protected abstract DayDate _makeDate(int day, DayDate.Month month, int year);
    protected abstract int _getMinimumYear();
    protected abstract int _getMaximumYear();

    // Public static API — delegates to the current factory
    public static DayDate makeDate(int ordinal) {
        return factory._makeDate(ordinal);
    }
    public static int getMinimumYear() {
        return factory._getMinimumYear();
    }
    public static int getMaximumYear() {
        return factory._getMaximumYear();
    }
}
```

```java
// SpreadsheetDateFactory provides the concrete implementation
public class SpreadsheetDateFactory extends DayDateFactory {
    public DayDate _makeDate(int ordinal) {
        return new SpreadsheetDate(ordinal);
    }
    protected int _getMinimumYear() {
        return SpreadsheetDate.MINIMUM_YEAR_SUPPORTED;
    }
    protected int _getMaximumYear() {
        return SpreadsheetDate.MAXIMUM_YEAR_SUPPORTED;
    }
}
```

**Also note the naming improvement:** `createInstance()` becomes `makeDate()`. "Make" is a common factory prefix that signals object creation. See [[Naming Conventions#Method Names]].

### 3.5 Move Methods to Where They Belong

A recurring theme: methods live in the wrong classes. Uncle Bob systematically relocates them.

| Method | Was In | Moved To | Reason |
|--------|--------|----------|--------|
| `stringToWeekdayCode` | DayDate | `Day` enum | It's the parse function for Day—belongs with the type |
| `weekdayCodeToString` | DayDate | `Day` enum (as `toString()`) | Belongs with the type |
| `monthCodeToQuarter` | DayDate | `Month` enum (as `quarter()`) | Feature envy—asks Month data, should be on Month |
| `monthCodeToString` | DayDate | `Month` enum (as `toString()`) | Belongs with the type |
| `stringToMonthCode` | DayDate | `Month` enum (as `parse()`) | Belongs with the type |
| `getMonthNames` | DayDate | `DateUtil` | Utility function, not core to date abstraction |
| `isLeapYear` | DayDate | `DateUtil` | Utility function |
| `lastDayOfMonth` | DayDate | `DateUtil` | Utility function |
| `leapYearCount` | DayDate | `SpreadsheetDate` | Only used by the derived class |

**The refactoring for `monthCodeToString` → `Month.toString()` + `Month.toShortString()`:**

```java
// Before — twin methods with a boolean flag (code smell: flag argument)
public static String monthCodeToString(int month) {
    return monthCodeToString(month, false);
}
public static String monthCodeToString(int month, boolean shortened) {
    // ... complex switch or array lookup with shortened flag
}

// After — two clear, single-purpose methods on the enum
public enum Month {
    // ...
    public String toString() {
        return dateFormatSymbols.getMonths()[index - 1];
    }
    public String toShortString() {
        return dateFormatSymbols.getShortMonths()[index - 1];
    }
}
```

*Lesson:* [[Code Smells Catalog#Feature Envy]] — when a method uses more data from another class than its own, move it. Flag arguments are also a smell; prefer separate methods with clear names.

### 3.6 Push Down Implementation Details; Pull Up Generic Behavior

Two complementary forces in inheritance refactoring:

**Push Down** (move to derived class):
- `EARLIEST_DATE_ORDINAL` / `LATEST_DATE_ORDINAL` → `SpreadsheetDate` (only used there)
- `LEAP_YEAR_AGGREGATE_DAYS_TO_END_OF_MONTH` → `SpreadsheetDate`
- `AGGREGATE_DAYS_TO_END_OF_PRECEDING_MONTH` → `SpreadsheetDate`
- `leapYearCount()` → `SpreadsheetDate`
- `MINIMUM_YEAR_SUPPORTED` / `MAXIMUM_YEAR_SUPPORTED` → `SpreadsheetDate`

**Pull Up** (move to abstract base class):
- `toDate()` — implementation doesn't depend on SpreadsheetDate internals
- `compare()` — renamed to `daysSince()`, implementation is generic
- `getDayOfWeek()` — after extracting one abstract hook (`getDayOfWeekForOrdinalZero()`)
- Six more abstract methods that had generic implementations in SpreadsheetDate

**The `getDayOfWeek` trap — logical vs. physical dependency:**

```java
// The implementation in SpreadsheetDate "works" generically—
// but it implicitly depends on the origin day (day 0 = Saturday).
// Making the dependency explicit:

// Abstract hook in DayDate
protected abstract Day getDayOfWeekForOrdinalZero();

// Generic algorithm in DayDate
public Day getDayOfWeek() {
    Day startingDay = getDayOfWeekForOrdinalZero();
    int startingOffset = startingDay.index - Day.SUNDAY.index;
    return Day.fromInt((getOrdinalDay() + startingOffset) % 7 + 1);
}

// Concrete hook in SpreadsheetDate
protected Day getDayOfWeekForOrdinalZero() {
    return Day.SATURDAY;
}
```

*Lesson:* If a method has a *logical* dependency on the implementation, make it a *physical* dependency too. Extract the implementation-specific part into an abstract method. See [[Class Design & SOLID#Template Method Pattern]].

### 3.7 Static → Instance Methods: The Mutability Contract

Several key methods were `static` but should be instance methods because they operate on the state of a `DayDate`. But this creates a naming hazard:

```java
// DANGEROUS: Looks like mutation but returns a new instance
date.addDays(7);  // Am I mutating date? Or getting a new one?

// CLEAR: plusDays signals immutability
DayDate newDate = date.plusDays(7);  // Obvious: returns new instance
```

```java
// Before — static, uses instance data through parameter
public static DayDate addDays(int days, DayDate base) {
    return createInstance(base.toSerial() + days);
}

// After — instance method, clear immutability contract
public DayDate plusDays(int days) {
    return DayDateFactory.makeDate(toOrdinal() + days);
}
```

**Same transformation for `addMonths` → `plusMonths`**, with explaining variables:

```java
// Before — dense, hard to follow
public static DayDate addMonths(int months, DayDate base) {
    int yy = (12 * base.getYYYY() + base.getMonth() + months - 1) / 12;
    int mm = (12 * base.getYYYY() + base.getMonth() + months - 1) % 12 + 1;
    int dd = Math.min(base.getDayOfMonth(),
        lastDayOfMonth(mm, yy));
    return createInstance(dd, mm, yy);
}

// After — each step named, algorithm transparent
public DayDate plusMonths(int months) {
    int thisMonthAsOrdinal = 12 * getYear() + getMonth().index - 1;
    int resultMonthAsOrdinal = thisMonthAsOrdinal + months;
    int resultYear = resultMonthAsOrdinal / 12;
    Month resultMonth = Month.fromInt(resultMonthAsOrdinal % 12 + 1);
    int lastDayOfResultMonth = DateUtil.lastDayOfMonth(resultMonth, resultYear);
    int resultDay = Math.min(getDayOfMonth(), lastDayOfResultMonth);
    return DayDateFactory.makeDate(resultDay, resultMonth, resultYear);
}
```

**Explaining Temporary Variables** are a refactoring technique: give intermediate results names that explain *why* they exist, not just *what* they hold. `thisMonthAsOrdinal` tells you "we're flattening the month into a linear scale." The name is the documentation.

See [[Function Design#Explaining Variables]].

### 3.8 Simplify Algorithms: Day-of-Week Methods

The three day-of-week navigation methods (`getPreviousDayOfWeek`, `getFollowingDayOfWeek`, `getNearestDayOfWeek`) were overly complex. After fixing the bugs in Phase 1, Uncle Bob simplifies them to be consistent and expressive:

```java
// Before — getPreviousDayOfWeek (lines 628-660), complex and long

// After — 4 lines, self-documenting
public DayDate getPreviousDayOfWeek(Day targetDayOfWeek) {
    int offsetToTarget = targetDayOfWeek.index - getDayOfWeek().index;
    if (offsetToTarget >= 0)
        offsetToTarget -= 7;
    return plusDays(offsetToTarget);
}

public DayDate getFollowingDayOfWeek(Day targetDayOfWeek) {
    int offsetToTarget = targetDayOfWeek.index - getDayOfWeek().index;
    if (offsetToTarget <= 0)
        offsetToTarget += 7;
    return plusDays(offsetToTarget);
}

public DayDate getNearestDayOfWeek(Day targetDay) {
    int offsetToThisWeeksTarget = targetDay.index - getDayOfWeek().index;
    int offsetToFutureTarget = (offsetToThisWeeksTarget + 7) % 7;
    int offsetToPreviousTarget = offsetToFutureTarget - 7;
    if (offsetToFutureTarget > 3)
        return plusDays(offsetToPreviousTarget);
    else
        return plusDays(offsetToFutureTarget);
}
```

*Lesson:* Algorithm clarity matters more than cleverness. The three methods now share a consistent pattern (compute offset, adjust, return `plusDays`). Consistency reduces cognitive load. [[Clean Code Principles#Consistency]].

### 3.9 Replacing Switch Statements with Polymorphism

`isInRange()` contained a switch on interval type. Instead, each enum constant provides its own implementation:

```java
// Before — switch in the method
public boolean isInRange(DayDate d1, DayDate d2, int include) {
    // ...
    switch (include) {
        case INCLUDE_NONE: return d > left && d < right;
        case INCLUDE_FIRST: return d >= left && d < right;
        case INCLUDE_SECOND: return d > left && d <= right;
        case INCLUDE_BOTH: return d >= left && d <= right;
    }
}

// After — polymorphic enum
public enum DateInterval {
    OPEN {
        public boolean isIn(int d, int left, int right) {
            return d > left && d < right;
        }
    },
    CLOSED_LEFT {
        public boolean isIn(int d, int left, int right) {
            return d >= left && d < right;
        }
    },
    CLOSED_RIGHT {
        public boolean isIn(int d, int left, int right) {
            return d > left && d <= right;
        }
    },
    CLOSED {
        public boolean isIn(int d, int left, int right) {
            return d >= left && d <= right;
        }
    };

    public abstract boolean isIn(int d, int left, int right);
}

public boolean isInRange(DayDate d1, DayDate d2, DateInterval interval) {
    int left = Math.min(d1.getOrdinalDay(), d2.getOrdinalDay());
    int right = Math.max(d1.getOrdinalDay(), d2.getOrdinalDay());
    return interval.isIn(getOrdinalDay(), left, right);
}
```

*Lesson:* Every switch on a type code is a missed opportunity for polymorphism. Replace with polymorphic dispatch when the branches represent distinct behaviors of distinct types. [[Code Smells Catalog#Switch Statements]].

### 3.10 Remove Dead Code, Redundant Comments, and Clutter

Throughout the refactoring, Uncle Bob deletes:

| Deletion | Reason |
|----------|--------|
| Change history comments (lines 1–60) | Source control tracks this now — [[Code Smells Catalog#Obsolete Comment]] |
| Javadoc on `stringToWeekdayCode` | Became wrong after switching to enum; signature says enough |
| `final` keywords on locals and params | Adds clutter, no real safety benefit when you have unit tests |
| `AGGREGATE_DAYS_TO_END_OF_MONTH` table | Never used anywhere in JCommon |
| `LEAP_YEAR_AGGREGATE_DAYS_TO_END_OF_MONTH` table | Also unused |
| `description` field + accessor/mutator | Never used |
| Default constructor (line 213) | Compiler generates it |
| `isValidMonthCode()` | Type system guarantees validity now |
| `weekInMonthToString()` + tests | Nobody called it except tests—deleted tests too |
| `relativeToString()` + tests | Same—only test callers |
| `serialVersionUID` | Prefer automatic control; `InvalidClassException` is better than silent corruption |
| Redundant Javadoc | "Redundant comments are just places to collect lies and misinformation" |

**The `final` debate:** "Eliminating `final` flies in the face of some conventional wisdom … I think that there are a few good uses for `final`, such as the occasional `final` constant, but otherwise the keyword adds little value and creates a lot of clutter. Perhaps I feel this way because the kinds of errors that `final` might catch are already caught by the unit tests I write."

### 3.11 The Deleted `weekInMonthToString` — A Cautionary Tale

Uncle Bob performed an elegant chain of refactorings:
1. Move method to `WeekInMonth` enum → rename to `toString()` → change from static to instance → delete the method entirely → change tests to use enum names directly.

**Then he realized:** the only callers were the tests he just modified. The function was dead code all along—he had refactored and tested something nobody used. He deleted both function and tests.

> *"Fool me once, shame on you. Fool me twice, shame on me!"*

*Lesson:* Before investing in refactoring a method, check if anything actually calls it. Dead code isn't worth polishing—it's worth deleting. [[Code Smells Catalog#Dead Code]].

---

## 4. Before/After Summary: Key Transformations

### Class Structure

```
BEFORE                                    AFTER
======                                    =====
SerialDate (abstract)                     DayDate (abstract)
  extends MonthConstants                    implements Comparable, Serializable
  constants: MONDAY..SUNDAY               DayDateFactory (abstract factory)
  constants: JANUARY..DECEMBER            SpreadsheetDateFactory
  tables: LAST_DAY_OF_MONTH, etc.         Month (enum, own file)
  methods scattered everywhere            Day (enum, own file)
  static methods operating on instances   WeekInMonth (enum, own file)
                                           DateInterval (enum, own file)
                                           WeekdayRange (enum, own file)
                                           DateUtil (utility class)
```

### Method Organization

| Concern | Before Location | After Location |
|---------|----------------|----------------|
| Month parsing/formatting | DayDate static methods | `Month` enum |
| Day parsing/formatting | DayDate static methods | `Day` enum |
| Leap year calculation | DayDate static | `DateUtil` static |
| Factory creation | `createInstance()` on DayDate | `DayDateFactory.makeDate()` |
| Implementation limits | DayDate constants | `SpreadsheetDate` + factory |
| Day-of-week navigation | Complex static methods | Simple instance methods on DayDate |

### Naming Improvements

| Before | After | Why |
|--------|-------|-----|
| `SerialDate` | `DayDate` | Abstraction, not implementation |
| `toSerial()` | `toOrdinal()` → `getOrdinalDay()` | Accurate term + JavaBean convention |
| `getYYYY()` | `getYear()` | No need for four Y's |
| `createInstance()` | `makeDate()` | "make" is a factory verb |
| `addDays()` | `plusDays()` | Signals immutability |
| `addMonths()` | `plusMonths()` | Same |
| `compare()` | `daysSince()` | Tells you what it returns |
| `Month.make()` | `Month.fromInt()` | "from" is a conversion convention |
| `INCLUDE_NONE/FIRST/SECOND/BOTH` | `OPEN/CLOSED_LEFT/CLOSED_RIGHT/CLOSED` | Mathematical precision |

---

## 5. Refactoring Lessons — The Checklist

### Mindset
- [ ] **Professional review is normal.** Critique code like doctors review cases—it's how we learn.
- [ ] **First make it work, then make it right.** Never refactor without test coverage.
- [ ] **Run tests after every single change.** One change, one test run. You break it, you know why.
- [ ] **The Boy Scout Rule:** Leave the code cleaner than you found it. Every edit is an opportunity.

### Code Smells Addressed
- [ ] **Inheritance from constants** → Replace with enums
- [ ] **Primitive obsession** (`int month`, `int day`) → Replace with typed enums
- [ ] **Feature envy** → Move method to the class whose data it uses most
- [ ] **Flag arguments** → Split into separate methods
- [ ] **Base class knowing about derivatives** → Abstract Factory pattern
- [ ] **Dead code** → Delete it; don't refactor it
- [ ] **Redundant comments** → Delete them; they'll only lie later
- [ ] **Switch on type code** → Replace with polymorphic dispatch
- [ ] **Static methods on instance data** → Convert to instance methods
- [ ] **Implied mutability** → Name methods to clarify immutability (`plus`, not `add`)
- [ ] **Logical dependency without physical dependency** → Extract abstract hook method
- [ ] **Error strings as return values** → Throw exceptions instead

### Design Patterns Applied
- [ ] **Enum with behavior** — Replaces constant classes + utility methods
- [ ] **Abstract Factory** — `DayDateFactory` hides which concrete implementation is used
- [ ] **Singleton** — Default factory instance
- [ ] **Template Method** — `getDayOfWeek()` with `getDayOfWeekForOrdinalZero()` hook
- [ ] **Strategy/Polymorphic Enum** — `DateInterval.isIn()` replaces switch statement

---

## 6. Final Metrics

| Metric | Before | After |
|--------|--------|-------|
| Executable statements | 185 | 53 |
| Test coverage | ~50% (91/185) | ~85% (45/53) |
| Files | 1 monolithic class | 7+ focused files |
| Bugs found | 0 known | 3+ fixed |
| Dead code | Extensive | Removed |
| Class hierarchy | Leaks implementation | Clean abstraction |

The coverage percentage *decreased* slightly (92% → 85%) but this is because the class shrank so dramatically that the few uncovered trivial lines now carry more weight. The *quality* of coverage is far higher.

---

## References

- [[Clean Code Principles]]
- [[Function Design]]
- [[Naming Conventions]]
- [[Class Design & SOLID]]
- [[Code Smells Catalog]]
- [[Unit Testing]]
- Gamma et al., *Design Patterns: Elements of Reusable Object Oriented Software*, 1996.
- Fowler et al., *Refactoring: Improving the Design of Existing Code*, 1999.
- Beck, *Smalltalk Best Practice Patterns*, 1997.
