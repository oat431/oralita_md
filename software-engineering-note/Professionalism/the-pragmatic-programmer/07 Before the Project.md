---
tags:
- book-summary
- pragmatic-programmer
- professionalism
- software-engineering
---

# 07 Before the Project (Tips 50–54)

The work that happens before a single line of code is written. Requirements, puzzles, and resisting the pressure to start coding too soon.

---

## Tip 49: The Requirements Pit

> Don't gather requirements — dig for them.

Requirements don't lie on the surface. They're buried under assumptions, politics, and wishful thinking. The Pragmatic Programmer's job is to DIG.

### The Requirements Pitfalls

| Pitfall | Reality |
|---------|---------|
| "The customer told us what they want." | The customer described a symptom, not a solution. |
| "The spec is 200 pages — we're done." | Big specs are often wrong specs. Nobody reads 200 pages. |
| "It's in the document — that means it's a requirement." | A requirement is something you NEED. Document filler is not a requirement. |

### How to Dig

1. **Become the user.** Spend a day doing their job.
2. **Ask "Why?" five times.** Each answer reveals a deeper requirement.
3. **Distinguish needs from wants.** "I need the report by 9am." → Why? → "So I can submit it before the 10am deadline." → The real requirement: "Report available before 10am deadline."
4. **Document use cases, not just features.** Who does what, why, and what happens when things go wrong.

### Use Cases Are Not Requirements

> A use case describes a specific interaction. The requirements are the constraints that ALL use cases must satisfy.

---

## Tip 50: Solving Impossible Puzzles — Don't Think Outside the Box — Find the Box

> When you encounter an impossible problem, you're probably imposing constraints that don't exist.

### The Approach

1. Enumerate all the constraints you believe exist
2. For each constraint, ask: "Is this really a constraint? Who says?"
3. Find the constraints that are self-imposed. Eliminate them.
4. The remaining real constraints bound the real problem — which is now solvable.

### Example

"We need to process 10,000 transactions per second, but the database can only handle 1,000." 
- Constraint: "Database can only handle 1,000" → Real?
- Option: Use multiple databases (sharding)
- Option: Queue and process asynchronously
- Option: Batch transactions

The constraint wasn't real — it was a design assumption masquerading as a limitation.

---

## Tip 51: Not Until You're Ready

> A great idea held too long before its time becomes a great mistake. Let ideas prove themselves before committing.

Listen to nagging doubts. When you feel resistance to an idea, investigate. Don't dismiss the doubt as "just being negative." It might be wisdom.

> Start when you're ready. Not when the schedule says you should start.

---

## Tip 52: The Specification Trap

> Writing a specification is not the same as understanding the requirements.

Specifications are attempts to freeze requirements at a point in time. Requirements change. A specification that's too detailed will be wrong before it's printed. A specification that's too vague is useless.

### The Alternative
- Use **user stories** and **acceptance tests** as living specifications
- Keep specifications lightweight and frequently updated
- Treat specifications as a communication tool, not a legal document

---

## Tip 53: Circles and Arrows — Formal Methods

> Formal methods have their place. But be careful: diagrams can give a false sense of precision.

UML, flowcharts, state diagrams — they're tools for communication, not substitutes for thinking. A beautiful diagram of a bad design is still a bad design. Use them to clarify your thinking, not to impress stakeholders.

> The value is in the process of drawing — making your ideas explicit — not in the artifact itself.

---

## Sources

- Hunt & Thomas. *The Pragmatic Programmer*, Chapter 7.
