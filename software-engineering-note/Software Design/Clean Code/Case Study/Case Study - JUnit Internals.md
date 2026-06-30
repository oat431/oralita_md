---
tags:
- clean-code
- software-design
- software-engineering
---

# Case Study: JUnit Internals

*Robert C. Martin — Clean Code, Chapter 15 (pp. 251–266)*

> *"No module is immune from improvement, and each of us has the responsibility to leave the code a little better than we found it."*

---

## ### What Is ComparisonCompactor?

The `ComparisonCompactor` is a utility inside JUnit that produces human-readable string mismatch messages. Given two differing strings like `"ABCDE"` and `"ABXDE"`, it identifies the delta and wraps it in brackets with optional surrounding context—output: `<...B[X]D...>`.

The **contextLength** parameter controls how many surrounding characters to show. A context of 0 produces ellipsis (`...`), while a context ≥1 shows that many characters before and after the difference.

The chapter walks through the author's real-world JUnit source code and refactors it step by step as a teaching exercise.

---

## ### The Test Suite — A Specification in Code

Before touching the production code, Martin presents the full test suite (**Listing 15-1**, 19 tests). The tests cover:

- Different context lengths (0, 1, 2)
- Prefix-matched, suffix-matched, and both-matched scenarios
- Overlapping match edge cases
- Null inputs for both expected and actual
- The `Bug609972` regression test

> *"The code is 100 percent covered. Every line of code, every `if` statement and `for` loop, is executed by the tests."*

This is the safety net that makes aggressive refactoring possible. Without it, the changes in this chapter would be reckless.

---

## ### The Original Code — What's Wrong?

The original `ComparisonCompactor.java` (**Listing 15-2**) is already "nicely partitioned, reasonably expressive, and simple in structure." But the Boy Scout Rule demands we leave it better. Here's what needs fixing:

| Issue | Smell | Impact |
|-------|-------|--------|
| Hungarian notation prefix `f` on fields | [[Naming Conventions]] N6 | Redundant scope encoding |
| Guard-clause conditional in `compact()` not encapsulated | [[Function Design]] G28 | Intent is hidden |
| Local variables shadow member names (`expected`, `actual`) | [[Naming Conventions]] N4 | Ambiguous names |
| Negative conditional (`shouldNotCompact`) | [[Code Smells Catalog]] G29 | Harder to parse than positive |
| Method named `compact` that might not compact | [[Naming Conventions]] N7 | Misleading; side-effect hidden |
| `compact()` both compacts AND formats — two responsibilities | [[Class Design & SOLID]] G30 | Cohesion problem |
| `findCommonSuffix` depends on `findCommonPrefix` being called first | [[Code Smells Catalog]] G31 | Hidden temporal coupling |
| `suffixIndex` is 1-based rather than a true length, causing `+1` noise | [[Code Smells Catalog]] G33 | Off-by-one confusion |
| Dead/useless `if` statements in `compactString()` | [[Code Smells Catalog]] G9 | Dead code |
| Long inline expressions in `computeCommonPrefix` and `computeCommonSuffix` | [[Clean Code Principles]] | Poor readability |

