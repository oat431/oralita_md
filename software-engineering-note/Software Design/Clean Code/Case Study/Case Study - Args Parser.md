# Case Study - Args Parser

**Source:** *Clean Code* by Robert C. Martin — Chapter 14, "Successive Refinement" (pp. 193–250)

> *"To write clean code, you must first write dirty code and then clean it."*

---

## Overview

This chapter is a **step-by-step refactoring case study** of a command-line argument parser. Uncle Bob doesn't just show the final clean version—he shows the **entire journey**: the messy first draft, how it gradually rotted as features were added, the moment he decided to stop and refactor, and every tiny step that got him from the festering pile to the clean final product.

The key lesson: **clean code doesn't happen in one pass.** It happens through *successive refinement*—write a rough draft, then clean it up through many small, safe steps (each one keeping all tests passing).

---

## The Final Product (What We're Building Toward)

The clean `Args` class parses command-line arguments via a format string:

```java
// Usage
Args arg = new Args("l,p#,d*", args);
boolean logging = arg.getBoolean('l');   // -l  → boolean flag
int port = arg.getInt('p');              // -p  → integer value
String directory = arg.getString('d');   // -d  → string value
```

### Final Architecture (Listing 14-2)

```java
public class Args {
  private Map<Character, ArgumentMarshaler> marshalers;
  private Set<Character> argsFound;
  private ListIterator<String> currentArgument;

  public Args(String schema, String[] args) throws ArgsException {
    marshalers = new HashMap<Character, ArgumentMarshaler>();
    argsFound = new HashSet<Character>();
    parseSchema(schema);
    parseArgumentStrings(Arrays.asList(args));
  }

  private void parseSchema(String schema) throws ArgsException {
    for (String element : schema.split(","))
      if (element.length() > 0)
        parseSchemaElement(element.trim());
  }

  private void parseSchemaElement(String element) throws ArgsException {
    char elementId = element.charAt(0);
    String elementTail = element.substring(1);
    validateSchemaElementId(elementId);
    if (elementTail.length() == 0)
      marshalers.put(elementId, new BooleanArgumentMarshaler());
    else if (elementTail.equals("*"))
      marshalers.put(elementId, new StringArgumentMarshaler());
    else if (elementTail.equals("#"))
      marshalers.put(elementId, new IntegerArgumentMarshaler());
    else if (elementTail.equals("##"))
      marshalers.put(elementId, new DoubleArgumentMarshaler());
    else if (elementTail.equals("[*]"))
      marshalers.put(elementId, new StringArrayArgumentMarshaler());
    else
      throw new ArgsException(INVALID_ARGUMENT_FORMAT, elementId, elementTail);
  }

  private void parseArgumentStrings(List<String> argsList) throws ArgsException {
    for (currentArgument = argsList.listIterator(); currentArgument.hasNext();) {
      String argString = currentArgument.next();
      if (argString.startsWith("-")) {
        parseArgumentCharacters(argString.substring(1));
      } else {
        currentArgument.previous();
        break;
      }
    }
  }

  private void parseArgumentCharacters(String argChars) throws ArgsException {
    for (int i = 0; i < argChars.length(); i++)
      parseArgumentCharacter(argChars.charAt(i));
  }

  private void parseArgumentCharacter(char argChar) throws ArgsException {
    ArgumentMarshaler m = marshalers.get(argChar);
    if (m == null) {
      throw new ArgsException(UNEXPECTED_ARGUMENT, argChar, null);
    } else {
      argsFound.add(argChar);
      try {
        m.set(currentArgument);
      } catch (ArgsException e) {
        e.setErrorArgumentId(argChar);
        throw e;
      }
    }
  }

  public boolean getBoolean(char arg) {
    return BooleanArgumentMarshaler.getValue(marshalers.get(arg));
  }
  public String getString(char arg) {
    return StringArgumentMarshaler.getValue(marshalers.get(arg));
  }
  public int getInt(char arg) {
    return IntegerArgumentMarshaler.getValue(marshalers.get(arg));
  }
  public boolean has(char arg) { return argsFound.contains(arg); }
}
```

