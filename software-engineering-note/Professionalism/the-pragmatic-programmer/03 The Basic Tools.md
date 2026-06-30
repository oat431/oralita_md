---
tags:
- book-summary
- pragmatic-programmer
- professionalism
- software-engineering
---

# 03 The Basic Tools (Tips 20–29)

A craftsman masters their tools. These are the Pragmatic Programmer's essential toolkit — not IDEs, not frameworks, but the fundamentals.

---

## Tip 20: Keep Knowledge in Plain Text

> Plain text is portable, searchable, durable, and universally readable.

| Plain Text | Binary Formats |
|-----------|---------------|
| Readable in 30 years | Requires specific software |
| Diffable, mergeable | Black box |
| Searchable with grep | Requires custom tools |
| Any editor works | Vendor-locked |

Store documentation, configuration, build scripts, and design notes in plain text. Markdown, YAML, TOML, JSON, XML — all plain text.

---

## Tip 21: Use the Power of Command Shells

> The GUI is convenient. The shell is powerful.

In the shell, you can compose commands, script repetitive tasks, and automate everything. A GUI is point-and-click. A shell is programmable.

```bash
# GUI: manually rename 100 files
# Shell: one line
for f in *.jpg; do mv "$f" "vacation_${f}"; done

# GUI: find which files mention "FIXME"
# Shell:
grep -r "FIXME" src/ | wc -l
```

---

## Tip 22: Use a Single Editor Well

> Pick one editor. Master it. Use it for everything.

Your editor is your primary interface to code. Knowing it cold — every shortcut, every extension, every configuration — pays compound interest. Whether it's VS Code, Vim, Emacs, or IntelliJ: **pick one and go deep.**

---

## Tip 23: Always Use Source Code Control

> Even if you're working alone. Even if it's a one-day project. ALWAYS.

Version control gives you:
- Undo any mistake, anytime
- A history of every change and why
- The confidence to experiment ("if it doesn't work, revert")
- Branching for parallel work
- An audit trail

---

## Tip 24–25: Debugging Mindset

> Fix the problem, not the blame. Don't panic.

### The Debugging Process
1. Isolate the bug. Reproduce it reliably.
2. Form a hypothesis. "I think X is causing Y."
3. Test the hypothesis.
4. If wrong, form a new hypothesis.
5. Fix the root cause, not the symptom.
6. Add a test that would have caught this bug.

### The "select" Isn't Broken Rule

> When you're absolutely certain the bug is in the OS, the compiler, or the library — it's probably in your code. Check your assumptions before blaming the tools.

---

## Tip 26: Don't Assume It — Prove It

> When debugging, don't just "think" you know what's happening. Prove it with data.

- "This variable should be 42" → Print it and verify
- "This function should never get called twice" → Add a counter
- "The database should return results" → Log the query and result

---

## Tip 27: Learn a Text Manipulation Language

> awk, sed, Perl, Python, Ruby — pick one. Master text manipulation.

The ability to slice, dice, transform, and generate text is the programmer's superpower. A 10-line Python script can do what would take hours manually.

---

## Tip 28: Code Generators

> Write code that writes code.

| Passive Generators | Active Generators |
|-------------------|------------------|
| Run once, output saved | Run every build |
| Example: scaffolding tools | Example: ORM entity generation from DB schema |
| Output checked into version control | Output is build artifact |

When you find yourself writing the same boilerplate for the 10th time — generate it.

---

## Sources

- Hunt & Thomas. *The Pragmatic Programmer*, Chapter 3.
