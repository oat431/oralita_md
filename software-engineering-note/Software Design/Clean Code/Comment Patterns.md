---
tags:
- clean-code
- software-design
- software-engineering
---

# Comment Patterns

> *Source: Clean Code by Robert C. Martin, Chapter 4 (pp. 53–74)*

> *"Don't comment bad code—rewrite it."*
> — Brian W. Kernighan and P. J. Plaugher

---

## Core Philosophy

**Comments are, at best, a necessary evil.** The proper use of comments is to compensate for our failure to express ourselves in code. Comments are always failures—not a cause for celebration.

**Comments lie.** Not always, and not intentionally, but too often. The older a comment is and the farther away from the code it describes, the more likely it is to be just plain wrong. Code changes and evolves; comments don't always follow.

**Inaccurate comments are far worse than no comments at all.** They delude and mislead. Truth can only be found in one place: the code.

### Comments Do Not Make Up for Bad Code

Clear and expressive code with few comments is far superior to cluttered and complex code with lots of comments. Rather than spend time writing comments that explain the mess, spend it cleaning that mess.

### Explain Yourself in Code

```java
// ❌ Comment explaining what code does
// Check to see if the employee is eligible for full benefits
if ((employee.flags & HOURLY_FLAG) && (employee.age > 65))
```

```java
// ✅ Intent expressed in code
if (employee.isEligibleForFullBenefits())
```

> It takes only a few seconds of thought to explain most of your intent in code. In many cases it's simply a matter of creating a function that says the same thing as the comment you want to write.

---

## Good Comments

> The only truly good comment is the comment you found a way not to write.

### Legal Comments
Copyright and authorship statements required by corporate policy. Keep them brief; refer to a standard license instead of putting full terms in the comment. Let the IDE collapse them.

```java
// Copyright (C) 2003,2004,2005 by Object Mentor, Inc. All rights reserved.
// Released under the terms of the GNU General Public License version 2 or later.
```

### Informative Comments
Provide basic information when the code itself can't. Still, prefer a better name or a dedicated class first.

```java
// format matched kk:mm:ss EEE, MMM dd, yyyy
Pattern timeMatcher = Pattern.compile(
    "\\d*:\\d*:\\d* \\w*, \\w* \\d*, \\d*");
```

Better alternative: extract to a `DateFormatConverter` class and eliminate the comment entirely.

### Explanation of Intent
Document *why* a non-obvious decision was made. These are among the most valuable comments.

```java
// ✅ Explains intent behind a non-obvious return value
return 1; // we are greater because we are the right type.
```

```java
// ✅ Explains an unusual testing strategy
// This is our best attempt to get a race condition
// by creating large number of threads.
for (int i = 0; i < 25000; i++) { ... }
```

### Clarification
Translate obscure arguments or return values into something readable—especially when dealing with standard libraries or code you cannot change.

```java
assertTrue(a.compareTo(b) == -1); // a < b
assertTrue(b.compareTo(a) == 1);  // b > a
```

> ⚠ **Risk:** Clarifying comments are hard to verify. Before writing them, make sure there is no better way—and then make sure they're accurate.

### Warning of Consequences
Warn other programmers about non-obvious side effects or dangers.

```java
// SimpleDateFormat is not thread safe,
// so we need to create each instance independently.
SimpleDateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z");
df.setTimeZone(TimeZone.getTimeZone("GMT"));
return df;
```

This prevents an overly eager programmer from using a static initializer in the name of efficiency.

### TODO Comments
Mark work that should be done but can't be done right now. Not an excuse to leave bad code.

```java
// TODO-MdM these are not needed
// We expect this to go away when we do the checkout model
protected VersionInfo makeVersion() throws Exception {
    return null;
}
```

> Scan TODOs regularly and eliminate the ones you can. Don't let them litter the codebase.

### Amplification
Emphasize the importance of something that otherwise seems inconsequential.

```java
String listItemContent = match.group(3).trim();
// the trim is real important. It removes the starting
// spaces that could cause the item to be recognized
// as another list.
new ListItemWidget(this, listItemContent, this.level + 1);
```