### The Polymorphic Dispatch: ArgumentMarshaler

```java
public interface ArgumentMarshaler {
  void set(Iterator<String> currentArgument) throws ArgsException;
}

public class BooleanArgumentMarshaler implements ArgumentMarshaler {
  private boolean booleanValue = false;
  public void set(Iterator<String> currentArgument) throws ArgsException {
    booleanValue = true;
  }
  public static boolean getValue(ArgumentMarshaler am) {
    if (am != null && am instanceof BooleanArgumentMarshaler)
      return ((BooleanArgumentMarshaler) am).booleanValue;
    return false;
  }
}

public class StringArgumentMarshaler implements ArgumentMarshaler {
  private String stringValue = "";
  public void set(Iterator<String> currentArgument) throws ArgsException {
    try {
      stringValue = currentArgument.next();
    } catch (NoSuchElementException e) {
      throw new ArgsException(MISSING_STRING);
    }
  }
  // getValue similar pattern...
}

public class IntegerArgumentMarshaler implements ArgumentMarshaler {
  private int intValue = 0;
  public void set(Iterator<String> currentArgument) throws ArgsException {
    String parameter = null;
    try {
      parameter = currentArgument.next();
      intValue = Integer.parseInt(parameter);
    } catch (NoSuchElementException e) {
      throw new ArgsException(MISSING_INTEGER);
    } catch (NumberFormatException e) {
      throw new ArgsException(INVALID_INTEGER, parameter);
    }
  }
  // getValue similar pattern...
}
```

**Why this is clean:**
- You can read top-to-bottom without jumping around.
- Adding a new argument type (e.g., Date) requires only: a new `ArgumentMarshaler` derivative, a new `getXXX` method, and one new `else if` in `parseSchemaElement`.
- Each marshaler encapsulates its own parsing, storage, and type conversion.
- Error handling is consistent via `ArgsException`.

---

## The Rough Draft: How the Mess Developed

### Stage 0: Boolean Only (Listing 14-9) — Clean but Fragile

When only booleans existed, the code was simple:

```java
public class Args {
  private Map<Character, Boolean> booleanArgs = new HashMap<>();
  private Set<Character> unexpectedArguments = new TreeSet<>();
  // ...
  private void parseElement(char argChar) {
    if (isBoolean(argChar)) {
      numberOfArguments++;
      setBooleanArg(argChar, true);
    } else
      unexpectedArguments.add(argChar);
  }
  public boolean getBoolean(char arg) {
    return booleanArgs.get(arg);
  }
}
```

This was compact and readable. But it contained the **seeds of the mess**: one `HashMap` per argument type, type-specific `set` methods, and type-specific `get` methods all in one class.

### Stage 1: Boolean + String (Listing 14-10) — Growing Pains

Adding string arguments required:
- A second `HashMap<Character, String> stringArgs`
- `isStringSchemaElement()`, `parseStringSchemaElement()`
- `isString()`, `setStringArg()` with exception handling
- `getString()` with null-safety helper `blankIfNull()`

The class doubled in size. The `setArgument` method now had an `if/else if` chain. Instance variables proliferated.

### Stage 2: Boolean + String + Integer (Listing 14-8) — The Festering Pile

At this point the code became the "festering pile"—functionally correct but structurally rotten:

```java
public class Args {
  // Instance variable explosion — 13 fields!
  private String schema;
  private String[] args;
  private boolean valid = true;
  private Set<Character> unexpectedArguments = new TreeSet<>();
  private Map<Character, Boolean> booleanArgs = new HashMap<>();
  private Map<Character, String> stringArgs = new HashMap<>();
  private Map<Character, Integer> intArgs = new HashMap<>();
  private Set<Character> argsFound = new HashSet<>();
  private int currentArgument;
  private char errorArgumentId = '\0';
  private String errorParameter = "TILT";
  private ErrorCode errorCode = ErrorCode.OK;
  // ...
}
```

