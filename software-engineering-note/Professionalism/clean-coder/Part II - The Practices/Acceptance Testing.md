---
tags:
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# Acceptance Testing

> *Source: The Clean Coder by Robert C. Martin, Chapter 7 (pp. 95–111)*

---

## Core Principle

> **Automated acceptance tests are the perfect requirements document. They are completely unambiguous, they execute, and they cannot get out of sync with the application. Done means all acceptance tests pass.**

---

## The Rules

### 1. Define "Done" Unambiguously
Done means done. All code written, all tests pass, QA and stakeholders have accepted. There is no "done-done" — there is only done. The acceptance tests for a feature serve as the formal specification of what "done" means. When they pass, you are done.

### 2. Automate Every Acceptance Test
Acceptance tests must never be manual. The cost of executing manual test plans is enormous — one company Martin consulted for spent over a million dollars per six-week manual test run. Automating acceptance tests is so cheap by comparison that it makes no economic sense to write scripts for humans to execute. Use tools like FitNesse, Cucumber, Selenium, or Robot Framework to make tests readable by non-programmers.

### 3. Collaborate on Test Authorship
Acceptance tests are written by a collaboration of stakeholders, QA, and programmers. Business analysts typically write the "happy path" tests; QA writes the "unhappy path" (boundary conditions, exceptions, corner cases). Developers review for consistency. If developers must write the tests, the author and the implementer must be different people.

### 4. Defer Precision, Eliminate Ambiguity
Avoid premature precision: requirements specified too early become irrelevant as feedback from working software changes what stakeholders want (the "Uncertainty Principle"). But deferring precision must not create late ambiguity. The only reliable antidote to ambiguity is the discipline of writing concrete, executable acceptance tests. An ambiguity in a requirements document represents an unresolved argument among stakeholders.

### 5. Negotiate Tests — Don't Be Passive-Aggressive
When an acceptance test is wrong, awkward, or unrealistic, negotiate with the test author for a better test. Never silently implement exactly what a broken test demands while muttering "that's what the spec says." As a professional, your job is to help the team create the best software possible.

### 6. Write Tests as Late as Possible — But by Iteration Midpoint
Following the principle of late precision, acceptance tests should be written a few days before the feature is implemented. The first tests should be ready by the first day of the iteration, and all tests should be complete by the midpoint. If they are not ready by then, developers must pitch in to finish them. If this happens frequently, add more BAs or QA to the team.

### 7. Keep Acceptance Tests and Unit Tests Separate
Unit tests are design documents written by programmers for programmers — they describe the lowest-level structure and behavior of the code. Acceptance tests are requirements documents written by the business for the business — they specify system behavior from the business's point of view. They test different execution pathways and serve different audiences; they are not redundant.

### 8. Test Business Rules Through an API, Not the GUI
GUIs are subjective and volatile — fonts, colors, layouts, and workflows change constantly. Write business rule acceptance tests to go through a real API just below the GUI. Reserve GUI-specific tests for the GUI itself, decouple the GUI from business rules, and replace business rules with stubs during GUI-only tests. Keep GUI tests minimal.

### 9. Run Tests Continuously — Stop the Presses on Failure
All unit tests and acceptance tests must run several times per day in a continuous integration system, triggered by every commit. A broken CI build is an emergency — a "stop the presses" event. The entire team stops what they are doing and focuses on getting the tests green again. Never remove failing tests from the build to hide the problem.

---

## Key Dialogue: The Log File Backup (Late Ambiguity)

Sam (stakeholder) tells Paula (developer): "OK, now these log files need to be backed up — daily." Paula implements a script that copies *last night's* single log file into a `backup` directory at midnight. Meanwhile, Sam tells Carl (the customer) that the log files will be saved. Carl expects *all* log files, stretching back months or years, to be preserved forever.

When Tom (tester) later joins the conversation, he asks clarifying questions that expose the gap: "Backups of *what*?" and "You mean there's one active log file and many log file backups?" The ambiguity is resolved only through the discipline of writing concrete acceptance tests — the directory is renamed `old_inactive_logs` to make its purpose explicit, and tests are created to verify both directory creation on startup and preservation of existing files.

**Lesson:** An ambiguity in requirements represents an unresolved disagreement. Only executable, precise acceptance tests eliminate it.

---

## Key Dialogue: The Two-Second Post (Test Negotiation)

Tom writes an acceptance test: `ensure that the post operation finishes in 2 seconds`. Paula pushes back — she can only guarantee that statistically (99.5% of the time), not absolutely. Rather than passive-aggressively accepting an impossible test or rejecting it outright, Paula negotiates. She has already spoken with Sam, who is satisfied with a normal user experience of two seconds or less. Together they rework the test to read: `execute 15 post transactions and accumulate times; ensure odds are 99.5% that time will be less than 2 seconds.` Paula commits to showing the intermediate Z-score calculations in the test report so Tom can verify the math.

**Lesson:** Professional developers negotiate with test authors rather than passively submitting to flawed specifications.

---

## Key Scenario: The ED-402 Trouble-Ticket System (Premature Precision)

In 1979, Martin sat with Tom (a non-programmer manager) to build a trouble-ticket system using a macro-based text editor. Over the course of a full day, Martin implemented features while Tom watched, described what he wanted, saw it running, and changed his mind. The cycle time was under five minutes. Martin realized: "He was the sculptor, and I was the tool he was wielding." Tom got exactly the application he needed, but could never have specified it in advance. The lesson: a customer's vision of features rarely survives actual contact with the computer.

---

## Summary Checklist

- [ ] Every feature has automated acceptance tests that define "done"
- [ ] Acceptance tests are written collaboratively by stakeholders, QA, and developers
- [ ] The developer who writes the test is not the same as the developer who implements the feature
- [ ] All acceptance tests are automated — never manual
- [ ] Test authors negotiate with implementers when tests are wrong or unrealistic
- [ ] Business rule tests go through an API, not the GUI
- [ ] GUI-specific tests are minimal and use stubs for business rules
- [ ] All tests run in CI on every commit; a broken build is a "stop the presses" emergency
- [ ] Acceptance tests are written as late as possible but ready by iteration midpoint
- [ ] Acceptance tests and unit tests are kept separate — they serve different audiences

---

## Related

- [[Test Driven Development]]
- [[Testing Strategies]]
- [[Saying Yes]]
- [[Collaboration]]
- [[Estimation]]
