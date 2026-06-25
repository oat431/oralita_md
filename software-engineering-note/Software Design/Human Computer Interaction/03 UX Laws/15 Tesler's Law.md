# 15 Tesler's Law (Law of Conservation of Complexity)

> **Every system has an irreducible amount of complexity. The question is: who handles it — the user or the system?**

You can't eliminate complexity. You can only move it. A good designer moves complexity into the system so the user doesn't have to deal with it.

---

## The Principle

![Tesler's Law - complexity must go somewhere](https://lawsofux.com/images/teslers-law.svg)

*Source: lawsofux.com*

---

## Who Handles the Complexity?

| The User Handles It | The System Handles It |
|--------------------|-----------------------|
| User must manually enter shipping address | System auto-fills from saved profile |
| User must remember password | System offers "Sign in with Google" / password manager |
| User must format date correctly | System accepts any reasonable format and parses it |
| User must calculate total with tax | System shows total including tax upfront |
| User must search for the right setting | System provides smart defaults |

---

## Examples

### Search

| ❌ Complexity on User | ✅ Complexity in System |
|---------------------|------------------------|
| Must type exact spelling | Fuzzy search, autocorrect, "Did you mean...?" |
| Must know the right keywords | Search understands synonyms, natural language |

### Forms

| ❌ | ✅ |
|----|-----|
| "Enter your phone: (format: +XX-XXX-XXX-XXXX)" | Auto-format as user types. Accept any format. |
| "Select your country" (195-item dropdown) | Auto-detect from IP / browser locale. Pre-select. |

### E-Commerce

| ❌ | ✅ |
|----|-----|
| "Enter coupon code" — user must find, copy, paste, hope it works | Auto-apply best available coupon at checkout |

---

## The Engineering Implication

> **Simplicity for the user requires complexity in the codebase.**

A "simple" UX often means a more complex backend. Auto-complete, smart defaults, fuzzy matching, graceful error handling — all of these add engineering complexity to reduce user complexity. **That's the tradeoff worth making.**

---

## Sources

- *Laws of UX* — https://lawsofux.com/teslers-law/
- Tesler, L. (1984). *The Law of Conservation of Complexity.*