The horror in `setArgument`:

```java
private boolean setArgument(char argChar) throws ArgsException {
  if (isBooleanArg(argChar))
    setBooleanArg(argChar, true);
  else if (isStringArg(argChar))
    setStringArg(argChar);
  else if (isIntArg(argChar))
    setIntArg(argChar);
  else
    return false;
  return true;
}
```

Each new type: 3+ new methods + 1 new HashMap + 1 new error code + additions to every conditional chain. **The class was screaming to be refactored.**

---

## The Refactoring Journey: Step by Step

### The Central Insight

> *"Each argument type required new code in three major places: schema parsing, command-line parsing, and value retrieval. Many different types, all with similar methods—that sounds like a class to me."*

This is the moment the **`ArgumentMarshaler`** concept is born. The refactoring target: **replace type-specific HashMaps + conditional chains with polymorphic dispatch**.

### Phase 1: Introduce the ArgumentMarshaler Skeleton (Zero-Risk)

The very first change—adding empty inner classes—cannot break anything:

```java
private class ArgumentMarshaler {
  private boolean booleanValue = false;
  public void setBoolean(boolean value) { booleanValue = value; }
  public boolean getBoolean() { return booleanValue; }
}
private class BooleanArgumentMarshaler extends ArgumentMarshaler { }
private class StringArgumentMarshaler extends ArgumentMarshaler { }
private class IntegerArgumentMarshaler extends ArgumentMarshaler { }
```

**Heuristic:** Make the first change as trivial as possible. If it can't break anything, it won't.

### Phase 2: Migrate One Type at a Time (Boolean First)

Change the Boolean map type:

```java
// Before
private Map<Character, Boolean> booleanArgs = new HashMap<>();

// After
private Map<Character, ArgumentMarshaler> booleanArgs = new HashMap<>();
```

Fix the three touch points—parse, set, get:

```java
// Parse
private void parseBooleanSchemaElement(char elementId) {
  booleanArgs.put(elementId, new BooleanArgumentMarshaler());
}
// Set
private void setBooleanArg(char argChar, boolean value) {
  booleanArgs.get(argChar).setBoolean(value);
}
// Get (bug introduced — NullPointerException when arg not found!)
public boolean getBoolean(char arg) {
  return falseIfNull(booleanArgs.get(arg).getBoolean());
}
```

**A test broke.** The old `falseIfNull` protected against null booleans, but now the null was at the `ArgumentMarshaler` level. Fix:

```java
public boolean getBoolean(char arg) {
  Args.ArgumentMarshaler am = booleanArgs.get(arg);
  return am != null && am.getBoolean();
}
```

**Heuristic:** When a test breaks, fix it *immediately* before continuing. Never pile changes onto a broken system.

### Phase 3: Repeat for String and Integer

Same pattern: change each type-specific HashMap → `Map<Character, ArgumentMarshaler>`, update parse/set/get, keep tests passing.

At this point all three HashMaps still exist, but each now holds `ArgumentMarshaler` values.

### Phase 4: Push Behavior Down into Derivatives (Remove Type-Specific Methods)

**Goal:** Eliminate `setBoolean()`, `setString()`, `setInteger()` from the base class.

First, create an abstract `set(String s)`:

```java
private abstract class ArgumentMarshaler {
  public abstract void set(String s);
}
```

Implement in each derivative:

```java
private class BooleanArgumentMarshaler extends ArgumentMarshaler {
  private boolean booleanValue = false;
  public void set(String s) { booleanValue = true; }  // ignores s
}
private class StringArgumentMarshaler extends ArgumentMarshaler {
  private String stringValue = "";
  public void set(String s) { stringValue = s; }
}
private class IntegerArgumentMarshaler extends ArgumentMarshaler {
  private int intValue = 0;
  public void set(String s) throws ArgsException {
    try {
      intValue = Integer.parseInt(s);
    } catch (NumberFormatException e) {
      throw new ArgsException();
    }
  }
}
```

