---
tags:
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# Tooling

> *Source: The Clean Coder by Robert C. Martin, Appendix A (pp. 187–204)*

---

The appendix catalogs the essential tools every professional programmer should use. Uncle Bob's opinions are characteristically strong and pragmatic.

---

## Source Code Control

Uncle Bob opens with a personal war story from the late '70s: source code lived on magnetic tapes. Three programmers shared a master tape, checked out files by placing colored pins on a bulletin board, and edited on screen-based terminals (ED-402, similar to vi) — but nobody wrote or modified code directly at the terminal. Changes were marked up on printed listings first, then typed in.

Today's tooling is dramatically better, but the principles endure.

### Open Source vs. "Enterprise" Tools

- **Open source** source control tools are written by developers, for developers. They prioritize what developers actually need — chief among those: **speed**.
- **"Enterprise" version control** systems are sold to managers and executives, not developers. Their feature lists are impressive but often miss what matters on the ground.
- **Pragmatic advice**: If your company has invested in an enterprise system you can't escape, check code into it at iteration boundaries (every two weeks), but use an open-source system inside the iteration. "This keeps everyone happy, doesn't violate any corporate rules, and keeps your productivity high."

### Pessimistic vs. Optimistic Locking

- **Pessimistic locking** (the '80s way): if I'm editing a file, you can't. The colored-pin system was exactly this. Problems: vacation locks, day-long blocks.
- **Optimistic locking** (modern): tools can merge concurrent edits automatically, using the common ancestor and multiple merge strategies. "The era of pessimistic locking is over."
- Modern workflow: check out the whole system, edit any files, run an "update" to merge others' changes, resolve conflicts, then commit. **Never check in code that doesn't pass all tests. Never ever.**

### Tool Evolution: CVS → SVN → Git

- **CVS**: good for its day, but weak on file renames, directory deletion, and the dreaded "attic."
- **Subversion (SVN)**: whole-system checkout, simple update/merge/commit. Works well as long as you avoid heavy branching.
- **Uncle Bob's SVN-era branching rule**: if you create a branch, merge it back before the end of the iteration. Branching was rare.
- **Git** (late 2008 onward): a complete game changer. Distributed, no central repository, no true "main line." Every developer keeps the entire project history locally. Short-lived branches and merges become the natural workflow. "git, and tools like it, are what the future of source code control looks like."

---

## IDE / Editor

As developers, we spend most of our time reading and editing code. The editor is our most intimate tool.

### vi

- Still has a significant following due to simplicity, speed, and flexibility.
- Uncle Bob was once a vi "god" but has barely used it for real coding in the last decade. He still reaches for vi for quick text edits or remote changes.

### Emacs

- One of the most powerful general-purpose editors ever built; the internal Lisp engine guarantees its longevity.
- But: "editing code is not a general-purpose editing job." Emacs can't compete with modern purpose-built IDEs.
- Uncle Bob was an Emacs bigot in the '90s. Then he met IntelliJ in the early 2000s and "never looked back."

### Eclipse / IntelliJ

- **IntelliJ** is Uncle Bob's IDE of choice. He uses it for Java, Ruby, Clojure, Scala, JavaScript, and more. "Written by programmers who understand what programmers need."
- **Eclipse** is comparable in power and scope.
- Both are "leaps and bounds above Emacs" for Java editing.
- **Key advantage**: these IDEs let you manipulate code at the level of *transformations*, not characters and lines. Extract superclass, rename variables, extract methods, convert inheritance to composition — all single-command operations. "The programming model is remarkably different and highly productive."
- **Cost**: steep learning curve, significant setup time, heavy computing resources.

### TextMate

- Lightweight, intuitive, low learning curve. Can't match IntelliJ/Eclipse for code manipulation, but ideal for quick tasks. Uncle Bob uses it for occasional C++ work.

---

## Issue Tracking

Uncle Bob currently uses **Pivotal Tracker** — elegant, simple, fits the Agile/iterative approach, and lets stakeholders and developers communicate quickly.

Other viable options:
- **Lighthouse**: quick and easy for very small projects, but less powerful than Tracker.
- **Wiki**: flexible, imposes no rigid process. Good for internal projects.
- **Cards on a bulletin board**: columns for "To Do," "In Progress," "Done." "This may be the most common issue-tracking system used by agile teams today."

### Uncle Bob's Recommendation

Start with a manual system (bulletin board and cards) *before* purchasing a tracking tool. Once you've mastered the manual system, you'll know what you actually need. The right choice may simply be to keep the manual system.

### Bug Counts

For a team of 5–12 developers, the issue list should be in the **dozens to hundreds** — not thousands. "If you have thousands of bugs, something is wrong. If you have thousands of features and/or tasks, something is wrong."

When issue-tracking tools are forced to track thousands of issues, they become "issue dumps" — and often smell like a dump, too.

---

## Continuous Build

Uncle Bob uses **Jenkins** — lightweight, simple, almost no learning curve.

### Philosophy

- Hook CI to your source code control system: every check-in triggers an automatic build that reports status to the team.
- **Keep the build working at all times.** A build failure is a "stop the presses" event. The team meets and resolves it immediately. "Under no circumstances should the failure be allowed to persist for a day or more."
- On the FitNesse project: developers run the full build script (under 5 minutes) *before* they commit. So the automatic build seldom breaks. Most automatic build failures are environment-related, not code-related.

---

## Testing Tools

### Unit Testing

Language-specific favorites: **JUnit** (Java), **RSpec** (Ruby), **NUnit** (.NET), **Midje** (Clojure), **CppUTest** (C/C++).

Regardless of the tool, five essential features:

1. **Quick and easy to run**. The gesture to run tests must be trivial — a single button push or keyboard shortcut. Uncle Bob runs CppUTest tests with `Command-M` in TextMate; JUnit and RSpec via a button in IntelliJ; NUnit via Resharper.

2. **Clear visual pass/fail indication**. A green bar or a one-line "All Tests Pass" message. If you have to read a multiline report or compare output files to know whether tests passed, the tool has failed this requirement.

3. **Clear visual indication of progress**. A progress bar or a string of dots — anything that tells you tests are still running and haven't stalled.

4. **Discourages test interdependence**. JUnit creates a new test-class instance for each test method, preventing tests from communicating through instance variables. Other tools randomize test order. "Dependent tests are a deep trap that you don't want to fall into."

5. **Makes it very easy to write tests**. Convenient assertion APIs, automatic test discovery (no manual suite wiring), and good IDE integration.

### Component Testing

Component testing tools specify component behavior in a language that business analysts and QA people can understand. They are the means by which we specify what "done" means: when business and QA collaborate to create an executable specification that passes, **"All Tests Pass"** gives "done" an unambiguous meaning.

- **FitNesse**: Uncle Bob's own tool (primary committer). Wiki-based; tests written in simple tabular format (inspired by Parnas tables). Written in Java, but can test systems in any language via Fit or Slim test systems. Supported languages: Java, C#/.NET, C, C++, Python, Ruby, PHP, Delphi, and others.

- **RobotFX**: developed by Nokia engineers. Similar tabular format to FitNesse but not wiki-based; runs on flat files prepared with Excel. Written in Python.

- **Green Pepper**: commercial tool based on the Confluence wiki. Similar to FitNesse.

- **Cucumber**: plain-text tool driven by a Ruby engine. Uses the Given/When/Then style. Can test many platforms.

- **JBehave**: similar to Cucumber, written in Java. Logical parent of Cucumber.

### Integration Testing

Component testing tools can handle many integration tests, but are less appropriate for tests driven through the UI. In general, avoid driving many tests through the UI — UIs are notoriously volatile, making such tests fragile.

However, some tests *must* go through the UI: UI tests themselves, and a few end-to-end smoke tests through the fully assembled system.

Recommended UI testing tools: **Selenium** and **Watir**.

---

## UML / MDA

> *This is where Uncle Bob's skepticism reaches its peak. The take is characteristically blunt — don't soften it.*

### The Dream That Failed

In the early '90s, Uncle Bob was hopeful about CASE tools and Model Driven Architecture (MDA). The vision: software developers would leave textual code behind and author systems in diagrams. Architects could create whole systems from UML. Engines — "vast and cool and unsympathetic to the plight of mere programmers" — would transform diagrams into executable code.

**"Boy was I wrong."**

Every attempt to move in this direction has met with abject failure. The tools exist, but they don't realize the dream, and "hardly anybody seems to want to use them."

### Code Is Not the Problem

The fundamental flaw of MDA: it assumes code is the problem. **Code is not the problem. It has never been the problem. The problem is detail.**

Programmers are **detail managers**. That's what we do — we specify system behavior in the minutest detail. We use textual languages because textual languages are remarkably convenient (consider English, for example).

### The Carriage Return Story

Uncle Bob illustrates "detail" with the `\r` vs `\n` story:

- Teletypes (ASR33) had a print head on a physical carriage. `\r` returned the carriage; `\n` advanced the paper. You needed `\r\n` — in the right order — or characters would print on top of each other or smudge.
- UNIX later shortened this to just `\n`. DOS kept `\r\n`.
- Today, programmers still deal with mismatched line endings at least once a year: files don't compare, checksums don't match, editors misbehave, programs crash on unexpected blank lines.
- **"Try coding the horrible logic for sorting out line ends in UML!"**

### Three Reasons the MDA Hope Is Forlorn

1. **There isn't that much extra detail in code that diagrams can eliminate.** And diagrams contain their *own* accidental details — their own grammar, syntax, rules, and constraints. The difference in detail is a wash.

2. **Diagrams haven't proven to be at a meaningfully higher level of abstraction** than code. The jump from assembler to Java was real. The jump from code to diagrams is "tiny at best."

3. **Even if someone invents a truly useful diagrammatic language, it won't be architects drawing those diagrams — it will be programmers.** The diagrams will simply become the new code, and programmers will be needed to draw it. Because in the end, **it's all about detail, and programmers manage detail.**

---

## Summary Checklist

- [ ] Choose open-source source code control (git preferred); use optimistic locking workflows
- [ ] If stuck with an enterprise VCS, use it at iteration boundaries only — use git/OSS inside iterations
- [ ] Never check in code that doesn't pass all tests
- [ ] Master a modern IDE (IntelliJ/Eclipse) — learn the code transformations, not just the text editing
- [ ] Keep an issue tracking system that stays in the dozens-to-hundreds range, not thousands
- [ ] Start issue tracking with a physical board and cards before buying a tool
- [ ] Hook CI to source control; every commit builds automatically
- [ ] Treat build failures as "stop the presses" events — never let them persist overnight
- [ ] Unit tests must be trivial to run, give clear pass/fail, show progress, prevent interdependence, and be easy to write
- [ ] Use component testing tools (FitNesse, Cucumber, etc.) to create executable specifications that business and QA can read
- [ ] Limit UI-driven tests to UI testing and a few end-to-end smoke tests; use Selenium or Watir
- [ ] Be skeptical of UML/MDA hype — the problem is detail, not code, and programmers are detail managers

---

## Related

- [[Coding Discipline]]
- [[Test Driven Development]]
- [[Testing Strategies]]
- [[Professionalism]]
- [[Saying No]]