### Original Code (before changes)
```java
package junit.framework;

public class ComparisonCompactor {

    private static final String ELLIPSIS = "...";
    private static final String DELTA_END = "]";
    private static final String DELTA_START = "[";

    private int fContextLength;
    private String fExpected;
    private String fActual;
    private int fPrefix;
    private int fSuffix;

    public ComparisonCompactor(int contextLength,
                                String expected,
                                String actual) {
        fContextLength = contextLength;
        fExpected = expected;
        fActual = actual;
    }

    public String compact(String message) {
        if (fExpected == null || fActual == null || areStringsEqual())
            return Assert.format(message, fExpected, fActual);

        findCommonPrefix();
        findCommonSuffix();
        String expected = compactString(fExpected);
        String actual = compactString(fActual);
        return Assert.format(message, expected, actual);
    }

    private String compactString(String source) {
        String result = DELTA_START +
            source.substring(fPrefix, source.length() - fSuffix + 1) + DELTA_END;
        if (fPrefix > 0)
            result = computeCommonPrefix() + result;
        if (fSuffix > 0)
            result = result + computeCommonSuffix();
        return result;
    }

    private void findCommonPrefix() {
        fPrefix = 0;
        int end = Math.min(fExpected.length(), fActual.length());
        for (; fPrefix < end; fPrefix++) {
            if (fExpected.charAt(fPrefix) != fActual.charAt(fPrefix))
                break;
        }
    }

    private void findCommonSuffix() {
        int expectedSuffix = fExpected.length() - 1;
        int actualSuffix = fActual.length() - 1;
        for (;
             actualSuffix >= fPrefix && expectedSuffix >= fPrefix;
             actualSuffix--, expectedSuffix--) {
            if (fExpected.charAt(expectedSuffix) != fActual.charAt(actualSuffix))
                break;
        }
        fSuffix = fExpected.length() - expectedSuffix;
    }

    private String computeCommonPrefix() {
        return (fPrefix > fContextLength ? ELLIPSIS : "") +
            fExpected.substring(Math.max(0, fPrefix - fContextLength), fPrefix);
    }

    private String computeCommonSuffix() {
        int end = Math.min(fExpected.length() - fSuffix + 1 + fContextLength,
                           fExpected.length());
        return fExpected.substring(fExpected.length() - fSuffix + 1, end) +
            (fExpected.length() - fSuffix + 1 < fExpected.length() - fContextLength
                ? ELLIPSIS : "");
    }

    private boolean areStringsEqual() {
        return fExpected.equals(fActual);
    }
}
```

For perspective on how **bad** it *could* have been, the chapter also shows a "defactored" version with names like `ctxt`, `s1`, `s2`, `pfx`, `sfx`, and no methods extracted at all. The original is already far better than that—but we can do better still.

---

## ### Refactoring Step 1: Remove Hungarian Notation

**[[Naming Conventions]] — N6: Scope encoding is redundant.** Modern IDEs highlight member variables differently. The `f` prefix adds no value.

### Before
```java
private int fContextLength;
private String fExpected;
private String fActual;
private int fPrefix;
private int fSuffix;
```

### After
```java
private int contextLength;
private String expected;
private String actual;
private int prefix;
private int suffix;
```

> **Rule:** Let your IDE handle scope visualization. Don't encode it in names.

---

## ### Refactoring Step 2: Encapsulate the Guard Conditional

**[[Function Design]] — G28: Encapsulate conditionals.** The inline `expected == null || actual == null || areStringsEqual()` hides intent. Extract it.

### Before
```java
public String compact(String message) {
    if (expected == null || actual == null || areStringsEqual())
        return Assert.format(message, expected, actual);
    ...
}
```

### After
```java
public String compact(String message) {
    if (shouldNotCompact())
        return Assert.format(message, expected, actual);
    ...
}

private boolean shouldNotCompact() {
    return expected == null || actual == null || areStringsEqual();
}
```

> **Rule:** Name conditionals after what they mean, not what they check.

---

## ### Refactoring Step 3: Disambiguate Variable Names

**[[Naming Conventions]] — N4: Don't shadow member variables.** After renaming `fExpected` to `expected`, the local variables `expected` and `actual` in `compact()` shadow the fields. They represent compacted versions, so name them accordingly.

### Before
```java
String expected = compactString(this.expected);
String actual = compactString(this.actual);
```

### After
```java
String compactExpected = compactString(expected);
String compactActual = compactString(actual);
```

> **Rule:** If a local has a different meaning than the field, give it a different name.

---

## ### Refactoring Step 4: Invert the Negative Conditional

**[[Code Smells Catalog]] — G29: Avoid negatives.** `shouldNotCompact` is a double-negative thought. Invert to `canBeCompacted()` and flip the if/else.

### Before
```java
public String compact(String message) {
    if (shouldNotCompact())
        return Assert.format(message, expected, actual);

    findCommonPrefix();
    findCommonSuffix();
    String compactExpected = compactString(expected);
    String compactActual = compactString(actual);
    return Assert.format(message, compactExpected, compactActual);
}
```

### After
```java
public String compact(String message) {
    if (canBeCompacted()) {
        findCommonPrefix();
        findCommonSuffix();
        String compactExpected = compactString(expected);
        String compactActual = compactString(actual);
        return Assert.format(message, compactExpected, compactActual);
    } else {
        return Assert.format(message, expected, actual);
    }
}

private boolean canBeCompacted() {
    return expected != null && actual != null && !areStringsEqual();
}
```