Then do the same for `get()` → `abstract Object get()`. Each derivative returns its typed value, and callers cast the result.

**Heuristic:** Push behavior down into subclasses one method at a time. The base class shrinks; derivatives become self-contained.

### Phase 5: Unify the Three HashMaps into One (Listing 14-12)

This is the pivotal refactoring. Add a *fourth* map (`marshalers`) and dual-populate during migration:

```java
private Map<Character, ArgumentMarshaler> booleanArgs = ...;
private Map<Character, ArgumentMarshaler> stringArgs = ...;
private Map<Character, ArgumentMarshaler> intArgs = ...;
private Map<Character, ArgumentMarshaler> marshalers = new HashMap<>(); // NEW

private void parseBooleanSchemaElement(char elementId) {
  ArgumentMarshaler m = new BooleanArgumentMarshaler();
  booleanArgs.put(elementId, m);  // old
  marshalers.put(elementId, m);   // new
}
```

Then, method by method, switch from the type-specific map to `marshalers`:

```java
// Before: type-specific lookup
private boolean isBooleanArg(char argChar) {
  return booleanArgs.containsKey(argChar);
}

// After: polymorphic type check via the unified map
private boolean isBooleanArg(char argChar) {
  ArgumentMarshaler m = marshalers.get(argChar);
  return m instanceof BooleanArgumentMarshaler;
}
```

Once all references migrate to `marshalers`, **delete the three type-specific maps**.

**Heuristic:** Use parallel structures during migration—add the new, keep the old, switch references one by one, then remove the old when nothing uses it.

### Phase 6: Eliminate the Type-Case in `setArgument`

The remaining ugly code:

```java
private boolean setArgument(char argChar) throws ArgsException {
  ArgumentMarshaler m = marshalers.get(argChar);
  if (m instanceof BooleanArgumentMarshaler)
    setBooleanArg(m);
  else if (m instanceof StringArgumentMarshaler)
    setStringArg(m);
  else if (m instanceof IntegerArgumentMarshaler)
    setIntArg(m);
  // ...
}
```

**Problem:** `setIntArg` and `setStringArg` reference `args[currentArgument]` directly—instance variables of `Args`. To push these into the marshalers, the marshalers need access to the argument iterator.

**Solution:** Convert the `args` array to a `List<String>` and pass an `Iterator<String>`:

```java
private Iterator<String> currentArgument;
private List<String> argsList;

public Args(String schema, String[] args) throws ParseException {
  argsList = Arrays.asList(args);
  // ...
}

private boolean parseArguments() throws ArgsException {
  for (currentArgument = argsList.iterator(); currentArgument.hasNext();) {
    String arg = currentArgument.next();
    parseArgument(arg);
  }
}
```

Then push `set` with the iterator into marshalers:

```java
// In StringArgumentMarshaler
public void set(Iterator<String> currentArgument) throws ArgsException {
  try {
    stringValue = currentArgument.next();
  } catch (NoSuchElementException e) {
    throw new ArgsException(MISSING_STRING);
  }
}

// In IntegerArgumentMarshaler
public void set(Iterator<String> currentArgument) throws ArgsException {
  String parameter = null;
  try {
    parameter = currentArgument.next();
    intValue = Integer.parseInt(parameter);
  } catch (NoSuchElementException e) {
    throw new ArgsException(MISSING_INTEGER);
  } catch (NumberFormatException e) {
    throw new ArgsException(INVALID_INTEGER, parameter);
  }
}
```

**The `instanceof` chain collapses to a single polymorphic call:**

