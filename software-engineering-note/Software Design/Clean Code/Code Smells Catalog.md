---
tags:
- clean-code
- software-design
- software-engineering
---

# Code Smells Catalog

> *"Clean code is not written by following a set of rules. Professionalism and craftsmanship come from values that drive disciplines."*
> — Robert C. Martin, *Clean Code*, Chapter 17 (pp. 285–314)

A quick-reference catalog of all 66 heuristics and code smells from the capstone chapter. Each entry includes the reference code, a one-line summary, and the key insight. For deeper treatment of topics covered in earlier chapters, follow the [[#See Also|wikilinks]].

---

## Comments

*See also: [[Comment Patterns]]*

#### **C1** — **Inappropriate Information**
Comments should hold technical notes about code and design—not metadata better kept in source control, issue trackers, or other record-keeping systems. Change histories, authors, and SPR numbers in comments become clutter.

#### **C2** — **Obsolete Comment**
Comments age quickly. An outdated, incorrect comment becomes a floating island of misdirection. Update or delete obsolete comments as soon as you find them.

#### **C3** — **Redundant Comment**
A comment that restates what the code already says is noise. `i++; // increment i` adds nothing. Javadoc that merely echoes the function signature is equally useless. Comments should say what code *cannot* say for itself.

#### **C4** — **Poorly Written Comment**
If a comment is worth writing, it's worth writing well. Use correct grammar, be brief, don't ramble, and don't state the obvious.

#### **C5** — **Commented-Out Code**
> *"Commented-out code is an abomination."*

It rots, calls functions that no longer exist, and pollutes modules. Delete it—source control remembers it.

---

## Environment

#### **E1** — **Build Requires More Than One Step**
You should be able to check out the system with one command and build it with one command. No arcane scripts, no hunting for extra JARs or XML files. `svn get mySystem && ant all`—that's the ideal.

#### **E2** — **Tests Require More Than One Step**
All unit tests should run with a single command (or one IDE button click). If running tests isn't trivially easy, they won't be run.

---

## Functions

*See also: [[Function Design]]*

#### **F1** — **Too Many Arguments**
Zero arguments is ideal; one is good; two is acceptable; three is questionable. More than three should be avoided with prejudice. Related: [[Function Design#Function Arguments]].

#### **F2** — **Output Arguments**
Readers expect arguments to be inputs, not outputs. If your function must change state, change the state of the object it's called on—don't mutate a parameter. Related: [[Function Design#Output Arguments]].

#### **F3** — **Flag Arguments**
A boolean argument loudly declares the function does *more than one thing*. Split into separate functions: `straightPay()` and `overTimePay()` instead of `calculateWeeklyPay(false)`. Related: [[Function Design#Flag Arguments]].

#### **F4** — **Dead Function**
Methods never called should be discarded. Fear of deletion is irrational—your source control system remembers them.

---

## General

*The largest category—36 heuristics covering day-to-day craftsmanship. See also: [[Clean Code Principles]], [[Class Design & SOLID]], [[Objects vs Data Structures]].*

#### **G1** — **Multiple Languages in One Source File**
A single source file mixing Java, XML, HTML, JavaScript, English, YAML, etc. is confusing at best, sloppy at worst. Minimize the number and extent of extra languages in each file.

#### **G2** — **Obvious Behavior Is Unimplemented**
Follow the *Principle of Least Surprise*. If a function is called `StringToDay("Monday")`, readers expect it to handle abbreviations and case-insensitivity. When obvious behavior is missing, readers lose trust and must read implementation details.

#### **G3** — **Incorrect Behavior at the Boundaries**
Don't trust intuition about correctness. Every boundary condition, corner case, and quirk can confound even elegant algorithms. Write tests for every boundary.

#### **G4** — **Overridden Safeties** *(Chernobyl)*
Disabling compiler warnings, turning off failing tests, or manually controlling `serialVersionUID` is risky. Safeties exist for a reason—overriding them to "get the build to succeed" trades convenience for disaster.

#### **G5** — **Duplication** *(DRY)*
> *"Every time you see duplication in the code, it represents a missed opportunity for abstraction."*

The *most important rule in the book*. DRY (Don't Repeat Yourself), "Once and Only Once." Duplication appears in many forms:
- **Cloned code blocks** → extract into methods
- **Repeated `switch/case` or `if/else` chains** → replace with polymorphism (see [[Class Design & SOLID]])
- **Similar algorithms with different code** → TEMPLATE METHOD or STRATEGY pattern
- **Database schema duplication** → Codd Normal Forms

Most design patterns are simply well-known ways to eliminate duplication.

#### **G6** — **Code at Wrong Level of Abstraction**
Higher-level general concepts and lower-level detailed concepts must be fully separated. A `Stack` interface shouldn't have `percentFull()`—that belongs in a `BoundedStack` derivative. You cannot fake your way out of a misplaced abstraction.

```java
// Wrong: percentFull() doesn't belong on every Stack
public interface Stack {
    Object pop() throws EmptyException;
    void push(Object o) throws FullException;
    double percentFull();  // belongs on BoundedStack
}
```

#### **G7** — **Base Classes Depending on Their Derivatives**
Base classes should know nothing about their derivatives. When a base class mentions derivative names, deployment becomes coupled—changing a derivative forces redeploying the base. See also: [[Class Design & SOLID]].

#### **G8** — **Too Much Information**
Well-defined modules have *small interfaces*. Hide data, utility functions, constants, temporaries. The fewer methods and instance variables a class exposes, the lower the coupling. Keep interfaces tight.

#### **G9** — **Dead Code**
Code that never executes: unreachable `if` branches, `catch` blocks that never catch, utility methods never called. It still compiles but doesn't follow newer conventions. Delete it.

#### **G10** — **Vertical Separation**
Variables and functions should be defined *close* to where they're used. Declare locals just above first use. Define private functions just below their first invocation—finding them should be a matter of scanning downward.

#### **G11** — **Inconsistency**
If you use `response` for `HttpServletResponse` in one function, use it everywhere. If you name one method `processVerificationRequest`, name the next `processDeletionRequest`. Consistent patterns make code predictable and readable.

#### **G12** — **Clutter**
Default constructors with no implementation, unused variables, dead functions, comment noise—all clutter. Keep source files clean and well-organized.

#### **G13** — **Artificial Coupling**
Don't put a general-purpose enum inside a specific class just because it's convenient. Things that don't depend on each other shouldn't be coupled. Take the time to find the *right* home for every declaration.

#### **G14** — **Feature Envy** *(Fowler)*
A method that uses another class's accessors/mutators to manipulate that class's data "envies" the other class's scope. The method wishes it lived there. Usually the fix is to move the method to the envied class—but sometimes Feature Envy is necessary to avoid coupling (e.g., report formatting shouldn't live inside the domain object).

```java
// Feature Envy: calculateWeeklyPay reaches into HourlyEmployee to get data
public Money calculateWeeklyPay(HourlyEmployee e) {
    int tenthRate = e.getTenthRate().getPennies();
    int tenthsWorked = e.getTenthsWorked();
    // ... manipulates e's data extensively
}
```

#### **G15** — **Selector Arguments**
`calculateWeeklyPay(false)`—what does `false` mean? A selector argument (boolean, enum, int) chooses between behaviors. Split into separate functions instead. Many small functions beat one function with a behavior-selector argument.

```java
// Bad: what does "false" mean?
calculateWeeklyPay(false);

// Good: explicit purpose
straightPay();
overTimePay();
```

#### **G16** — **Obscured Intent**
Run-on expressions, Hungarian notation, magic numbers—all hide what the code is trying to do. Code should be expressive. Take the time to make intent visible.

#### **G17** — **Misplaced Responsibility**
Place code where readers naturally expect to find it. `PI` belongs with trig functions. `OVERTIME_RATE` belongs in `HourlyPayCalculator`. Use function names as guides: `getTotalHours` implies summation, `saveTimeCard` does not. Related: [[Clean Code Principles#The Principle of Least Surprise]].

#### **G18** — **Inappropriate Static**
Prefer non-static methods to static methods. If there's *any* chance you'll want polymorphic behavior, don't make it static. `Math.max(a, b)` is fine as static; `calculatePay(employee, rate)` probably isn't—you might want `OvertimeHourlyPayCalculator` later. See also: [[Objects vs Data Structures]].

#### **G19** — **Use Explanatory Variables**
Break calculations into well-named intermediate values. This is one of the most powerful readability techniques—opaque modules become transparent.

```java
Matcher match = headerPattern.matcher(line);
if (match.find()) {
    String key = match.group(1);    // not just "group 1"
    String value = match.group(2);  // not just "group 2"
    headers.put(key.toLowerCase(), value);
}
```

> *"It is remarkable how an opaque module can suddenly become transparent simply by breaking the calculations up into well-named intermediate values."*

#### **G20** — **Function Names Should Say What They Do**
`date.add(5)`—adds 5 *what*? Days? Weeks? Does it mutate or return a new instance? Use `addDaysTo` vs `daysLater` to make mutation clear. If you must read the implementation to understand the name, find a better name.

#### **G21** — **Understand the Algorithm**
>"There is a difference between knowing how the code works and knowing whether the algorithm will do the job. Being unsure that an algorithm is appropriate is often a fact of life. Being unsure what your code does is just laziness."

Passing tests isn't enough—you must *know* the solution is correct. The best way to gain this understanding is to refactor until it's *obvious* that it works.

#### **G22** — **Make Logical Dependencies Physical**
If module A depends on module B, that dependency should be *explicit*. Don't have `HourlyReporter` assume the page size is 55—ask `HourlyReportFormatter` via `getMaxPageSize()`. Logical assumptions rot; physical dependencies are visible and testable.

#### **G23** — **Prefer Polymorphism to If/Else or Switch/Case**
The **"ONE SWITCH" rule:** There may be at most *one* `switch` statement for a given type of selection, and its cases must create polymorphic objects that eliminate all other `switch` statements in the system. Most `switch` usage is brute-force, not thoughtful design. See also: [[Objects vs Data Structures]].

#### **G24** — **Follow Standard Conventions**
Every team follows a coding standard. It doesn't matter *where* you put your braces—as long as everyone agrees. The code itself should serve as the example document. See also: [[Formatting Style]].

#### **G25** — **Replace Magic Numbers with Named Constants**
`86400` → `SECONDS_PER_DAY`. But some constants are so well-known (5280 feet/mile, 8 work hours) that naming them adds noise. The rule applies to *any* non-self-describing token, including string literals like `"John Doe"` → `HOURLY_EMPLOYEE_NAME`.

#### **G26** — **Be Precise**
- Expecting the *only* match from a query? Check for duplicates anyway.
- Using floats for currency? Use integers (or a `Money` class).
- Declaring `ArrayList` when `List` suffices? Overly constraining.
- Calling a function that might return `null`? Check for `null`.
- Possibility of concurrent update? Implement locking.

Ambiguity and imprecision are either laziness or disagreement. Eliminate both.

#### **G27** — **Structure over Convention**
Naming conventions are good; structural enforcement is better. Switch/case with nicely named enums is inferior to base classes with abstract methods—the compiler forces implementation of all abstract methods, but nobody forces consistent switch/case.

#### **G28** — **Encapsulate Conditionals**
Extract boolean logic into intention-revealing functions. `if (shouldBeDeleted(timer))` beats `if (timer.hasExpired() && !timer.isRecurrent())`. See also: [[Function Design#Do One Thing]].

#### **G29** — **Avoid Negative Conditionals**
Negatives are cognitively harder than positives. Prefer `if (buffer.shouldCompact())` over `if (!buffer.shouldNotCompact())`.

#### **G30** — **Functions Should Do One Thing**
Functions that loop, check conditions, *and* perform actions are doing multiple things. Extract until each function does exactly one thing. See also: [[Function Design#Do One Thing]].

```java
// Before: pay() loops, checks, AND pays
public void pay() {
    for (Employee e : employees) {
        if (e.isPayday()) {
            Money pay = e.calculatePay();
            e.deliverPay(pay);
        }
    }
}

// After: each function does one thing
public void pay() {
    for (Employee e : employees)
        payIfNecessary(e);
}
```

#### **G31** — **Hidden Temporal Couplings**
If `saturateGradient()` must be called before `reticulateSplines()`, don't hide that dependency. Use a **bucket brigade**: each function produces the argument the next function needs, making the order physically impossible to violate.

```java
// Hidden temporal coupling
public void dive(String reason) {
    saturateGradient();
    reticulateSplines();      // must come after saturateGradient
    diveForMoog(reason);
}

// Physicalized: each step feeds the next
public void dive(String reason) {
    Gradient gradient = saturateGradient();
    List<Spline> splines = reticulateSplines(gradient);
    diveForMoog(splines, reason);
}
```

#### **G32** — **Don't Be Arbitrary**
Every structural decision should have a reason *communicated by the structure itself*. If a public inner class doesn't need to be scoped inside another class, make it a top-level class. Arbitrary structure invites others to change it.

#### **G33** — **Encapsulate Boundary Conditions**
Boundary conditions (`+1`, `-1`, `< length`) are hard to track. Give them names and keep them in one place. `int nextLevel = level + 1` is clearer than repeating `level + 1` throughout. Don't let swarms of ±1 scatter across the code.

#### **G34** — **Functions Should Descend Only One Level of Abstraction**
The hardest heuristic to follow well. All statements in a function should be at *one* level below the function's name. Mixing high-level concepts ("construct an HR tag") with low-level details (`html.append(" size=\"")`) is the norm, but it shouldn't be. See also: [[Function Design#One Level of Abstraction per Function]].

#### **G35** — **Keep Configurable Data at High Levels**
Default values and configuration constants should live at high levels of abstraction—exposed as arguments to low-level functions, not buried inside them. If a default port is 80, declare it in `Arguments`, not in a low-level `if (port == 0)` check.

#### **G36** — **Avoid Transitive Navigation** *(Law of Demeter)*
`a.getB().getC().doSomething()`—modules should know only their *immediate* collaborators. If you later need to insert `Q` between `B` and `C`, every chain like this breaks. A module should simply say `myCollaborator.doSomething()`. See also: [[Boundaries & Dependencies]].

---

## Java

#### **J1** — **Avoid Long Import Lists by Using Wildcards**
If you use two or more classes from a package, use `import package.*;`. Wildcard imports are not true dependencies—they just add the package to the search path. Modern IDEs can expand them when needed.

#### **J2** — **Don't Inherit Constants**
> *"This is a hideous practice!"*

Putting constants in an interface and inheriting that interface to access them (`class Employee implements PayrollConstants`) cheats the language's scoping rules. Use `import static PayrollConstants.*` instead.

#### **J3** — **Constants vs Enums**
Use Java enums, not `public static final int`. Enums belong to a named enumeration, can have methods and fields, and provide far more expressiveness. Study enum syntax deeply—they're powerful tools.

```java
public enum HourlyPayGrade {
    APPRENTICE { public double rate() { return 1.0; } },
    JOURNEYMAN { public double rate() { return 1.5; } },
    MASTER     { public double rate() { return 2.0; } };
    public abstract double rate();
}
```

---

## Names

*See also: [[Naming Conventions]]*

#### **N1** — **Choose Descriptive Names**
Names are 90% of software readability. Take time to choose them wisely and reevaluate as software evolves. Well-chosen names *overload* the code's structure with description—readers can infer what other functions do just from the names.

```java
// Before: opaque
public int x() {
    int q = 0; int z = 0;
    for (int kk = 0; kk < 10; kk++) {
        if (l[z] == 10) { q += 10 + (l[z+1] + l[z+2]); z += 1; }
        // ...
    }
    return q;
}

// After: self-documenting
public int score() {
    int score = 0; int frame = 0;
    for (int frameNumber = 0; frameNumber < 10; frameNumber++) {
        if (isStrike(frame)) { score += 10 + nextTwoBallsForStrike(frame); frame += 1; }
        else if (isSpare(frame)) { score += 10 + nextBallForSpare(frame); frame += 2; }
        else { score += twoBallsInFrame(frame); frame += 2; }
    }
    return score;
}
```

#### **N2** — **Choose Names at the Appropriate Level of Abstraction**
Don't let implementation details leak into names. `dial(phoneNumber)` is wrong for a cable modem that's always connected. Use `connect(connectionLocator)`—the name works for phone numbers, USB ports, or any future connection strategy.

#### **N3** — **Use Standard Nomenclature Where Possible**
Use pattern names (`Decorator`), language conventions (`toString`), and team *ubiquitous language* (Evans' DDD term). The more a name is overloaded with relevant project meaning, the easier code is to understand.

#### **N4** — **Unambiguous Names**
`doRename()` is vague, especially when it calls `renamePage()` inside. What's the difference? `renamePageAndOptionallyAllReferences` is long, but it's called from one place—the explanatory value outweighs the length.

#### **N5** — **Use Long Names for Long Scopes**
Variable names like `i` are fine for a 5-line loop. But the longer the scope, the longer and more descriptive the name should be. A field used across a 500-line class needs a rich name; a loop counter does not.

#### **N6** — **Avoid Encodings**
No Hungarian notation. No `m_` or `f` prefixes. No `vis_` subsystem encodings. Modern IDEs provide type and scope information without mangling names.

#### **N7** — **Names Should Describe Side-Effects**
If `getOos()` also *creates* the `ObjectOutputStream` if null, the name lies by omission. Rename to `createOrReturnOos`. Don't use a simple verb for a function that does more than that verb suggests.

---

## Tests

*See also: [[Unit Testing]]*

#### **T1** — **Insufficient Tests**
A test suite should test *everything that could possibly break*. "That seems like enough" is the wrong metric. Tests are insufficient as long as untested conditions or unvalidated calculations remain.

#### **T2** — **Use a Coverage Tool!**
Coverage tools reveal gaps in testing strategy. They visually mark uncovered lines (red) and covered lines (green), making it trivial to find `if` or `catch` bodies never executed by any test.

#### **T3** — **Don't Skip Trivial Tests**
Trivial tests are easy to write and their *documentary value* exceeds their production cost. A test is documentation that verifies itself.

#### **T4** — **An Ignored Test Is a Question about an Ambiguity**
When requirements are unclear, express the question as a test—either commented out or annotated `@Ignore`. The test captures the ambiguity and the current assumption.

#### **T5** — **Test Boundary Conditions**
We often get the middle of an algorithm right but misjudge the boundaries. Take special care to test edge cases.

#### **T6** — **Exhaustively Test Near Bugs**
Bugs tend to congregate. When you find one, exhaustively test that function—you'll probably find more. The first bug is rarely alone.

#### **T7** — **Patterns of Failure Are Revealing**
Complete, well-ordered test suites expose failure patterns. If *every* test with input >5 characters fails, or every test passing a negative number to the second argument fails—the pattern itself can spark the diagnosis.

#### **T8** — **Test Coverage Patterns Can Be Revealing**
Looking at which code *is* or *isn't* executed by passing tests provides clues about why failing tests fail.

#### **T9** — **Tests Should Be Fast**
> *"A slow test is a test that won't get run."*

When deadlines tighten, slow tests are the first to be dropped. Do whatever it takes to keep tests fast.

---

## Quick-Reference Checklist

| Code | Smell | One-Word Fix |
|------|-------|-------------|
| C1 | Inappropriate comment info | Delete |
| C2 | Obsolete comment | Update/Delete |
| C3 | Redundant comment | Delete |
| C4 | Poorly written comment | Rewrite |
| C5 | Commented-out code | Delete |
| E1 | Build needs multiple steps | Automate |
| E2 | Tests need multiple steps | Single command |
| F1 | Too many arguments | Reduce/encapsulate |
| F2 | Output arguments | Return, don't mutate |
| F3 | Flag arguments | Split functions |
| F4 | Dead function | Delete |
| G1 | Multiple languages per file | Separate |
| G2 | Obvious behavior missing | Implement it |
| G3 | Incorrect at boundaries | Boundary tests |
| G4 | Overridden safeties | Restore safeties |
| G5 | Duplication | **Abstract it** |
| G6 | Wrong abstraction level | Move up/down |
| G7 | Base depends on derivative | Decouple |
| G8 | Too much information | Hide internals |
| G9 | Dead code | Delete |
| G10 | Vertical separation | Move closer |
| G11 | Inconsistency | Standardize |
| G12 | Clutter | Remove |
| G13 | Artificial coupling | Separate |
| G14 | Feature envy | Move method |
| G15 | Selector arguments | Split functions |
| G16 | Obscured intent | Clarify |
| G17 | Misplaced responsibility | Move it |
| G18 | Inappropriate static | Make non-static |
| G19 | No explanatory variables | Name intermediates |
| G20 | Vague function name | Rename |
| G21 | Don't understand algorithm | Refactor until obvious |
| G22 | Logical dependency | Make physical |
| G23 | Switch/if-else chain | Polymorphism |
| G24 | Non-standard conventions | Follow standard |
| G25 | Magic numbers | Named constant |
| G26 | Imprecision | Be exact |
| G27 | Convention over structure | Enforce structurally |
| G28 | Raw boolean logic | Encapsulate in method |
| G29 | Negative conditional | Flip to positive |
| G30 | Multiple things in function | Split |
| G31 | Hidden temporal coupling | Bucket brigade |
| G32 | Arbitrary structure | Justify or fix |
| G33 | Scattered boundary logic | Encapsulate |
| G34 | Mixed abstraction levels | Descend one level |
| G35 | Config data in low levels | Move to high levels |
| G36 | Transitive navigation | Law of Demeter |
| J1 | Long import lists | Wildcard imports |
| J2 | Inheriting constants | Static import |
| J3 | int constants for enums | Use Java enums |
| N1 | Poor descriptive names | Rename |
| N2 | Wrong abstraction level name | Rename |
| N3 | Custom nomenclature | Use standard terms |
| N4 | Ambiguous name | Be specific |
| N5 | Short name, long scope | Lengthen name |
| N6 | Encoded names | Remove prefixes |
| N7 | Hidden side-effect in name | Name the side-effect |
| T1 | Insufficient tests | Write more |
| T2 | No coverage tool | Use one |
| T3 | Skipping trivial tests | Write them |
| T4 | Ignored test = ambiguity | Document as test |
| T5 | Untested boundaries | Test edges |
| T6 | Single bug, no follow-up | Exhaustive test |
| T7 | Not analyzing failures | Look for patterns |
| T8 | Ignoring coverage gaps | Study gaps |
| T9 | Slow tests | Speed them up |

---

## See Also

- [[Clean Code Overview]] — Chapter summaries and core philosophy
- [[Clean Code Principles]] — DRY, Least Surprise, Boy Scout Rule
- [[Function Design]] — Arguments, do one thing, one level of abstraction
- [[Naming Conventions]] — Descriptive names, level of abstraction, encodings
- [[Comment Patterns]] — When to comment, what makes a good comment
- [[Formatting Style]] — Vertical density, horizontal alignment, team conventions
- [[Objects vs Data Structures]] — Polymorphism, switch statements, Feature Envy
- [[Class Design & SOLID]] — SRP, OCP, base/derivative relationships
- [[Error Handling]] — Boundaries, null checks, exception patterns
- [[Boundaries & Dependencies]] — Law of Demeter, transitive navigation
- [[Unit Testing]] — F.I.R.S.T., coverage, boundary conditions, test speed
- [[Emergent Design]] — Simple Design rules, refactoring toward cleanliness
- [[Concurrency]] — Thread safety, deadlock, testing multithreaded code
- [[System Architecture]] — Separation, configuration at high levels
- [[Code Smell Overview]] — Alternative listing of the same smells
- [[Clean Architecture Overview]] — Higher-level architectural heuristics
