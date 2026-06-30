---
tags:
- programming
- qa
- testing
---

# 01 Test Planning & Design

Testing without a plan is just hoping. Good test design answers: what to test, how to test it, in what order, and when to stop.

---

## Test Planning

A test plan answers:

| Question | Deliverable |
|----------|------------|
| **What** are we testing? | Scope, features in/out |
| **How** will we test? | Approaches: manual, automated, exploratory |
| **Who** will test? | Team, roles |
| **When** will we test? | Schedule, milestones |
| **What** environment? | Hardware, software, test data |
| **What** are the risks? | Risk-based prioritization |

---

## Test Case Design

Every test case needs:

```
ID:          TC-LOGIN-001
Title:       Login with valid credentials
Precondition: User exists in DB (test@example.com / password123)
Steps:
  1. Navigate to /login
  2. Enter "test@example.com" in email field
  3. Enter "password123" in password field
  4. Click "Sign In"
Expected:
  - Redirect to /dashboard
  - Welcome message displays user name
  - Auth cookie set with valid JWT
```

---

## Test Oracles

How do you know if a test passed? You need an **oracle** — a mechanism to determine correctness.

| Oracle Type | Example |
|------------|---------|
| **Specification** | "The API must return 201 on successful creation" |
| **Existing system** | Compare output with old version (regression) |
| **Heuristic** | "Response time should be < 500ms" |
| **Consistency** | Same input → same output |
| **Human** | Manual verification (slow, expensive, unreliable) |

> Without an oracle, you're not testing — you're just running code.

---

## Test Prioritization

You can't test everything. Prioritize by risk:

| Priority | What to Test First |
|:--------:|-------------------|
| 🔴 **Critical** | Core business flows (checkout, login, payment) |
| 🟡 **High** | Frequently used features with history of bugs |
| 🟢 **Medium** | Less-used features, edge cases |
| ⚪ **Low** | Cosmetic issues, rarely-triggered paths |

### Risk-Based Testing Matrix

```
                    High Impact
                        │
         ┌──────────────┼──────────────┐
         │  Test First  │  Test Second │
   Low   │              │              │   High
Probability│──────────────┼──────────────│ Probability
         │  Test Last   │  Don't Test  │
         │              │              │
                    Low Impact
```

---

## When to Stop Testing

| Criteria | Threshold |
|----------|-----------|
| **Coverage target met** | 80% line, 90% branch |
| **Defect discovery rate drops** | < 1 new bug/day for 3 consecutive days |
| **Risk acceptable** | All critical/high-risk areas tested |
| **Time/money ran out** | Ship date. Document untested areas. |

---

## Sources

- ISTQB Foundation Level Syllabus
- Kaner, Cem. *Testing Computer Software*, 2nd ed., Wiley, 1999.