```java
// Before: type-case nightmare
private boolean setArgument(char argChar) throws ArgsException {
  ArgumentMarshaler m = marshalers.get(argChar);
  if (m instanceof BooleanArgumentMarshaler) m.set(currentArgument);
  else if (m instanceof StringArgumentMarshaler) m.set(currentArgument);
  else if (m instanceof IntegerArgumentMarshaler) m.set(currentArgument);
  else return false;
  return true;
}

// After: pure polymorphism
private boolean setArgument(char argChar) throws ArgsException {
  ArgumentMarshaler m = marshalers.get(argChar);
  if (m == null) return false;
  try {
    m.set(currentArgument);
    return true;
  } catch (ArgsException e) {
    e.setErrorArgumentId(argChar);
    throw e;
  }
}
```

**Heuristic:** An `instanceof` chain against subtypes of the same base class is a code smell. Replace with a polymorphic method on the base class/interface. Each new type requires a new class, not a new `else if`.

### Phase 7: Convert to Interface, Extract Classes

With the hierarchy clean, `ArgumentMarshaler` becomes an interface:

```java
private interface ArgumentMarshaler {
  void set(Iterator<String> currentArgument) throws ArgsException;
  Object get();
}
```

Each marshaler becomes its own top-level `.java` file (not inner classes).

### Phase 8: Extract ArgsException

Error handling code cluttering `Args` is extracted into its own module:

```java
public class ArgsException extends Exception {
  private char errorArgumentId = '\0';
  private String errorParameter = "TILT";
  private ErrorCode errorCode = ErrorCode.OK;

  public enum ErrorCode {
    OK, INVALID_ARGUMENT_FORMAT, UNEXPECTED_ARGUMENT, INVALID_ARGUMENT_NAME,
    MISSING_STRING, MISSING_INTEGER, INVALID_INTEGER,
    MISSING_DOUBLE, INVALID_DOUBLE
  }
  // Constructors, getters, setters, errorMessage()...
}
```

**Heuristic:** `Args` should be about argument processing, not error message formatting. Extract cross-cutting concerns into their own classes. (*See [[Class Design & SOLID]] — SRP.*)

### Phase 9: Adding a New Type (Double) — The Acid Test

The refactoring proves its value when adding `double` takes minimal, isolated changes:

1. One new `else if` in `parseSchemaElement`:
   ```java
   else if (elementTail.equals("##"))
     marshalers.put(elementId, new DoubleArgumentMarshaler());
   ```

2. One new class (`DoubleArgumentMarshaler`), ~20 lines.

3. One new `getDouble()` method on `Args`.

4. Two new error codes (`MISSING_DOUBLE`, `INVALID_DOUBLE`).

No changes to parsing logic, no new HashMaps, no new conditionals in `setArgument`. **This is what clean code enables.**

---

## The Refactoring Playbook: Heuristics Demonstrated

