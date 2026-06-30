---
tags:
- book-summary
- pragmatic-programmer
- professionalism
- software-engineering
---

# 06 While You Are Coding (Tips 44–49)

The act of typing — done right or wrong. This chapter covers what to think about while your fingers are on the keyboard.

---

## Tip 44: Don't Program by Coincidence

> Rely only on reliable things. Beware of accidental success.

Programming by coincidence: you write code that seems to work, but you don't know WHY. You tested it once and it passed. You copy-pasted from Stack Overflow without understanding. You changed a variable and the bug disappeared — but you don't know which change fixed it.

| Coincidental | Deliberate |
|-------------|-----------|
| "It works on my machine." | "Here's the test that proves it works." |
| "I added `sleep(100)` and the race condition went away." | "I fixed the synchronization. Here's the proof." |
| "I think this covers all edge cases." | "Here are the edge cases and the tests for them." |

### How to Avoid It
- **Always know what your code is doing.** If you don't, stop and learn.
- **Plan before you code.** Not waterfall-level. Just think.
- **Test your assumptions.** "I think sorting happens here." Prove it.
- **Document your reasoning.** Not for others — for your future self.

---

## Tip 45: Estimate the Order of Your Algorithms

> Know your O(n). Use Big-O to think about algorithm choices BEFORE writing code.

| n | O(1) | O(log n) | O(n) | O(n log n) | O(n²) | O(2ⁿ) |
|----|:---:|:-------:|:---:|:--------:|:-----:|:-----:|
| 10 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 100 | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| 1,000 | ✅ | ✅ | ✅ | ✅ | ⚠️ | ❌ |
| 100,000 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 1,000,000 | ✅ | ✅ | ✅ | ⚠️ | ❌ | ❌ |

### Practical Rules
- Simple loops = O(n)
- Nested loops = O(n²) (or O(n×m))
- Binary search = O(log n)
- Divide and conquer = O(n log n)
- Generating all subsets = O(2ⁿ)

### Test Your Estimates

> If an algorithm looks like O(n²) but profiling shows O(n log n), your analysis is wrong. Fix it. Understanding why the estimate was wrong teaches more than the estimate itself.

---

## Tip 46: Refactoring — Early and Often

> Refactoring is not a phase. It's a continuous activity.

Like weeding a garden: you don't schedule "weeding week." You pull weeds every time you see them. Code works the same way — fix small problems before they grow.

### When to Refactor
- **Duplication** — you're about to copy-paste
- **Non-orthogonal design** — you notice coupling that shouldn't exist
- **Outdated knowledge** — requirements changed, code didn't
- **Performance** — after profiling, not before

### The Safety Net
Refactoring without tests is not refactoring. It's hacking. Tests give you the confidence to improve code fearlessly.

---

## Tip 47: Code That's Easy to Test

> Design to test. Testability is a design goal, not an afterthought.

| Hard to Test | Easy to Test |
|-------------|-------------|
| Global state | Dependency injection |
| Methods with many responsibilities | Small, focused methods |
| Hardcoded dependencies | Interfaces, mocks |
| No logging/output | Observable behavior |
| GUI logic mixed with business logic | Humble Object / MVP |

### The Test Harness

Build a test harness — a framework that lets you exercise your code automatically. Unit tests, integration tests, end-to-end tests. The harness should run with a single command. It should complete in minutes. It should give you a clear pass/fail.

---

## Tip 48: Don't Use Wizard Code You Don't Understand

> Generated code is still YOUR code. You're responsible for it.

IDE wizards, code generators, AI assistants — they produce code. If you don't understand what that code does, don't use it. When it breaks (and it will break), YOU need to fix it.

| Using Wizards Well | Using Wizards Badly |
|-------------------|-------------------|
| Generate a starting point, then understand and modify | Accept everything without question |
| Read the generated code carefully | Treat it as magic |
| Supplement with your own tests | Assume it's correct |

---

## Sources

- Hunt & Thomas. *The Pragmatic Programmer*, Chapter 6.