> **Rule:** Positive conditionals read like English. `if (canBeCompacted())` beats `if (!shouldNotCompact())`.

---

## ### Refactoring Step 5: Rename Method — It Formats, Not Just Compacts

**[[Naming Conventions]] — N7 & [[Function Design]] — G30.** The method named `compact` doesn't always compact—it also formats the message. And when it does compact, it bundles compacting with formatting.

**What it really does:** Formats a comparison. If compacting is appropriate, it compacts first, then formats.

### Before
```java
public String compact(String message) { ... }
```

### After
```java
public String formatCompactedComparison(String message) { ... }
```

But there's still a cohesion problem. The method both compacts and formats. **Extract the compacting logic:**

```java
private String compactExpected;
private String compactActual;

public String formatCompactedComparison(String message) {
    if (canBeCompacted()) {
        compactExpectedAndActual();
        return Assert.format(message, compactExpected, compactActual);
    } else {
        return Assert.format(message, expected, actual);
    }
}

private void compactExpectedAndActual() {
    findCommonPrefix();
    findCommonSuffix();
    compactExpected = compactString(expected);
    compactActual = compactString(actual);
}
```

> **Rule:** A function should do one thing. Compacting and formatting are two things.

---

## ### Refactoring Step 6: Fix Side-Effect Methods to Return Values

**[[Code Smells Catalog]] — G11: Inconsistent conventions.** Inside `compactExpectedAndActual()`, two lines mutate fields (`findCommonPrefix()`, `findCommonSuffix()`) and two lines return values (`compactString(...)`). This is inconsistent.

**Refactor `findCommonPrefix` and `findCommonSuffix` to return their results** instead of writing to fields:

### Before (side-effect style)
```java
private void compactExpectedAndActual() {
    findCommonPrefix();   // mutates prefixIndex via field
    findCommonSuffix();   // mutates suffixIndex via field
    compactExpected = compactString(expected);
    compactActual = compactString(actual);
}

private void findCommonPrefix() {
    prefixIndex = 0;
    int end = Math.min(expected.length(), actual.length());
    for (; prefixIndex < end; prefixIndex++) {
        if (expected.charAt(prefixIndex) != actual.charAt(prefixIndex))
            break;
    }
}
```

### After (return-value style)
```java
private void compactExpectedAndActual() {
    prefixIndex = findCommonPrefix();
    suffixIndex = findCommonSuffix();
    compactExpected = compactString(expected);
    compactActual = compactString(actual);
}

private int findCommonPrefix() {
    int prefixIndex = 0;
    int end = Math.min(expected.length(), actual.length());
    for (; prefixIndex < end; prefixIndex++) {
        if (expected.charAt(prefixIndex) != actual.charAt(prefixIndex))
            break;
    }
    return prefixIndex;
}

private int findCommonSuffix() {
    int expectedSuffix = expected.length() - 1;
    int actualSuffix = actual.length() - 1;
    for (; actualSuffix >= prefixIndex && expectedSuffix >= prefixIndex;
           actualSuffix--, expectedSuffix--) {
        if (expected.charAt(expectedSuffix) != actual.charAt(actualSuffix))
            break;
    }
    return expected.length() - expectedSuffix;
}
```

**Also rename prefix → prefixIndex, suffix → suffixIndex** for accuracy ([[Naming Conventions]] N1). They are indices, not strings.

> **Rule:** Prefer functions that return values over functions that mutate hidden state.

---

## ### Refactoring Step 7: Eliminate Hidden Temporal Coupling

**[[Code Smells Catalog]] — G31: Hidden temporal coupling.** `findCommonSuffix()` depends on `findCommonPrefix()` being called first because it reads `prefixIndex`. If you swap the calls, you get a mystery bug.

**First attempt:** Pass `prefixIndex` as an argument.
```java
suffixIndex = findCommonSuffix(prefixIndex);

private int findCommonSuffix(int prefixIndex) { ... }
```

Martin rejects this: the parameter feels arbitrary and doesn't explain *why* it's needed. Another programmer might remove it. ([[Code Smells Catalog]] G32)

**Better solution:** Merge them into one method that encodes the dependency structurally.

