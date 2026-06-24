# Topic 9: Discrete Probability

Probability quantifies uncertainty — how likely events are to occur. Discrete probability deals with finite sample spaces. It's the mathematical foundation for machine learning, randomized algorithms, reliability engineering, and performance modeling.

---

## 1. Probability Models

A probability model has:

| Component | Symbol | Meaning |
|-----------|--------|---------|
| Sample space | $S$ | Set of all possible outcomes |
| Event | $E \subseteq S$ | A subset of outcomes you care about |
| Probability | $P(E)$ | A number between 0 and 1 |

**Kolmogorov's Axioms:**
1. $0 \leq P(E) \leq 1$ for any event $E$
2. $P(S) = 1$ (something must happen)
3. For disjoint events: $P(E_1 \cup E_2) = P(E_1) + P(E_2)$

---

## 2. Random Variables

A **random variable** $X$ assigns a numeric value to each outcome in $S$.

| Type | Description | Example |
|------|-------------|---------|
| Discrete | Finite or countably infinite values | Number of heads in 10 coin flips |
| Continuous | Any value in an interval | Time until server responds |

### Probability Distribution

For discrete $X$, the probability distribution $p(x) = P(X = x)$ lists the probability of each value.

**Example — fair die roll:**
| $x$ | 1 | 2 | 3 | 4 | 5 | 6 |
|-----|---|---|---|---|---|---|
| $p(x)$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ |

---

## 3. Expected Value, Variance, and Standard Deviation

| Measure | Formula | Meaning |
|---------|---------|---------|
| Mean (expected value) | $\mu = E[X] = \sum x_i \cdot p(x_i)$ | "Average" outcome over many trials |
| Variance | $\sigma^2 = \sum (x_i - \mu)^2 \cdot p(x_i)$ | Spread of the distribution |
| Standard deviation | $\sigma = \sqrt{\sigma^2}$ | Same units as the data — easier to interpret |

**Example — fair die:**
- $\mu = 1\cdot\frac{1}{6} + 2\cdot\frac{1}{6} + \dots + 6\cdot\frac{1}{6} = 3.5$
- $\sigma^2 = (1-3.5)^2\cdot\frac{1}{6} + \dots + (6-3.5)^2\cdot\frac{1}{6} \approx 2.92$
- $\sigma \approx 1.71$

---

## 4. Key Rules

### Addition Rule (Disjoint Events)
$$P(A \cup B) = P(A) + P(B) \quad \text{(when $A$ and $B$ are mutually exclusive)}$$

### Addition Rule (General)
$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

### Complement Rule
$$P(\text{not } A) = 1 - P(A)$$

---

## 5. Permutations and Combinations in Probability

- **Permutations** (order matters): $P(n, r) = \frac{n!}{(n-r)!}$
- **Combinations** (order doesn't matter): $C(n, r) = \binom{n}{r} = \frac{n!}{r!(n-r)!}$

**Example:** Probability of a royal flush in 5-card poker:
$$\frac{4}{\binom{52}{5}} = \frac{4}{2,598,960} \approx 0.000154\%$$

---

## Why Probability Matters in SE

| Concept | SE Application |
|---------|---------------|
| Probability distributions | Modeling request latency, failure rates, user behavior |
| Expected value | Average-case algorithm analysis, A/B test metrics |
| Variance / Std Dev | Service reliability (SLOs), performance consistency |
| Bayes' theorem | Spam filters, recommendation systems, diagnostic tools |
| Randomized algorithms | QuickSort pivot selection, hash functions, Monte Carlo methods |
| Probability in testing | Statistical testing, fuzzing coverage probabilities, reliability modeling |
| Discrete probability | Load balancing (consistent hashing), Bloom filters (false positive rate) |

---

## Sources

- [1*] K. Rosen, *Discrete Mathematics and Its Applications*, 8th ed., McGraw-Hill, 2018.
- SWEBOK v4.0 — Chapter 17: Mathematical Foundations
