---
tags:
- clean-code
- software-design
- software-engineering
---

# Formatting Style

> *Source: Robert C. Martin, "Clean Code" — Chapter 5: Formatting*
>
> *"Code formatting is about communication, and communication is the professional developer's first order of business."*

---

## Core Principle

> *"When people look under the hood, we want them to be impressed with the neatness, consistency, and attention to detail... We want them to perceive that professionals have been at work."*

Formatting is **not cosmetic**. The functionality you write today will change; the readability of your code sets precedents that affect maintainability and extensibility long after the original code has been rewritten beyond recognition. Your style and discipline survive, even though your code does not.

---

## Vertical Formatting

### **The Newspaper Metaphor**

Think of a source file as a newspaper article:

- **Headline (filename)**: Simple but explanatory — tells you whether you're in the right module.
- **Opening paragraphs (top of file)**: High-level concepts and algorithms. Synopsis of the whole story.
- **Descending detail**: Detail increases as you move downward, ending with the lowest-level functions and details.
- **Many small articles**: A newspaper is composed of many short articles. Source files should be small — typically **under 200 lines**, with an upper limit of 500.

### **Vertical Openness vs Vertical Density**

**Openness** separates concepts. **Density** implies close association.

- Each blank line is a visual cue: *a new and separate concept begins here.*
- Remove blank lines, and the code collapses into an illegible muddle.

```java
// BEFORE: dense, hard to scan — everything blurs together
package fitnesse.wikitext.widgets;
import java.util.regex.*;
public class BoldWidget extends ParentWidget {
public static final String REGEXP = "'''.+?'''";
private static final Pattern pattern = Pattern.compile("'''(.+?)'''",
Pattern.MULTILINE + Pattern.DOTALL);
public BoldWidget(ParentWidget parent, String text) throws Exception {
super(parent);
Matcher match = pattern.matcher(text);
match.find();
addChildWidgets(match.group(1));}
public String render() throws Exception {
StringBuffer html = new StringBuffer("<b>");
html.append(childHtml()).append("</b>");
return html.toString();
}
}

// AFTER: openness separates package, imports, class body, each method
package fitnesse.wikitext.widgets;

import java.util.regex.*;

public class BoldWidget extends ParentWidget {
    public static final String REGEXP = "'''.+?'''";
    private static final Pattern pattern = Pattern.compile("'''(.+?)'''",
        Pattern.MULTILINE + Pattern.DOTALL
    );

    public BoldWidget(ParentWidget parent, String text) throws Exception {
        super(parent);
        Matcher match = pattern.matcher(text);
        match.find();
        addChildWidgets(match.group(1));
    }

    public String render() throws Exception {
        StringBuffer html = new StringBuffer("<b>");
        html.append(childHtml()).append("</b>");
        return html.toString();
    }
}
```

**Vertical density** keeps tightly related lines together. Don't break close association with useless comments:

```java
// BEFORE: comments destroy density between two tightly related fields
public class ReporterConfig {
    /**
     * The class name of the reporter listener
     */
    private String m_className;

    /**
     * The properties of the reporter listener
     */
    private List<Property> m_properties = new ArrayList<Property>();

    public void addProperty(Property property) {
        m_properties.add(property);
    }
}

// AFTER: fits in an "eye-full" — class structure is instantly visible
public class ReporterConfig {
    private String m_className;
    private List<Property> m_properties = new ArrayList<Property>();

    public void addProperty(Property property) {
        m_properties.add(property);
    }
}
```

### **Vertical Distance**

Concepts that are closely related should be kept **vertically close** to each other. Vertical separation should be a measure of how important each concept is to understanding the other.

#### **Variable Declarations**

| Variable Type | Convention |
|---|---|
| **Local variables** | As close to usage as possible (top of each short function) |
| **Loop control variables** | Inside the loop statement |
| **Instance variables** | At the top of the class, in one well-known place |

```java
// Local variables at top of function
public int countTestCases() {
    int count = 0;
    for (Test each : tests)
        count += each.countTestCases();
    return count;
}
```