```java
private void compactExpectedAndActual() {
    findCommonPrefixAndSuffix();
    compactExpected = compactString(expected);
    compactActual = compactString(actual);
}

private void findCommonPrefixAndSuffix() {
    findCommonPrefix();
    int expectedSuffix = expected.length() - 1;
    int actualSuffix = actual.length() - 1;
    for (; actualSuffix >= prefixIndex && expectedSuffix >= prefixIndex;
           actualSuffix--, expectedSuffix--) {
        if (expected.charAt(expectedSuffix) != actual.charAt(actualSuffix))
            break;
    }
    suffixIndex = expected.length() - expectedSuffix;
}
```

> **Rule:** If two functions must be called in order, merge them or make the dependency structurally impossible to violate.

---

## ### Refactoring Step 8: Clean Up the Suffix Loop — Extract Helper Methods

The nested loop in `findCommonPrefixAndSuffix()` is hard to parse. Extract `charFromEnd()` and `suffixOverlapsPrefix()` to make the intent explicit.

### Before (confusing loop)
```java
int suffixLength = 1;
for (; !suffixOverlapsPrefix(suffixLength); suffixLength++) {
    if (charFromEnd(expected, suffixLength) !=
        charFromEnd(actual, suffixLength))
        break;
}
suffixIndex = suffixLength;
```

Where:
```java
// Ugly raw access with arithmetic
actual.length() - suffixLength < prefixLength
// --- becomes ---
!suffixOverlapsPrefix(suffixLength)
```

### After (self-documenting)
```java
private void findCommonPrefixAndSuffix() {
    findCommonPrefix();
    int suffixLength = 1;
    for (; !suffixOverlapsPrefix(suffixLength); suffixLength++) {
        if (charFromEnd(expected, suffixLength) !=
            charFromEnd(actual, suffixLength))
            break;
    }
    suffixIndex = suffixLength;
}

private char charFromEnd(String s, int i) {
    return s.charAt(s.length() - i);
}

private boolean suffixOverlapsPrefix(int suffixLength) {
    return actual.length() - suffixLength < prefixLength ||
           expected.length() - suffixLength < prefixLength;
}
```

> **Rule:** Extract one-line helpers when they give a name to an intent.

---

## ### Refactoring Step 9: Fix the Off-by-One — Make suffixLength Truly Zero-Based

**[[Code Smells Catalog]] — G33: Off-by-one confusion.** `suffixIndex` is 1-based, not zero-based. This forces `+1` throughout the code, especially in `computeCommonSuffix()`.

**Change `suffixIndex` to `suffixLength`** and make it zero-based:

| What Changes | Before | After |
|-------------|--------|-------|
| Variable name | `suffixIndex` | `suffixLength` |
| Initialization | `suffixLength = 1` | `suffixLength = 0` |
| `charFromEnd` | `s.charAt(s.length() - i)` | `s.charAt(s.length() - i - 1)` |
| `suffixOverlapsPrefix` | `<` (strict) | `<=` (inclusive) |
| `compactString` substring end | `source.length() - suffixLength + 1` | `source.length() - suffixLength` |
| `computeCommonSuffix` | `expected.length() - suffixLength + 1` | `expected.length() - suffixLength` |

### Before
```java
private String compactString(String source) {
    String result = DELTA_START +
        source.substring(prefixLength, source.length() - suffixLength + 1) + // +1 noise
        DELTA_END;
    if (prefixLength > 0)
        result = computeCommonPrefix() + result;
    if (suffixLength > 0)
        result = result + computeCommonSuffix();
    return result;
}
```

### After (interim)
```java
private String compactString(String source) {
    String result = DELTA_START +
        source.substring(prefixLength, source.length() - suffixLength) + // clean
        DELTA_END;
    if (prefixLength > 0)
        result = computeCommonPrefix() + result;
    if (suffixLength > 0)
        result = result + computeCommonSuffix();
    return result;
}
```

> **Rule:** Zero-based is the convention. A 1-based index masquerading as a length costs you `+1`s everywhere.

---

## ### Refactoring Step 10: Eliminate Dead Conditional Branches

**Bug discovered during refactoring:** After making `suffixLength` zero-based, the condition `if (suffixLength > 0)` should have become `if (suffixLength >= 0)` to preserve the same behavior. But it was left as `> 0`... and *it makes sense now!*

**This means the original `>` was already a bug** — `suffixIndex` could *never* be less than 1 (it was 1-based), so the condition `suffixIndex > 0` was always true. The `if` statement was dead code that executed unconditionally. The same was true for `if (prefixIndex > 0)` when there's no prefix to show.