### Javadocs in Public APIs
Well-described public APIs are invaluable—the Java standard library javadocs are a case in point. If you're writing a public API, write good javadocs for it.

> Javadocs can be just as misleading, nonlocal, and dishonest as any other kind of comment. The rest of this chapter still applies.

---

## Bad Comments

Most comments fall into this category. Usually they are crutches or excuses for poor code.

### Mumbling
A comment thrown in without care, leaving the reader with more questions than answers.

```java
// ❌ What does this actually mean?
catch(IOException e) {
    // No properties files means all defaults are loaded
}
```

What loads the defaults? Where? Was this a reminder to come back later? A comment that forces you to examine other modules to understand it has failed.

### Redundant Comments
Restating what the code already says, but less precisely.

```java
// ❌ Redundant—longer to read than the code
// Utility method that returns when this.closed is true. Throws an exception
// if the timeout is reached.
public synchronized void waitForClose(final long timeoutMillis)
    throws Exception {
    if(!closed) {
        wait(timeoutMillis);
        if(!closed)
            throw new Exception("MockResponseSender could not be closed");
    }
}
```

### Misleading Comments
A comment that's imprecise enough to be wrong. In the `waitForClose` example above, the comment says "returns when this.closed is true"—but the method actually waits for a blind timeout and then throws if closed is still false. Subtle misinformation like this causes painful debugging sessions.

### Mandated Comments
Rules like "every function must have a javadoc" or "every variable must have a comment" produce clutter that propagates lies.

```java
// ❌ Mandated noise—adds nothing
/**
 * @param title The title of the CD
 * @param author The author of the CD
 * @param tracks The number of tracks on the CD
 * @param durationInMinutes The duration of the CD in minutes
 */
public void addCD(String title, String author,
                  int tracks, int durationInMinutes) { ... }
```

### Journal Comments
Change logs at the top of modules.

```
* Changes (from 11-Oct-2001)
* 11-Oct-2001 : Re-organised the class and moved it to new package (DG);
* 05-Nov-2001 : Added a getDescription() method (DG);
* 12-Nov-2001 : Fixed bugs (DG);
```

This made sense before source code control systems existed. Now these are just clutter. **Delete them.** Git remembers.

### Noise Comments
Restating the obvious with zero new information.

```java
// ❌ Pure noise
/** Default constructor. */
protected AnnualDateRule() { }

/** The day of the month. */
private int dayOfMonth;
```

We learn to ignore noise—then real comments get ignored too, and eventually everything lies as the code changes.

### Scary Noise
Noisy javadocs, often with copy-paste errors.

```java
/** The name. */
private String name;

/** The version. */
private String version;

/** The licenceName. */
private String licenceName;

/** The version. */  // ❌ Copy-paste error: says "version" but is "info"
private String info;
```

If the author wasn't paying attention when writing the comment, why should readers profit from it?

### Don't Use a Comment When You Can Use a Function or a Variable

```java
// ❌ Comment instead of well-named variables
// does the module from the global list <mod> depend on the
// subsystem we are part of?
if (smodule.getDependSubsystems().contains(subSysMod.getSubSystem()))
```

```java
// ✅ Self-documenting through naming
ArrayList moduleDependees = smodule.getDependSubsystems();
String ourSubSystem = subSysMod.getSubSystem();
if (moduleDependees.contains(ourSubSystem))
```

### Position Markers
Banner comments separating sections of a file.

```java
// ❌ Visual noise
// Actions //////////////////////////////////
```

Use sparingly—only when the benefit is significant. Overuse makes them invisible background noise.

### Closing Brace Comments
Labeling `}` with what block it closes.

```java
// ❌ Clutter in small functions
} // while
} // try
} //catch
} //main
```

If you feel the need to mark closing braces, **shorten your functions instead.**

### Attributions and Bylines
"Added by Rick" type comments. Source control systems track this. Bylines become inaccurate over time and pollute the code.

### Commented-Out Code

