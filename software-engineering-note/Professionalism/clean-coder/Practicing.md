# Practicing

> *Source: The Clean Coder by Robert C. Martin, Chapter 6 (pp. 85–94)*

---

## Core Principle

> **Programming speed comes from practice—repeating known problem/solution pairs until they are automatic, just as musicians drill scales and martial artists drill kata. Professionals practice deliberately, on their own time, because it is their responsibility—not their employer's—to keep their skills sharp.**

---

## Practice Formats

### Katas

A **kata** is a precise, choreographed set of keystrokes and mouse movements that simulates solving a known programming problem. You aren't actually solving the problem—you already know the solution. Rather, you are practicing the movements and micro-decisions involved in solving it, striving for asymptotic perfection.

The purpose is to train your brain and fingers how to react, driving common problem/solution pairs into your subconscious so that you simply know how to solve them when facing them in real programming. Katas are also an excellent way to learn hot keys, navigation idioms, and disciplines like TDD and CI.

Like a martial artist, a programmer should know several katas and practice them regularly so they don't fade. Martin's favorites include:
- **The Bowling Game** (TDD flow, design conflict, ~30 min)
- **Prime Factors** (algorithmic decomposition)
- **Word Wrap** (edge cases, incremental design)

For an advanced challenge: learn a kata so well you can perform it set to music.

### Wasa

**Wasa** (from jujitsu) is a two-person kata—precisely memorized routines where partners swap roles. In programming, this maps to **ping-pong pairing**:

1. Partner A writes a failing unit test.
2. Partner B writes the minimum code to make it pass.
3. Roles reverse and the cycle continues.

When partners use a known kata, they critique each other's keyboarding, mousing, and memorization fidelity. When they choose a new problem, the test-writer holds disproportionate power to set constraints (e.g., speed and memory limits on a sort algorithm), making the exercise competitive, improvisational, and fun.

### Randori

**Randori** is free-form, multi-person group practice. With the screen projected on the wall:

1. One person writes a test, then sits down.
2. The next person makes the test pass, writes the next test, and sits down.
3. Rotation continues around the table—or people simply line up as they feel moved.

The primary value of randori is gaining immense insight into how other programmers approach problems—different strategies, tool usage, and design instincts. This broadens your own approach far more than solo practice can.

---

## Ways to Broaden Your Experience

- **Contribute to open source.** Treat it as pro-bono work, like lawyers and doctors do. Work on something someone else cares about—and pick a project outside your day-job stack. If you write Java at work, contribute to a Rails project. If you write C++, find a Python project.
- **Practice in new languages on your own time.** Keep your polyglot skills sharp. If you work in a .NET shop, practice Java or Ruby at lunch or at home.
- **Side projects.** Use your own time to explore languages, platforms, and domains your employer doesn't expose you to. Employers often enforce a single stack; without deliberate broadening, your skills and mindset narrow dangerously, leaving you unprepared when the industry shifts.

---

## Summary Checklist

- [ ] Select 2–3 katas and practice each at least weekly until keystrokes are automatic
- [ ] Perform the Bowling Game Kata until it can be done without conscious thought
- [ ] Find a pair-programming partner and run ping-pong wasa sessions regularly
- [ ] Attend or organize a Coding Dojo with randori rotation
- [ ] Contribute to one open-source project in a language you don't use at work
- [ ] Practice in a new language or platform outside working hours
- [ ] Separate practice time from work time—practice on your own clock
- [ ] Recognize that speed without practice is sloppy; practice makes speed productive

---

## Related

- [[Coding Discipline]]
- [[Test Driven Development]]
- [[Mentoring & Craftsmanship]]