**Martin comments out both `if` statements and runs the tests — they pass.** Both branches were semantically dead.

### Before (dead if-statements)
```java
private String compactString(String source) {
    String result = DELTA_START +
        source.substring(prefixLength, source.length() - suffixLength) +
        DELTA_END;
    if (prefixLength > 0)
        result = computeCommonPrefix() + result;
    if (suffixLength > 0)
        result = result + computeCommonSuffix();
    return result;
}
```

### After (dead code removed; composition made linear)
```java
private String compactString(String source) {
    return
        computeCommonPrefix() +
        DELTA_START +
        source.substring(prefixLength, source.length() - suffixLength) +
        DELTA_END +
        computeCommonSuffix();
}
```

When `prefixLength` or `suffixLength` is 0, `computeCommonPrefix()` and `computeCommonSuffix()` naturally return `""` — no `if` needed.

> **Rule:** When refactoring reveals dead code, **prove** it's dead with tests, then delete it. Don't leave commented-out code.

---

## ### The Final Clean Version

After several more rounds (inlining, re-extracting, inverting conditionals again, decomposing `compactString` into small composable builder methods), the final result:

```java
package junit.framework;

public class ComparisonCompactor {

    private static final String ELLIPSIS = "...";
    private static final String DELTA_END = "]";
    private static final String DELTA_START = "[";

    private int contextLength;
    private String expected;
    private String actual;
    private int prefixLength;
    private int suffixLength;

    public ComparisonCompactor(
        int contextLength, String expected, String actual
    ) {
        this.contextLength = contextLength;
        this.expected = expected;
        this.actual = actual;
    }

    public String formatCompactedComparison(String message) {
        String compactExpected = expected;
        String compactActual = actual;
        if (shouldBeCompacted()) {
            findCommonPrefixAndSuffix();
            compactExpected = compact(expected);
            compactActual = compact(actual);
        }
        return Assert.format(message, compactExpected, compactActual);
    }

    private boolean shouldBeCompacted() {
        return !shouldNotBeCompacted();
    }

    private boolean shouldNotBeCompacted() {
        return expected == null ||
               actual == null ||
               expected.equals(actual);
    }

    // ── Analysis Functions ──────────

    private void findCommonPrefixAndSuffix() {
        findCommonPrefix();
        suffixLength = 0;
        for (; !suffixOverlapsPrefix(); suffixLength++) {
            if (charFromEnd(expected, suffixLength) !=
                charFromEnd(actual, suffixLength))
                break;
        }
    }

    private char charFromEnd(String s, int i) {
        return s.charAt(s.length() - i - 1);
    }

    private boolean suffixOverlapsPrefix() {
        return actual.length() - suffixLength <= prefixLength ||
               expected.length() - suffixLength <= prefixLength;
    }

    private void findCommonPrefix() {
        prefixLength = 0;
        int end = Math.min(expected.length(), actual.length());
        for (; prefixLength < end; prefixLength++)
            if (expected.charAt(prefixLength) != actual.charAt(prefixLength))
                break;
    }

    // ── Synthesis Functions ──────────

    private String compact(String s) {
        return new StringBuilder()
            .append(startingEllipsis())
            .append(startingContext())
            .append(DELTA_START)
            .append(delta(s))
            .append(DELTA_END)
            .append(endingContext())
            .append(endingEllipsis())
            .toString();
    }

    private String startingEllipsis() {
        return prefixLength > contextLength ? ELLIPSIS : "";
    }

    private String startingContext() {
        int contextStart = Math.max(0, prefixLength - contextLength);
        int contextEnd = prefixLength;
        return expected.substring(contextStart, contextEnd);
    }

    private String delta(String s) {
        int deltaStart = prefixLength;
        int deltaEnd = s.length() - suffixLength;
        return s.substring(deltaStart, deltaEnd);
    }

    private String endingContext() {
        int contextStart = expected.length() - suffixLength;
        int contextEnd =
            Math.min(contextStart + contextLength, expected.length());
        return expected.substring(contextStart, contextEnd);
    }

    private String endingEllipsis() {
        return (suffixLength > contextLength ? ELLIPSIS : "");
    }
}
```

### What Makes This Version Better

1. **Two clean layers:** *Analysis functions* (find prefix/suffix) come first; *Synthesis functions* (build the output string) come last. Topologically sorted — each function is defined right after its last use.

