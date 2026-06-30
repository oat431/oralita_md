---
tags:
- clean-code
- software-design
- software-engineering
---

# Function Design

> *Source: Clean Code by Robert C. Martin, Chapter 3 (pp. 31–52)*

---

## Core Principle

> **Functions should be small, do one thing, and tell a story.** The art of programming is the art of language design — functions are the verbs, classes are the nouns. Master programmers think of systems as stories to be told, not programs to be written.

---

## The Rules

### 1. Keep Functions Small

**The first rule of functions: they should be small. The second rule: they should be smaller than that.**

Aim for 2–4 lines. Functions should hardly ever be 20 lines long. Kent Beck's Sparkle program had every function at just two, three, or four lines — each transparently obvious, each telling a story.

```java
// ❌ Bad — 40+ lines, multiple abstraction levels, nested logic
public static String testableHtml(
PageData pageData, boolean includeSuiteSetup
) throws Exception {
    WikiPage wikiPage = pageData.getWikiPage();
    StringBuffer buffer = new StringBuffer();
    if (pageData.hasAttribute("Test")) {
        if (includeSuiteSetup) {
            WikiPage suiteSetup = PageCrawlerImpl.getInheritedPage(...);
            // ... 30 more lines of mixed concerns
        }
    }
    // ...
}

// ✅ Good — 4 lines, reads like a story
public static String renderPageWithSetupsAndTeardowns(
PageData pageData, boolean isSuite) throws Exception {
    if (isTestPage(pageData))
        includeSetupAndTeardownPages(pageData, isSuite);
    return pageData.getHtml();
}
```

**Blocks and indenting:** Blocks inside `if`, `else`, `while` should be one line long — probably a function call. Indent level should not exceed one or two. This adds documentary value because the called function has a descriptive name.

### 2. Do One Thing

> *FUNCTIONS SHOULD DO ONE THING. THEY SHOULD DO IT WELL. THEY SHOULD DO IT ONLY.*

A function does one thing if its steps are all **one level of abstraction below the stated name** of the function. Describe the function as a TO paragraph:

> TO *renderPageWithSetupsAndTeardowns*, we check to see whether the page is a test page and if so, we include the setups and teardowns. In either case we render the page in HTML.

**Test:** If you can extract another function from it with a name that is *not merely a restatement of its implementation*, the original function was doing more than one thing.

```java
// ❌ Bad — doing multiple things (declarations, initialization, sieve)
public int[] generatePrimes(int maxValue) {
    // section: declarations
    // section: initializations
    // section: sieve
}

// ✅ Good — each function does exactly one thing
private boolean isTestPage(PageData pageData) {
    return pageData.hasAttribute("Test");
}
```

**Sections within a function** (declarations, initializations, processing) are a symptom of doing more than one thing. One-thing functions cannot be reasonably divided into sections.

### 3. One Level of Abstraction per Function

Statements within a function must all be at the same level of abstraction. Mixing high-level concepts (`getHtml()`) with intermediate details (`PathParser.render(pagePath)`) and low-level noise (`.append("\n")`) is confusing and invites more detail to accrete.

**The Stepdown Rule:** Code should read like a top-down narrative. Every function is followed by those at the next level of abstraction, descending one level at a time:

> To include setups and teardowns, we include setups, then include the test page content, then include the teardowns.
> 
> To include the setups, we include the suite setup if this is a suite, then include the regular setup.
> 
> To include the suite setup, we search the parent hierarchy for the "SuiteSetUp" page and add an include statement with the path of that page.

```java
// ❌ Bad — mixed abstraction levels
public void process() {
    String highLevel = getStrategy();          // high
    String pagePath = PathParser.render(p);     // mid
    buffer.append("\n");                        // low
}

// ✅ Good — each function at one consistent level
private void includeSetupAndTeardownPages() throws Exception {
    includeSetupPages();
    includePageContent();
    includeTeardownPages();
    updatePageContent();
}
```

### 4. Bury Switch Statements

**Switch statements** always do N things, violate SRP (multiple reasons to change), and violate OCP (must change when new types are added). Worse: they tend to multiply — the same switch structure appears in `calculatePay`, `isPayday`, `deliverPay`…

**The fix:** Bury the switch in the basement of an **Abstract Factory**, use it *once* to create polymorphic objects, and hide it behind an inheritance relationship.

```java
// ❌ Bad — switch repeated everywhere
public Money calculatePay(Employee e) throws InvalidEmployeeType {
    switch (e.type) {
        case COMMISSIONED: return calculateCommissionedPay(e);
        case HOURLY:       return calculateHourlyPay(e);
        case SALARIED:     return calculateSalariedPay(e);
        default: throw new InvalidEmployeeType(e.type);
    }
}

// ✅ Good — switch in factory only, polymorphic dispatch
public abstract class Employee {
    public abstract boolean isPayday();
    public abstract Money calculatePay();
    public abstract void deliverPay(Money pay);
}

public class EmployeeFactoryImpl implements EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord r) {
        switch (r.type) {
            case COMMISSIONED: return new CommissionedEmployee(r);
            case HOURLY:       return new HourlyEmployee(r);
            case SALARIED:     return new SalariedEmployee(r);
            default: throw new InvalidEmployeeType(r.type);
        }
    }
}
```