```java
// ❌ Never do this
InputStreamResponse response = new InputStreamResponse();
response.setBody(formatter.getResultStream(), formatter.getByteCount());
// InputStream resultsStream = formatter.getResultStream();
// StreamReader reader = new StreamReader(resultsStream);
// response.setContent(reader.read(formatter.getByteCount()));
```

Others won't have the courage to delete it. It accumulates like sediment. **Just delete it.** Source control remembers.

### HTML Comments
HTML markup in source code comments makes them unreadable in the editor—the one place they should be readable.

```java
// ❌ Unreadable in the IDE
/**
 * Task to run fit tests.
 * <p/>
 * <pre>
 * Usage:
 * &lt;taskdef name=&quot;execute-fitnesse-tests&quot;
 * ...
 * </pre>
 */
```

If the tool (like Javadoc) needs HTML adornment, that's the tool's responsibility, not the programmer's.

### Nonlocal Information
Comments that describe something far away from where they sit.

```java
// ❌ Describes the default port—something this function has no control over
/**
 * Port on which fitnesse would run. Defaults to <b>8082</b>.
 */
public void setFitnessePort(int fitnessePort) { ... }
```

No guarantee this comment changes when the distant code containing the default changes.

### Too Much Information
Historical discussions, RFC citations, or arcane implementation details that the reader doesn't need.

```java
// ❌ Nobody reading this needs the entire RFC 2045 specification summary
/*
RFC 2045 - Multipurpose Internet Mail Extensions (MIME)
Part One: Format of Internet Message Bodies
section 6.8. Base64 Content-Transfer-Encoding
The encoding process represents 24-bit groups of input bits...
*/
```

### Inobvious Connection
Comments whose relationship to the code is unclear, requiring their own explanation.

```java
// ❌ What is a filter byte? Relates to +1? *3? Why 200?
/*
 * start with an array that is big enough to hold all the pixels
 * (plus filter bytes), and an extra 200 bytes for header info
 */
this.pngBytes = new byte[((this.width + 1) * this.height * 3) + 200];
```

### Function Headers
Short, well-named functions don't need comment headers. A good name is better than a header comment.

### Javadocs in Nonpublic Code
Javadocs are useful for public APIs but are anathema to internal code. The extra formality amounts to cruft and distraction.

---

## Complete Example: Before & After

### ❌ Bad: Comments as a crutch for unclear code

```java
/**
 * This class Generates prime numbers up to a user specified
 * maximum. The algorithm used is the Sieve of Eratosthenes.
 * <p>
 * Eratosthenes of Cyrene, b. c. 276 BC, Cyrene, Libya --
 * d. c. 194, Alexandria. The first man to calculate the
 * circumference of the Earth...
 *
 * @author Alphonse
 * @version 13 Feb 2002 atp
 */
public class GeneratePrimes {
    /**
     * @param maxValue is the generation limit.
     */
    public static int[] generatePrimes(int maxValue) {
        if (maxValue >= 2) { // the only valid case
            // declarations
            int s = maxValue + 1; // size of array
            boolean[] f = new boolean[s];
            int i;
            // initialize array to true.
            for (i = 0; i < s; i++)
                f[i] = true;
            // get rid of known non-primes
            f[0] = f[1] = false;
            // sieve
            int j;
            for (i = 2; i < Math.sqrt(s) + 1; i++) {
                if (f[i]) // if i is uncrossed, cross its multiples.
                    for (j = 2 * i; j < s; j += i)
                        f[j] = false; // multiple is not prime
            }
            // how many primes are there?
            int count = 0;
            for (i = 0; i < s; i++) {
                if (f[i])
                    count++; // bump count.
            }
            int[] primes = new int[count];
            // move the primes into the result
            for (i = 0, j = 0; i < s; i++) {
                if (f[i]) // if prime
                    primes[j++] = i;
            }
            return primes; // return the primes
        } else // maxValue < 2
            return new int[0]; // return null array if bad input.
    }
}
```

*Problems: redundant comments, noise (`// declarations`, `// bump count`), vague variable names (`f`, `s`, `j`), historical trivia in header, bylines, explanation of what instead of why.*