2. **`compact(String s)` as a builder:** Uses `StringBuilder` with named private methods for each fragment: `startingEllipsis()`, `startingContext()`, `DELTA_START`, `delta(s)`, `DELTA_END`, `endingContext()`, `endingEllipsis()`. You can read the assembly order top to bottom.

3. **No dead code, no off-by-one noise, no temporal coupling** — each function stands alone.

4. **Conditional intent is clear:** `shouldBeCompacted()` delegates to `shouldNotBeCompacted()` — both positive and negative forms are available. The original violated G29 (negatives are harder); this version gives you both explicitly.

5. **Method name says what it does:** `formatCompactedComparison(String message)` — no surprises.

---

## ### Refactoring Lessons Learned

| Lesson | Detail |
|--------|--------|
| **Refactoring is iterative and circular** | Martin re-inlined methods he'd previously extracted, and flipped the conditional back to `shouldNotBeCompacted`. One refactoring often leads to another that undoes the first. That's normal. |
| **Tests are non-negotiable** | 100% code coverage gave Martin the confidence to delete dead `if` statements, rename everything, and restructure the architecture. No tests = no refactoring. |
| **Naming is half the battle** | `fContextLength` → `contextLength`. `compact()` → `formatCompactedComparison()`. `suffixIndex` → `suffixLength`. Each rename clarified intent. |
| **Off-by-one errors hide in plain sight** | The 1-based `suffixIndex` caused invisible `+1` pollution. Normalizing to zero-based uncovered dead code and a latent bug. |
| **Hidden temporal coupling is a time bomb** | `findCommonSuffix()` silently depended on `findCommonPrefix()`. Merging them into `findCommonPrefixAndSuffix()` made the dependency obvious and unbreakable. |
| **Extract helpers to name intent** | `charFromEnd(s, i)` and `suffixOverlapsPrefix()` are one-liners. Their value isn't in code reuse — it's in giving names to concepts. |
| **Dead code doesn't always look dead** | The `if (prefixIndex > 0)` guard was *always true* in the original code. Only the refactoring exposed it. |
| **Layered architecture emerges** | The final version has a clear analysis→synthesis pipeline. Good structure isn't designed upfront — it's revealed through cleaning. |
| **Boy Scout Rule** | Always leave the code a little cleaner than you found it. Even JUnit — written by Kent Beck and Erich Gamma — had room for improvement. |

---

## ### Refactoring Checklist

Use this when reviewing your own comparison/formatting code:

- [ ] **No Hungarian notation** — field prefixes (`f`, `m_`, `_`) add no value in modern IDEs
- [ ] **Conditionals are encapsulated** — `if (canBeCompacted())` beats `if (x != null && y != null && !equals())`
- [ ] **Positive conditionals preferred** — `shouldCompact()` over `!shouldNotCompact()`
- [ ] **Method names reflect full behavior** — `formatCompactedComparison()`, not just `compact()`
- [ ] **No local/field name shadowing** — different concepts get different names
- [ ] **Functions return values** — avoid void methods that mutate fields as primary output
- [ ] **No hidden temporal coupling** — if A must run before B, merge them or make the dependency explicit
- [ ] **Zero-based indices** — `length`, not `index + 1`
- [ ] **Dead code removed** — prove it's dead with tests, then delete
- [ ] **Analysis and synthesis separated** — compute first, assemble later
- [ ] **Builder pattern for string composition** — `StringBuilder` with named fragment methods
- [ ] **Tests pass at every step** — refactor in tiny steps; run tests after each change

---

## ### Related Concepts

- [[Clean Code Principles]] — Boy Scout Rule, the craftsmanship mindset
- [[Function Design]] — Small functions, single responsibility, encapsulate conditionals (G28), side-effect-free (G30)
- [[Naming Conventions]] — No Hungarian (N6), no shadowing (N4), accurate names (N1, N7)
- [[Class Design & SOLID]] — Single Responsibility: separate analysis from synthesis
- [[Code Smells Catalog]] — G9 (dead code), G11 (inconsistency), G28, G29, G30, G31, G32, G33
- [[Unit Testing]] — Tests as safety net; 100% coverage enables aggressive refactoring
- [[Refactoring]] — Iterative process, trial and error, extract/inline round-tripping