**Rule:** Switch statements are tolerable only if they appear once, create polymorphic objects, and are hidden from the rest of the system.

### 5. Use Descriptive Names

> *"You know you are working on clean code when each routine turns out to be pretty much what you expected."* — Ward Cunningham

The smaller and more focused a function, the easier it is to name. Don't be afraid to make names long. A long descriptive name is better than a short enigmatic name *and* better than a long descriptive comment.

**Consistent phraseology tells a story:**

```java
includeSetupAndTeardownPages
    includeSetupPages
        includeSuiteSetupPage
        includeSetupPage
    includePageContent
    includeTeardownPages
        includeTeardownPage
        includeSuiteTeardownPage
```

Spend time choosing names. Experiment with different names in your IDE. Choosing a good name often reveals a better structure.

### 6. Minimize Function Arguments

**The ideal count is zero (niladic).** One (monadic) is good. Two (dyadic) is tolerable. Three (triadic) should be avoided. More than three (polyadic) needs very special justification.

```java
// ❌ Bad — 4 arguments, hard to test all combinations
Circle makeCircle(double x, double y, double radius, String label);

// ✅ Good — argument object groups related concepts
Circle makeCircle(Point center, double radius);
```

**Common monadic forms (and the only ones readers expect):**
- **Question about the argument:** `boolean fileExists("MyFile")`
- **Transform the argument and return it:** `InputStream fileOpen("MyFile")`
- **Event (use with care):** `void passwordAttemptFailedNtimes(int attempts)`

**Flag arguments are ugly.** Passing a boolean loudly proclaims the function does two things — one thing if `true`, another if `false`. Split the function instead:

```java
// ❌ Bad — what does `true` even mean?
render(true);

// ✅ Good — intent is explicit
renderForSuite();
renderForSingleTest();
```

**Dyads:** Reasonable only when arguments are ordered components of a single value (`new Point(0,0)`). Even then, beware ordering problems — how many times have you swapped `expected` and `actual` in `assertEquals`?

**Argument objects:** When arguments naturally travel together, wrap them in a class. `makeCircle(double x, double y, double r)` → `makeCircle(Point center, double r)`. This isn't cheating — `x` and `y` *are* a concept that deserves a name.

### 7. Use Verbs and Keywords

The function and its arguments should form a **verb/noun pair:**

```java
// ✅ Verb/noun pairs
write(name)              // "name" is being "written"
writeField(name)         // even better — "name" is a "field"
```

For dyads and triads, use the **keyword form** to encode argument roles into the function name:

```java
// ✅ Keyword form mitigates ordering confusion
assertExpectedEqualsActual(expected, actual)

// ❌ Ordering is a convention you have to learn
assertEquals(expected, actual)
```

### 8. Have No Side Effects

**Side effects are lies.** Your function promises to do one thing but also does hidden things — unexpected changes to class variables, parameters, or system globals. These create **temporal couplings** (the function can only be called at certain safe moments) and order dependencies.

```java
// ❌ Bad — checkPassword also initializes a session (hidden side effect!)
public boolean checkPassword(String userName, String password) {
    User user = UserGateway.findByName(userName);
    if (user != User.NULL) {
        String codedPhrase = user.getPhraseEncodedByPassword();
        String phrase = cryptographer.decrypt(codedPhrase, password);
        if ("Valid Password".equals(phrase)) {
            Session.initialize();  // ← SIDE EFFECT! Not in the name!
            return true;
        }
    }
    return false;
}

// ✅ Good — no side effects, or make them explicit
public boolean checkPassword(String userName, String password) {
    // ... only checks password, nothing else
}
// If you must have a temporal coupling, name it:
public void checkPasswordAndInitializeSession(...)
// But that violates "Do One Thing" — so refactor instead.
```

### 9. Avoid Output Arguments

Arguments should be **inputs**. Readers expect data in through arguments, out through the return value. Output arguments cause cognitive double-takes.

```java
// ❌ Bad — is `s` input or output? Must check the signature.
appendFooter(s);
// public void appendFooter(StringBuffer report)  ← s is mutated!

// ✅ Good — use the owning object (this)
report.appendFooter();
```

In OO languages, `this` is the intended output argument — change the state of the owning object instead.

### 10. Command-Query Separation

**A function should either do something or answer something, but not both.** Either change the state of an object (command) or return information about it (query). Doing both creates ambiguity.

```java
// ❌ Bad — is this checking or setting? Verb or adjective?
if (set("username", "unclebob")) ...

// ✅ Good — separated command and query
if (attributeExists("username")) {
    setAttribute("username", "unclebob");
    ...
}
```

### 11. Prefer Exceptions to Error Codes

Returning error codes is a subtle violation of command-query separation. It promotes commands being used in predicates, leading to deeply nested structures:

