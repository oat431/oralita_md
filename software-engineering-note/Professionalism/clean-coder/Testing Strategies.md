# Testing Strategies

> *Source: The Clean Coder by Robert C. Martin, Chapter 8 (pp. 113–119)*

---

## Core Principle

> **QA Should Find Nothing**

The development team's goal must be that QA finds nothing wrong with the software. Every time QA discovers a defect, the development team should react in horror — investigate how it happened and take steps to prevent it in the future. QA is not an adversary; they are part of the team, working alongside development to ensure quality.

QA's two roles on the team:

1. **QA as Specifiers** — Work with business to create automated acceptance tests that become the true specification and requirements document. Business writes the happy-path tests; QA writes corner, boundary, and unhappy-path tests.
2. **QA as Characterizers** — Use exploratory testing to characterize the true behavior of the running system and report that behavior back to development and business. They identify what the system actually does, not interpret what it should do.

---

## The Test Automation Pyramid

```
           ┌──────────┐
           │ Manual/  │  5%   — Exploratory, human-driven
           │Exploratory│
          ┌┴──────────┴┐
          │  System    │ 10%   — GUI, full integrated system
         ┌┴────────────┴┐
         │  Integration │ 20%   — API, component choreography
        ┌┴──────────────┴┐
        │   Component    │ 50%   — API, acceptance tests
       ┌┴────────────────┴┐
       │    Unit Tests    │ 100%  — xUnit, TDD
       └──────────────────┘
```

### Unit Tests (~100% coverage)

- Written **by programmers, for programmers**, in the system's programming language.
- Written **before** production code via Test Driven Development (TDD).
- Execute as part of Continuous Integration to uphold programmer intent.
- Coverage should be in the 90s — true coverage with meaningful assertions, not tests that execute code without asserting behavior.
- Specify the system at the lowest level.

### Component Tests (~50% coverage)

- Acceptance tests written against individual components that encapsulate business rules.
- Pass input data into a component and gather output data; all other components are decoupled via mocks and test-doubles.
- Written by **QA and Business** with assistance from development, using environments like FitNesse, JBehave, or Cucumber (GUI components use Selenium or Watir).
- Business stakeholders should be able to read and interpret these tests, if not author them.
- Focus on happy-path situations and obvious corner/boundary/alternate-path cases. The vast majority of unhappy-path cases belong to unit tests.

### Integration Tests (~20% coverage)

- Only meaningful for larger systems with many components.
- Assemble groups of components and test **how well they communicate with each other** — choreography tests, not business-rule tests.
- Plumbing tests that ensure components are properly connected and can clearly communicate.
- Written by **system architects or lead designers** to verify architectural soundness.
- May include performance and throughput tests at this level.
- Typically **not** executed as part of the CI suite (longer runtimes); run periodically — nightly, weekly, etc.

### System Tests (~10% coverage)

- Automated tests executed against the **entire integrated system** — the ultimate integration tests.
- Do not test business rules directly; test that the system is wired together correctly and its parts interoperate according to plan.
- Include throughput and performance tests.
- Written by **system architects and technical leads**, in the same language/environment as integration tests for the UI.
- Executed infrequently depending on duration, but the more frequently the better.
- Cover only ~10% of the system because correct behavior is already validated by lower layers of the pyramid.

### Manual/Exploratory Tests (~5% coverage)

- Humans put hands on keyboards and eyes on screens — **not automated, not scripted**.
- Intent: explore the system for unexpected behaviors while confirming expected ones.
- Requires human brains with human creativity; a written test plan defeats the purpose.
- Some teams use dedicated specialists; others declare "bug hunting" days where everyone — managers, secretaries, programmers, testers, tech writers — tries to break the system.
- Goal is **not coverage** of every business rule, but creatively finding as many peculiarities as possible and ensuring the system behaves well under human operation.

---

## Summary Checklist

- [ ] Development's goal: QA should find nothing
- [ ] QA acts as specifiers (automated acceptance tests) and characterizers (exploratory testing)
- [ ] Unit tests driven by TDD, near-100% coverage, part of CI
- [ ] Component tests cover business rules at ~50%, readable by business
- [ ] Integration tests verify component choreography at ~20%, run periodically
- [ ] System tests validate full-system wiring at ~10%
- [ ] Manual exploratory testing at ~5% for creative human investigation
- [ ] All layers run as frequently as possible for maximum feedback

---

## Related

- [[Test Driven Development]]
- [[Acceptance Testing]]
- [[Coding Discipline]]
- [[Continuous Integration]]