This case study is a masterclass in the following techniques (annotated with Uncle Bob's code smell references):

### 1. **Small, Safe Steps** (Incrementalism)
> *"One of the best ways to ruin a program is to make massive changes to its structure."*

Every change was tiny. Tests ran after each step. When a test broke, it was fixed *immediately*—never pile changes onto a broken system. This is the discipline of [[Clean Code Principles]] — TDD.

### 2. **Introduce Abstraction Gradually** (Parallel Change)
Add the new structure alongside the old. Dual-populate both the old type-specific maps and the new unified map during migration. Switch references one at a time. Delete the old only when nothing references it.

### 3. **Push Behavior Down** (Replace Conditional with Polymorphism)
Type-specific methods (`setBoolean`, `setString`, `setInteger`) and `instanceof` chains get pushed into polymorphic implementations. The base class shrinks to an interface. See [[Class Design & SOLID]] — Open/Closed Principle: open for extension (add new marshaler), closed for modification (no `if/else` chain to edit).

### 4. **Extract Class** (Separation of Concerns)
- `ArgumentMarshaler` → owns value storage and parsing
- `ArgsException` → owns error codes and message formatting
- `Args` → owns schema parsing and argument dispatch
Each class has one reason to change. See [[Code Smells Catalog]] — G16 (Large Class), G7 (Feature Envy).

### 5. **Naming as You Go** [N5]
When `argumentMarshaler` was too long, shorten to `am` in local scope. When `falseIfNull` became irrelevant after a refactoring, delete it immediately. Names must evolve with the code. See [[Naming Conventions]].

### 6. **Eliminate Dead Code Immediately**
`falseIfNull()`, `zeroIfNull()`, `blankIfNull()` — once the null checks moved into the marshalers' `getValue` methods, these helpers were dead. Uncle Bob deleted them the moment they became unused.

### 7. **Keep Functions Small** [F1]
The final `Args` class has methods that do one thing: `parseSchema` is ~5 lines, `parseArgumentCharacter` is ~10 lines. Each method fits on screen.

### 8. **Use Descriptive Names** [N1]
Methods like `parseSchemaElement`, `parseArgumentStrings`, `validateSchemaElementId` describe exactly what they do. No comments needed.

### 9. **Don't Repeat Yourself** (DRY)
The three type-specific HashMaps, three `isXxxArg` methods, three `setXxxArg` methods—all eliminated in favor of one map and polymorphic dispatch.

---

## Key Quotes from the Chapter

> *"It is not enough for code to work. Code that works is often badly broken."*

> *"Nothing has a more profound and long-term degrading effect upon a development project than bad code."*

> *"Bad code rots and ferments, becoming an inexorable weight that drags the team down."*

> *"If you made a mess in a module in the morning, it is easy to clean it up in the afternoon. Better yet, if you made a mess five minutes ago, it's very easy to clean it up right now."*

> *"Much of good software design is simply about partitioning—creating appropriate places to put different kinds of code. This separation of concerns makes the code much simpler to understand and maintain."*

> *"Refactoring is a lot like solving a Rubik's cube. There are lots of little steps required to achieve a large goal. Each step enables the next."*

---

## Refactoring Checklist: From Mess to Clean

Use this as a mental checklist when approaching your own refactoring:

- [ ] **Get it working first.** Write the rough draft. Don't try to be clean on the first pass.
- [ ] **Build a safety net.** Have a test suite you can run in seconds. If you don't have tests, write them *before* refactoring.
- [ ] **Identify the central abstraction.** What concept keeps repeating? (Here: each type needs parse/set/get → a class.)
- [ ] **Introduce the abstraction as a skeleton.** Add empty classes/interfaces that cannot break anything.
- [ ] **Migrate one type at a time.** Convert existing code to use the new abstraction, one argument type at a time, keeping tests green.
- [ ] **Parallel structures.** Add the new structure alongside the old. Switch references incrementally. Delete the old when unused.
- [ ] **Push behavior down.** Move type-specific methods from the base class/central class into derivatives.
- [ ] **Eliminate conditional chains.** Replace `if (x instanceof A) ... else if (x instanceof B)` with polymorphic method calls.
- [ ] **Extract cross-cutting concerns.** Error handling, formatting, logging → their own classes.
- [ ] **Delete dead code.** If a helper function is no longer used after a refactoring, delete it *now*.
- [ ] **Add a new type as validation.** If adding a new type is trivial and isolated, the architecture is right.

---

## See Also

- [[Clean Code Principles]] — TDD, Small Functions, DRY
- [[Function Design]] — Function size, single responsibility, descriptive names
- [[Naming Conventions]] — N1–N7: use intention-revealing, pronounceable, searchable names
- [[Class Design & SOLID]] — SRP, OCP, ISP; extract class, push behavior down
- [[Code Smells Catalog]] — G16 (Large Class), G23 (Type-case with instanceof), G7 (Feature Envy), F1 (too many arguments), N5 (long names)
- [[Refactoring Techniques]] — Replace Conditional with Polymorphism, Extract Class, Inline Method, Pull Up / Push Down
