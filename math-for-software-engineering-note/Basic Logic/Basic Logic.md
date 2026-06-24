# Topic 1: Basic Logic

Logic is the foundation of all mathematical reasoning and all automated reasoning. The rules of logic specify the meaning of mathematical statements — they help us determine what follows from what. In software engineering, logic is directly translated into conditional expressions, loop guards, and formal specifications.

---

## 1. Propositional Logic

A **proposition** is a declarative statement that is either **true (T)** or **false (F)**, but not both.

**Examples:**

| Statement | Truth Value |
| ----------- | ------------ |
| "The sky is blue." | T (on a clear day) |
| "$2 + 2 = 4$" | T |
| "$2 + 2 = 5$" | F |
| "What time is it?" | Not a proposition (question) |
| "$x + 1 = 2$" | Not a proposition (depends on $x$) |

### Logical Operators (Connectives)

| Operator | Symbol(s) | Read as | Truth Rule |
|----------|-----------|---------|------------|
| Negation | $\neg P$, !P | "not P" | Flips truth value |
| Conjunction | $P \land Q$, P && Q | "P and Q" | True only when both are true |
| Disjunction | $P \lor Q$, P \|\| Q | "P or Q" | True when at least one is true |
| Implication | $P \rightarrow Q$ | "if P then Q" | False only when P is true and Q is false |
| Biconditional | $P \leftrightarrow Q$ | "P if and only if Q" | True when both have same truth value |

### Truth Tables

Exhaustive listing of all possible truth values:

**Negation:**

| $P$ | $\neg P$ |
|-----|----------|
| T | F |
| F | T |

**Conjunction:**

| $P$ | $Q$ | $P \land Q$ |
|-----|-----|------------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

**Disjunction:**

| $P$ | $Q$ | $P \lor Q$ |
|-----|-----|------------|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**Implication** (the trickiest — "false implies anything"):

| $P$ | $Q$ | $P \rightarrow Q$ |
|-----|-----|------------------|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

⚠️ **Key insight:** $P \rightarrow Q$ is equivalent to $\neg P \lor Q$. When the premise is false, the implication is true regardless — this is why "if the moon is made of cheese, then 2+2=4" is technically true.

**Biconditional:**

| $P$ | $Q$ | $P \leftrightarrow Q$ |
|-----|-----|----------------------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | T |

### Special Proposition Types

| Type | Definition | Example |
|------|------------|---------|
| Tautology | Always true | $P \lor \neg P$ |
| Contradiction | Always false | $P \land \neg P$ |
| Contingency | Sometimes true, sometimes false | $P \land Q$ |

### Logical Equivalences

Two propositions are **logically equivalent** ($\equiv$) if they have identical truth tables.

| Law | Equivalence |
|-----|------------|
| Double Negation | $\neg(\neg P) \equiv P$ |
| De Morgan's (AND) | $\neg(P \land Q) \equiv \neg P \lor \neg Q$ |
| De Morgan's (OR) | $\neg(P \lor Q) \equiv \neg P \land \neg Q$ |
| Commutative | $P \land Q \equiv Q \land P$, $P \lor Q \equiv Q \lor P$ |
| Associative | $(P \land Q) \land R \equiv P \land (Q \land R)$ |
| Distributive | $P \land (Q \lor R) \equiv (P \land Q) \lor (P \land R)$ |
| Implication | $P \rightarrow Q \equiv \neg P \lor Q$ |

**In code — De Morgan's laws in action:**
```python
# These two are equivalent:
if not (is_admin and is_active):
    deny()

if not is_admin or not is_active:
    deny()

# These two are equivalent:
if not (is_guest or is_banned):
    allow()

if not is_guest and not is_banned:
    allow()
```

---

## 2. Predicate Logic

Predicate logic extends propositional logic to handle statements about **objects** and their **properties/relationships** — it lets us say things about "all" or "some" without naming each one individually.

### Predicates

A **predicate** $P(x)$ is a statement template with variables. It becomes a proposition when the variable is assigned a value.

| Expression | Meaning |
|-----------|---------|
| $P(x)$: "$x$ is red" | Template — not yet true or false |
| $P(\text{rose})$ | "The rose is red" — now a proposition (T or F) |
| $Q(x, y)$: "$x > y$" | Two-variable predicate |
| $Q(5, 3)$ | "$5 > 3$" — T |

### Quantifiers

Quantifiers let us make claims about entire collections without enumerating every element.

| Quantifier | Symbol | Read as | True when... |
|-----------|--------|---------|-------------|
| Universal | $\forall x \; P(x)$ | "for all $x$, $P(x)$" | $P(x)$ is true for **every** $x$ in the domain |
| Existential | $\exists x \; P(x)$ | "there exists $x$ such that $P(x)$" | $P(x)$ is true for **at least one** $x$ in the domain |

**Examples:**
- $\forall x \; \text{Tiger}(x) \rightarrow \text{Mammal}(x)$ — "All tigers are mammals." (T)
- $\exists x \; \text{Tiger}(x) \land \text{ManEater}(x)$ — "Some tigers are man-eaters." (T)
- $\forall x \in \mathbb{N} \; x \geq 0$ — "Every natural number is non-negative." (T)
- $\exists x \in \mathbb{Z} \; x^2 = 4$ — "There is an integer whose square is 4." (T: $x=2$ or $x=-2$)

### Negating Quantifiers

| Original | Negation | Mnemonic |
|----------|----------|----------|
| $\neg(\forall x \; P(x))$ | $\exists x \; \neg P(x)$ | "Not all" = "There exists one that isn't" |
| $\neg(\exists x \; P(x))$ | $\forall x \; \neg P(x)$ | "No such thing exists" = "Everything is not that" |

**Example:** "Not all birds can fly" $\equiv$ "There exists a bird that cannot fly" (penguin 🐧).

### Nested Quantifiers

Order matters with mixed quantifiers:

- $\forall x \; \exists y \; (x + y = 0)$ — "For every integer $x$, there exists a $y$ (namely $-x$)" — TRUE
- $\exists y \; \forall x \; (x + y = 0)$ — "There is a single $y$ that works for every $x$" — FALSE

**In code:** Nested quantifiers mirror nested loops. $\forall x \; \exists y$ is "for each $x$, I can find a $y$" — different $y$ per $x$. $\exists y \; \forall x$ is "one $y$ fits all $x$."

---

## Why Logic Matters in SE

| Concept | SE Application |
|---------|---------------|
| Truth tables | Exhaustive test case design, decision table testing |
| Logical equivalences | Refactoring conditionals, simplifying boolean expressions |
| De Morgan's laws | Negating complex conditions (`if (!(A && B))` → `if (!A \|\| !B)`) |
| $\rightarrow$ (implication) | Preconditions → postconditions, guard clauses |
| $\forall$ (universal) | Loop invariants, type system constraints ("all values of type T...") |
| $\exists$ (existential) | Test case existence, input validation |
| Predicate logic | Formal specifications, database queries (SQL WHERE clauses), pattern matching |
| Tautology/contradiction | Dead code detection (contradiction = unreachable), redundant check removal (tautology) |

---

## Sources

- [1*] K. Rosen, *Discrete Mathematics and Its Applications*, 8th ed., McGraw-Hill, 2018.
- SWEBOK v4.0 — Chapter 17: Mathematical Foundations