### ✅ Good: Clean code with minimal, intentional comments

```java
/**
 * This class Generates prime numbers up to a user specified
 * maximum. The algorithm used is the Sieve of Eratosthenes.
 * Given an array of integers starting at 2:
 * Find the first uncrossed integer, and cross out all its
 * multiples. Repeat until there are no more multiples
 * in the array.
 */
public class PrimeGenerator {
    private static boolean[] crossedOut;
    private static int[] result;

    public static int[] generatePrimes(int maxValue) {
        if (maxValue < 2)
            return new int[0];
        else {
            uncrossIntegersUpTo(maxValue);
            crossOutMultiples();
            putUncrossedIntegersIntoResult();
            return result;
        }
    }

    private static void uncrossIntegersUpTo(int maxValue) {
        crossedOut = new boolean[maxValue + 1];
        for (int i = 2; i < crossedOut.length; i++)
            crossedOut[i] = false;
    }

    private static void crossOutMultiples() {
        int limit = determineIterationLimit();
        for (int i = 2; i <= limit; i++)
            if (notCrossed(i))
                crossOutMultiplesOf(i);
    }

    private static int determineIterationLimit() {
        // Every multiple in the array has a prime factor that
        // is less than or equal to the root of the array size,
        // so we don't have to cross out multiples of numbers
        // larger than that root.
        double iterationLimit = Math.sqrt(crossedOut.length);
        return (int) iterationLimit;
    }

    private static void crossOutMultiplesOf(int i) {
        for (int multiple = 2 * i;
             multiple < crossedOut.length;
             multiple += i)
            crossedOut[multiple] = true;
    }

    private static boolean notCrossed(int i) {
        return crossedOut[i] == false;
    }

    private static void putUncrossedIntegersIntoResult() {
        result = new int[numberOfUncrossedIntegers()];
        for (int j = 0, i = 2; i < crossedOut.length; i++)
            if (notCrossed(i))
                result[j++] = i;
    }

    private static int numberOfUncrossedIntegers() {
        int count = 0;
        for (int i = 2; i < crossedOut.length; i++)
            if (notCrossed(i))
                count++;
        return count;
    }
}
```

*Only 2 comments remain—both explanatory and necessary. Small, well-named functions replace inline comments. The single remaining inline comment explains the square-root optimization rationale, which cannot be expressed cleanly in code alone.*

---

## Summary Checklist

- [ ] Treat every comment as a **failure of expression**—try to express the intent in code first
- [ ] **Rewrite bad code** instead of commenting it
- [ ] Use **legal comments** only as required; keep them brief and collapsible
- [ ] Write **informative comments** sparingly; prefer better names or dedicated classes
- [ ] Use **intent comments** to explain *why*, not *what*
- [ ] Add **clarification comments** only for unchangeable code (standard libraries); verify they are correct
- [ ] Include **warning comments** for non-obvious consequences (thread safety, performance)
- [ ] Leave **TODO comments** for deferred work; scan and resolve them regularly
- [ ] Use **amplification comments** to highlight importance of subtle details
- [ ] Write thorough **javadocs for public APIs** only; skip them for internal code
- [ ] **Never** commit commented-out code—delete it; source control remembers
- [ ] **No** journal/log comments—source control already tracks this
- [ ] **No** redundant comments that restate the code (`// increment i`)
- [ ] **No** noise comments (`/** Default constructor. */`)
- [ ] **No** closing-brace markers—shorten functions instead
- [ ] **No** position marker banners unless truly warranted
- [ ] **No** attributions or bylines
- [ ] **No** HTML in comments—let the documentation tool handle that
- [ ] Keep comments **local** to the code they describe
- [ ] Keep comments **concise**—no historical essays or unnecessary detail
- [ ] **Refactor** when tempted to write a comment; extract a function or rename a variable

---

## Related

- [[Clean Code Principles]]
- [[Naming Conventions]]
- [[Function Design]]
- [[Code Smells Catalog]]