**Anti-pattern**: Burying instance variables mid-file (as in JUnit's `TestSuite` — two fields `fName` and `fTests` hidden halfway down among static methods). Everyone should know exactly where to go to see the declarations.

#### **Dependent Functions**

If one function calls another, they should be vertically close, and the **caller should be above the callee**. This creates a natural downward flow — readers can trust that function definitions follow shortly after their use.

```java
// Caller-above-callee creates a natural top-down reading flow
public Response makeResponse(FitNesseContext context, Request request)
        throws Exception {
    String pageName = getPageNameOrDefault(request, "FrontPage");
    loadPage(pageName, context);
    if (page == null)
        return notFoundResponse(context, request);
    else
        return makePageResponse(context);
}

private String getPageNameOrDefault(Request request, String defaultPageName) {
    String pageName = request.getResource();
    if (StringUtil.isBlank(pageName))
        pageName = defaultPageName;
    return pageName;
}

protected void loadPage(String resource, FitNesseContext context)
        throws Exception {
    WikiPagePath path = PathParser.parse(resource);
    crawler = context.root.getPageCrawler();
    crawler.setDeadEndStrategy(new VirtualEnabledPageCrawler());
    page = crawler.getPage(context.root, path);
    if (page != null)
        pageData = page.getData();
}
```

#### **Conceptual Affinity**

Some bits of code have affinity beyond direct dependence — shared naming schemes, similar operations, a common task. The stronger the affinity, the less vertical distance between them.

```java
// Strong conceptual affinity: shared naming scheme, same basic task
public class Assert {
    static public void assertTrue(String message, boolean condition) {
        if (!condition)
            fail(message);
    }

    static public void assertTrue(boolean condition) {
        assertTrue(null, condition);
    }

    static public void assertFalse(String message, boolean condition) {
        assertTrue(message, !condition);
    }

    static public void assertFalse(boolean condition) {
        assertFalse(null, condition);
    }
    // ...
}
```

### **Vertical Ordering (Caller Above Callee)**

Function call dependencies should point **downward**. A called function is placed below the function that calls it. This creates a flow from high-level to low-level detail — exactly like a newspaper article.

> The most important concepts come first, expressed with the least polluting detail. Low-level details come last. Readers skim the first few functions to get the gist, without immersing themselves in details.

---

## Horizontal Formatting

### **Line Width**

Programmers prefer short lines. The empirical distribution across seven major Java projects shows:

- **~40% of lines** are between 20–60 characters
- **~30% of lines** are under 10 characters
- Lines above 80 characters drop off significantly

**Rule of thumb**: Strive to keep lines short. 80 is traditional; 100–120 is acceptable. Beyond 120 is probably careless. *"I personally set my limit at 120."* — Uncle Bob

### **Horizontal Openness and Density**

Use horizontal white space to **associate** tightly related things and **disassociate** weakly related things.

| Rule | Example |
|---|---|
| **Assignment operators**: surround with spaces to separate left from right | `lineCount++;` / `totalChars += lineSize;` |
| **Function names and parentheses**: no space — function and arguments are closely related | `measureLine(line)` not `measureLine (line)` |
| **Arguments within parentheses**: spaces after commas to show separation | `record(lineSize, lineCount)` |
| **Operator precedence**: no space around high-precedence factors; space around low-precedence terms | `b*b - 4*a*c` |

```java
// Spaces accentuate assignment operators and operator precedence
private void measureLine(String line) {
    lineCount++;
    int lineSize = line.length();
    totalChars += lineSize;
    lineWidthHistogram.addLine(lineSize, lineCount);
    recordWidestLine(lineSize);
}

public class Quadratic {
    public static double root1(double a, double b, double c) {
        double determinant = determinant(a, b, c);
        return (-b + Math.sqrt(determinant)) / (2*a);  // note: 2*a — tight for high precedence
    }

    private static double determinant(double a, double b, double c) {
        return b*b - 4*a*c;  // tight factors, spaced terms
    }
}
```

> ⚠️ Most automatic code formatters are blind to operator precedence and impose uniform spacing. Subtle spacings get lost after reformatting.

### **Horizontal Alignment**

**Don't do it.** Alignment of variable names or rvalues emphasizes the wrong things — it tempts the eye to read down a column of names without looking at types, or down a column of values without seeing the assignment operator.

```java
// BEFORE: aligned declarations — eye reads column of names, not types
public class FitNesseExpediter implements ResponseSender {
    private Socket             socket;
    private InputStream        input;
    private OutputStream       output;
    private Request            request;
    private Response           response;
    private FitNesseContext    context;
}

// AFTER: unaligned — if the list is long enough to need alignment,
// the class should probably be split up
public class FitNesseExpediter implements ResponseSender {
    private Socket socket;
    private InputStream input;
    private OutputStream output;
    private Request request;
    private Response response;
    private FitNesseContext context;
}
```

**Key insight**: If you have long lists that seem to need alignment, the problem is the *length of the lists*, not the lack of alignment. That's a signal that the class should be split.

### **Indentation**

A source file is a hierarchy — file → class → method → block → inner block. Indent in proportion to position in that hierarchy. **Without indentation, programs are virtually unreadable.**

| Scope Level | Indentation |
|---|---|
| File-level (class declaration) | None |
| Methods within class | +1 level |
| Method implementation | +1 level |
| Blocks within methods | +1 level per nesting |

### **Dummy Scopes — Never Collapse**

Never collapse scopes onto a single line. Always indent the body and use braces — even for empty bodies:

```java
// BEFORE: collapsed scope — semicolon is nearly invisible
public class CommentWidget extends TextWidget {
    public static final String REGEXP = "^#[^\r\n]*(?:(?:\r\n)|\n|\r)?";
    public CommentWidget(ParentWidget parent, String text){super(parent, text);}
    public String render() throws Exception {return ""; }
}

// AFTER: expanded and indented — structure is immediately visible
public class CommentWidget extends TextWidget {
    public static final String REGEXP = "^#[^\r\n]*(?:(?:\r\n)|\n|\r)?";

    public CommentWidget(ParentWidget parent, String text) {
        super(parent, text);
    }

    public String render() throws Exception {
        return "";
    }
}
```

For empty loop bodies (dummy scopes), put the semicolon **on its own line, indented**:

```java
// Dummy while-loop — semicolon on its own line, indented, with braces
while (dis.read(buf, 0, readBufferSize) != -1)
    ;
```

---

## Team Rules

> *"A team of developers should agree upon a single formatting style, and every member of that team should use that style."*

- A good software system is composed of documents that read nicely — they need a **consistent and smooth style**.
- The reader must trust that formatting seen in one file means the same thing in another.
- Don't add complexity by writing code in a jumble of different individual styles.
- **Encode the rules** into your IDE's code formatter and stick with them.
- On the FitNesse project, the team decided on brace placement, indent size, naming conventions in **10 minutes** — then encoded them into tooling.

The team rules. Not your personal preference. Not mine.

---

## Uncle Bob's Formatting Rules (Summary)

As illustrated by `CodeAnalyzer.java` (Listing 5-6):

1. **Instance variables** at the top of the class
2. **Public methods** above private methods
3. **Caller functions** above called functions
4. **Related functions** grouped together
5. **Consistent indentation** at every scope level
6. **Blank lines** between separate concepts; none within a single concept
7. **Spaces around assignment operators** and low-precedence operators
8. **No spaces** between function names and opening parentheses
9. **Line width** kept under 120 characters
10. **Dummy scopes** always on their own indented line

---

## Checklist: Formatting Review

- [ ] File size under 500 lines (preferably under 200)
- [ ] File reads like a newspaper: high-level at top, detail descending
- [ ] Blank lines separate distinct concepts
- [ ] Tightly related lines are vertically dense (no useless comments between them)
- [ ] Instance variables declared at the top of the class (one well-known place)
- [ ] Local variables declared close to their usage
- [ ] Caller functions appear above callee functions
- [ ] Functions with conceptual affinity are grouped together
- [ ] Lines are under 120 characters
- [ ] Assignment operators have surrounding spaces
- [ ] No spaces between function names and `(`
- [ ] Operator precedence reflected in spacing (tight for high-precedence, spaced for low)
- [ ] No horizontal alignment of declarations or assignments
- [ ] Consistent indentation at every scope level
- [ ] No collapsed scopes — every block is indented with braces on its own lines
- [ ] Dummy loop bodies have the semicolon on its own indented line
- [ ] Team has one agreed-upon style, enforced by automated tooling

---

## See Also

- [[Clean Code Principles]]
- [[Naming Conventions]]
- [[Function Design]]
- [[Code Smells Catalog]]
