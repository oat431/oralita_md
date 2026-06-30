---
tags:
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# Estimation

> *Source: The Clean Coder by Robert C. Martin, Chapter 10 (pp. 135–148)*

---

## Core Principle

> **An estimate is not a number — it is a probability distribution. Professionals draw a clear, non-negotiable line between estimates (guesses, no promise implied) and commitments (hard promises you must keep at any cost). The root of all estimation dysfunction is that business treats estimates as commitments while developers treat them as guesses.**

---

## The Rules

### 1. Never Confuse an Estimate with a Commitment

A **commitment** is something you *must* achieve. If you commit to a date, you honor it — 12-hour days, weekends, skipped vacations if necessary. Professionals do not make commitments unless they *know* they can achieve them. Missing a commitment is an act of dishonesty only slightly less onerous than an overt lie.

An **estimate** is a guess. No promise is made. Missing an estimate is not dishonorable. The reason we estimate is because we don't know how long something will take.

**The critical distinction:** When Peter says "three days," Mike hears a single number. But in Peter's mind, three is merely the *most likely* outcome. There is a whole probability distribution around it — four days, five days, possibly ten or eleven if everything goes wrong.

### 2. Communicate the Full Distribution, Not a Single Number

Giving a single number like "three days" hides the uncertainty. The professional's job is to surface the probability distribution so managers can make informed plans. Ask: "How likely is that estimate?" Then quantify it — 50%? 60%? What's the 95% confidence range?

### 3. Reject Implied Commitments — Especially "Try"

When a manager says, "Can you *try* to make it no more than six days?", the word "try" is a loaded trap. Agreeing to "try" is agreeing to *succeed* — it implies overtime, weekends, and skipped vacations. If you don't do those things, you can be accused of "not trying hard enough." Professionals draw a sharp line: they do not accept implied commitments and do not use "try" as a substitute for certainty.

### 4. Use Trivariate Estimates for Every Task

Never estimate with one number. Always provide three:

- **O (Optimistic):** Wildly optimistic. Everything goes perfectly. Should have <1% chance of occurrence.
- **N (Nominal):** The most likely duration — the highest bar on the probability chart.
- **P (Pessimistic):** Wildly pessimistic. Excludes only hurricanes, nuclear war, and stray black holes. Should have <1% chance of success.

### 5. Model Uncertainty with the PERT Formulas

Given O, N, and P, compute:

- **Expected duration (μ):** μ = (O + 4N + P) / 6
- **Standard deviation (σ):** σ = (P − O) / 6

μ is the expected completion time. σ measures uncertainty — a large σ means high variability. Together they tell the manager what range to plan for (μ ± 1σ is likely; μ ± 2σ is plausible).

### 6. Combine Sequence Estimates Properly

For a sequence of tasks, sums don't work the naive way:

- **μ_sequence = Σ μ_task** (simple sum of expected durations)
- **σ_sequence = √(Σ σ_task²)** (square root of the sum of squares)

Uncertainty compounds. Nominal estimates might add up to 10 days, but the PERT calculation can push the expected duration to 14 days with a 1σ range of 11–17 and a 2σ range of 8–20. This is realistic — projects routinely take 3–5× longer than optimistic guesses.

### 7. Estimate Collaboratively, Never Alone

The most important estimation resource is the people around you. They see things you don't. Estimating alone produces worse results than estimating together. Use structured group techniques to achieve consensus.

### 8. Break Large Tasks into Smaller Ones (Law of Large Numbers)

If you break a large task into many smaller tasks and estimate each independently, the sum of the small estimates will be more accurate than a single estimate of the large task. Errors in small tasks tend to integrate out (cancel each other). Caveat: errors skew toward underestimation, so cancellation is imperfect — but breaking tasks down still forces deeper understanding and uncovers hidden surprises.

---

## Estimating Techniques

- **PERT (Trivariate Analysis):** Created in 1957 for the U.S. Navy's Polaris project. Requires three estimates per task: O (optimistic, <1% chance), N (nominal, most likely), and P (pessimistic, <1% chance). Compute μ = (O + 4N + P) / 6 for expected duration and σ = (P − O) / 6 for uncertainty. For multiple sequential tasks, sum the μs and take the square root of the sum of σ². This produces a proper probability distribution that managers can plan against.

- **Wideband Delphi:** Introduced by Barry Boehm in the 1970s. A team assembles, discusses a task, estimates it, and iterates discussion and estimation until they reach **consensus**. The core insight is that group judgment, refined through structured debate, consistently outperforms individual estimates.

- **Planning Poker:** Popularized by James Grenning (2002). Each team member holds numbered cards (Martin recommends a simple deck: 0, 1, 3, 5, 10). A task is discussed, everyone selects a card face-down, and cards are revealed **simultaneously** to prevent anchoring bias. Agreement means the estimate is accepted; disagreement triggers further discussion and re-voting. Variants exist using Fibonacci sequences (0, 1, 2, 3, 5, 8, 13…) and cards for ∞ (too large) or ? (can't estimate).

- **Flying Fingers:** A low-tech variant. Team sits around a table, discusses a task, then everyone hides hands below the table and raises 0–5 fingers simultaneously on a count of 1-2-3. A mix of 3s and 4s is agreement; one person showing 1 while everyone else shows 4 demands discussion. Scale (days, "fingers × 3", "fingers squared") is decided up front.

- **Affinity Estimation:** A silent, spatial sorting technique. Tasks are written on cards and spread randomly. Team members silently sort cards left (smaller) to right (larger). Anyone can move any card at any time. Cards moved more than *h* times are set aside for discussion. Once sorting stabilizes, discussion begins and lines are drawn to demarcate bucket sizes (e.g., 1, 2, 3, 5, 8 in Fibonacci days/points).

- **Generating Trivariate Estimates from Group Techniques:** Wideband Delphi variants produce a single nominal estimate. To get the three PERT numbers: ask the team to show their pessimistic cards and take the **highest**; ask for optimistic cards and take the **lowest**. The nominal has already been agreed upon.

---

## Summary Checklist

- [ ] Always distinguish between an estimate (guess, no promise) and a commitment (hard promise you must keep)
- [ ] Never give a single-number estimate — communicate the probability distribution
- [ ] Refuse to make commitments when you aren't certain you can achieve them
- [ ] Never agree to "try" — it creates an implied commitment and sets you up for failure
- [ ] Use trivariate estimation: provide Optimistic (O), Nominal (N), and Pessimistic (P) for every task
- [ ] Calculate expected duration: μ = (O + 4N + P) / 6
- [ ] Calculate uncertainty: σ = (P − O) / 6
- [ ] For sequential tasks, sum the μs and take √(Σ σ²) for combined uncertainty
- [ ] Estimate collaboratively — never estimate alone; use Wideband Delphi, Planning Poker, or Flying Fingers
- [ ] Reveal estimates simultaneously to prevent anchoring bias
- [ ] Break large tasks into small ones — the Law of Large Numbers improves accuracy
- [ ] Present managers with ranges (μ ± σ), not single numbers

---

## Related

- [[Saying Yes]]
- [[Saying No]]
- [[Time Management]]
- [[Pressure]]
- [[Professionalism]]
- [[Teams and Projects]]
