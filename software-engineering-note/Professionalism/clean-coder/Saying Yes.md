# Saying Yes

> *Source: The Clean Coder by Robert C. Martin, Chapter 3 (pp. 45–56)*

---

## Core Principle

> **Professionals use the language of commitment — "I will . . . by . . ." — so there is no doubt about what they've promised. They say yes only when they mean it, and they refuse to sacrifice their professional disciplines to make a commitment possible.**

---

## The Language of Commitment

The chapter opens with a contribution from Roy Osherove. Commitment has three parts: **Say. Mean. Do.** Most people skip one or more of these stages. The language we use reveals whether we're truly committed or just avoiding responsibility.

### Recognizing Weasel Words (Non-Commitment)

These words and phrases signal that the speaker is **not taking personal responsibility** — they behave as victims of circumstance rather than people in control:

| Weasel Word / Phrase | Example | Why It Fails |
|---|---|---|
| **Need / Should** | "We need to get this done." "Someone should make that happen." | Deflects responsibility to an unnamed someone or the universe |
| **Hope / Wish** | "I hope to get this done by tomorrow." "I wish I had time for that." | Assumes the outcome is out of the speaker's hands |
| **Let's** (not followed by "I ...") | "Let's meet sometime." "Let's finish this thing." | Spreads responsibility so thinly that nobody owns it |
| **Try** (the "maybe, maybe not" variant) | "I'll try to get that done as well." | Deliberately ambiguous; neither a yes nor a no |

### The Commitment Formula

Real commitment has a specific linguistic shape:

> **"I will . . . by . . ."**

Every element matters:

- **"I"** — you, personally. Not "we," not "the team," not "someone."
- **"will"** — a definitive statement, not a possibility or hope.
- **"by"** — a concrete end time. The deadline makes the result binary: you either delivered or you didn't.

This formula puts you in front of at least one other person, stating a fact about an action **you** will take with a clear deadline. There is no way out — the result is binary, and you will be held accountable.

---

## The Rules

### 1. Commit Only to What You Control

When the end goal depends on someone else, do not commit to the integrated outcome. Instead, commit to **specific actions** you fully control that move you closer to the target.

**Wrong:** "I'll finish the module with full integration by Friday." (depends on another team)
**Right:** "I'll sit down with Gary from infrastructure to understand our dependencies by Wednesday, and create an interface that abstracts our module from his team's system by Friday."

### 2. When Uncertain, Commit to Investigation

If you don't know whether something can be done, commit to **finding out**. Discovery itself is an action you can own.

**Wrong:** "I'll fix all 25 bugs before the release."
**Right:** "I'll go through all 25 bugs, attempt to reproduce each one, and sit down with QA for a repro on any I can't reproduce — all by end of week."

### 3. Raise Red Flags Immediately

When you realize you cannot meet a commitment, **alert stakeholders the moment you know**. Early warning allows the team to reassess priorities, reassign help, or change the commitment. Silence destroys all options.

> "If you don't tell anyone about the potential problem as soon as possible, you're not giving anyone a chance to help you follow through on your commitment."

### 4. Answer Binary Questions With Binary Answers

When a manager asks a yes/no question about a deadline, avoid fuzzy language like "I think that's doable" or "probably." Give an honest boolean: "No, the earliest I can commit to is Tuesday." If you must express uncertainty, pair it with a concrete worst-case date: "Probably Friday, but it might be Monday."

### 5. Never Trade Professional Standards for a Commitment

When pressured to hit an impossible deadline, the professional does **not** drop testing, refactoring, or the full regression suite. Years of experience prove that breaking disciplines only slows you down. The professional has a prior, higher commitment to code quality — all other commitments are subordinate to it.

### 6. Negotiate Realistic Overtime With Clear Boundaries

If overtime is genuinely the only path to a critical commitment, negotiate it honestly:

- Confirm with family/support system first
- Specify the exact overtime and the recovery time afterward
- Make the trade explicit: "I'll deliver Monday morning, but then I'm gone until Wednesday"

Professionals know their limits. They understand how much overtime they can sustain and what the cost will be — to quality, to health, and to the team.

---

## Commitment Words vs. Weasel Words

| Commitment Language | Weasel Language |
|---|---|
| "I will finish this by Tuesday." | "I need to get this done." |
| "I will meet with Gary by Wednesday." | "Let's meet sometime." |
| "I will go through all 25 bugs this week." | "I hope to get to it by the end of the day." |
| "No, the earliest I can commit to is Tuesday." | "I'll try to get that done as well." |
| "I will have it all ready on Tuesday." | "I think that's doable." |

---

## Summary Checklist

- [ ] Eliminate weasel words — need, should, hope, wish, let's — from your vocabulary when discussing commitments
- [ ] Phrase every commitment as "I will ... by ..." with a specific person, action, and deadline
- [ ] Only commit to outcomes you fully control; commit to concrete actions when dependencies exist
- [ ] When uncertain whether something is possible, commit to investigation and discovery instead
- [ ] Alert stakeholders immediately — not later — the moment you realize a commitment is at risk
- [ ] Answer binary deadline questions with binary answers; replace "probably" with a worst-case date
- [ ] Never sacrifice testing, refactoring, or clean code to meet a commitment
- [ ] If overtime is unavoidable, negotiate it explicitly with clear recovery-time boundaries

---

## Related

- [[Saying No]] — The complement: having the courage to say no when something cannot be done
- [[Professionalism]] — The foundation: professionals speak truth to power
- [[Estimation]] — Providing honest estimates that commitments can be based on
- [[Coding Discipline]] — The professional standards you must never drop under pressure
- [[Pressure]] — Recognizing and resisting the pressures that lead to bad commitments