```java
// ❌ Bad — deeply nested, hard to read
if (deletePage(page) == E_OK) {
    if (registry.deleteReference(page.name) == E_OK) {
        if (configKeys.deleteKey(page.name.makeKey()) == E_OK) {
            logger.log("page deleted");
        } else {
            logger.log("configKey not deleted");
        }
    } else {
        logger.log("deleteReference failed");
    }
} else {
    logger.log("delete failed");
    return E_ERROR;
}

// ✅ Good — happy path is clean, error handling is separate
try {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
} catch (Exception e) {
    logger.log(e.getMessage());
}
```

### 12. Extract Try/Catch Blocks

Try/catch blocks confuse structure and mix error processing with normal processing. Extract their bodies into separate functions:

```java
// ✅ Good — error handling and business logic are separate concerns
public void delete(Page page) {
    try {
        deletePageAndAllReferences(page);
    } catch (Exception e) {
        logError(e);
    }
}

private void deletePageAndAllReferences(Page page) throws Exception {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
}

private void logError(Exception e) {
    logger.log(e.getMessage());
}
```

### 13. Error Handling Is One Thing

If the keyword `try` exists in a function, it should be the **very first word** and there should be nothing after the `catch`/`finally` blocks. The function handles errors — that's its one thing.

### 14. The Error.java Dependency Magnet

Error-code enums like `Error { OK, INVALID, NO_SUCH, LOCKED, ... }` are **dependency magnets.** Every class importing them must recompile and redeploy when the enum changes. Programmers reuse old codes instead of adding new ones.

**Exceptions are better:** New exception classes are derivatives of the base exception class. They can be added without forcing recompilation or redeployment — this is the Open Closed Principle in action.

### 15. Don't Repeat Yourself (DRY)

> *Duplication may be the root of all evil in software.*

Duplicated code bloats the module, multiplies modification effort, and creates multiple opportunities for omission errors. Elimination of duplication has driven innovations from subroutines to database normalization to OOP, AOP, and COP.

```java
// ❌ Bad — same algorithm repeated 4 times (SetUp, SuiteSetUp, TearDown, SuiteTearDown)
// Listing 3-1 has this duplication scattered throughout

// ✅ Good — extract the common algorithm once
private void include(String pageName, String arg) throws Exception {
    WikiPage inheritedPage = findInheritedPage(pageName);
    if (inheritedPage != null) {
        String pagePathName = getPathNameForPage(inheritedPage);
        buildIncludeDirective(pagePathName, arg);
    }
}
```

### 16. Structured Programming (Relaxed for Small Functions)

Dijkstra's rules: every function and block should have one entry and one exit (single `return`, no `break`/`continue`, no `goto`).

**But:** These rules serve little benefit when functions are very small. Occasional multiple `return`, `break`, or `continue` statements can be more expressive than forcing single-exit in a 3-line function. `goto` only makes sense in large functions — avoid it.

### 17. Write First, Refine Later

Nobody writes clean functions on the first draft. The process:

1. **Write it long and messy** — get the thoughts down, with long argument lists, duplicated code, arbitrary names
2. **Have unit tests** covering every clumsy line
3. **Massage and refine** — split functions, rename, eliminate duplication, shrink methods, reorder them, sometimes break out whole classes
4. **Keep tests passing** throughout

Writing software is like writing prose. The first draft is clumsy. You wordsmith it, restructure it, refine it until it reads well.

---

## Summary Checklist

- [ ] Is the function small — 4 lines or fewer where possible, rarely over 20?
- [ ] Does it do exactly **one thing** (all steps one level of abstraction below the function name)?
- [ ] Are all statements at the **same level of abstraction** (Stepdown Rule)?
- [ ] Are switch statements **buried in a factory**, used once, and hidden behind polymorphism?
- [ ] Is the name **descriptive, consistent, and long enough** to tell the story?
- [ ] Is the argument count **0, 1, or at most 2**?
- [ ] Are there **no flag arguments** (split into separate functions instead)?
- [ ] Are argument groups wrapped into **argument objects** where they form a concept?
- [ ] Are function names using **verb/noun pairs** and **keyword forms** for ordering clarity?
- [ ] Are there **no side effects** — does the function do exactly what the name says?
- [ ] Are all arguments **inputs only** — no output arguments?
- [ ] Does the function follow **command-query separation** (do something OR return something, not both)?
- [ ] Are exceptions used **instead of error codes**?
- [ ] Are `try`/`catch` blocks **extracted into their own functions**?
- [ ] Is error handling isolated — if `try` exists, is it the **first word** with nothing after `catch`/`finally`?
- [ ] Is there **no duplicated code** (DRY)?
- [ ] Does the code read like a **top-down narrative** — a set of TO paragraphs telling a story?

---

## Related

- [[Naming Conventions]] — Small functions make good names easier; descriptive names make functions self-documenting
- [[Clean Code Principles]] — DRY, SRP, OCP, and the craftsmanship mindset
- [[Comment Patterns]] — A long comment explaining what a function does is a failure to name it well
- [[Class Design & SOLID]] — Switch statements hide behind polymorphism; SRP keeps functions and classes focused
- [[Code Smells Catalog]] — G34 (functions doing more than one thing), G23 (polymorphism over switch), long functions, long parameter lists
