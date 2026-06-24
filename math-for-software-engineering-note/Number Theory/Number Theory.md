# Topic 7: Number Theory

Number theory studies the properties of integers. It underpins cryptography, hashing, random number generation, and modular arithmetic — essential for security engineering and efficient algorithms.

---

## Types of Numbers

| Set | Symbol | Definition | Example |
|-----|--------|------------|---------|
| Natural | $\mathbb{N}$ | $\{1, 2, 3, \dots\}$ (sometimes includes 0) | 1, 42, 1000 |
| Integer | $\mathbb{Z}$ | $\{\dots, -2, -1, 0, 1, 2, \dots\}$ | -5, 0, 7 |
| Rational | $\mathbb{Q}$ | $\frac{a}{b}$ where $a,b \in \mathbb{Z}, b \neq 0$ | $\frac{1}{2}, -3, 0.75$ |
| Irrational | — | Cannot be expressed as $\frac{a}{b}$ | $\pi, \sqrt{2}, e$ |
| Real | $\mathbb{R}$ | All points on the number line | $\pi, -2, 0, \sqrt{3}$ |
| Imaginary | — | Multiples of $i = \sqrt{-1}$ | $3i, -i$ |
| Complex | $\mathbb{C}$ | $a + bi$ where $a,b \in \mathbb{R}$ | $2 + 3i$ |

---

## Divisibility

$a \mid b$ (read "$a$ divides $b$") means $b = a \cdot k$ for some integer $k$.

**Key properties:**
- If $a \mid b$ and $a \mid c$, then $a \mid (b + c)$
- If $a \mid b$, then $a \mid bc$ for any integer $c$
- If $a \mid b$ and $b \mid c$, then $a \mid c$ (transitivity)

### The Division Algorithm

For any integers $a$ and $b$ (with $b > 0$), there exist unique integers $q$ (quotient) and $r$ (remainder) such that:
$$a = bq + r, \quad 0 \leq r < b$$

---

## Modular Arithmetic

$a \bmod m$ is the remainder when $a$ is divided by $m$.

**Congruence:** $a \equiv b \pmod{m}$ means $m \mid (a - b)$ — they have the same remainder modulo $m$.

**Properties (under modulo $m$):**
- $(a + b) \bmod m = ((a \bmod m) + (b \bmod m)) \bmod m$
- $(a \cdot b) \bmod m = ((a \bmod m) \cdot (b \bmod m)) \bmod m$

**Example:** $(17 + 25) \bmod 7 = (3 + 4) \bmod 7 = 0$ ✓ ($42 \bmod 7 = 0$)

**In code:**
```python
# Clock arithmetic — hours wrap at 12
(10 + 5) % 12  # = 3 (3 PM)

# Hash table index
index = hash(key) % table_size

# Even/odd check
is_even = n % 2 == 0
```

---

## Prime Numbers

A **prime** is an integer $p > 1$ whose only divisors are $1$ and $p$.

**Fundamental Theorem of Arithmetic:** Every integer > 1 can be uniquely factored into primes (up to ordering).

**Example:** $84 = 2^2 \times 3 \times 7$

### Why Primes Matter

- **RSA encryption:** Security relies on the difficulty of factoring the product of two large primes
- **Hash functions:** Prime table sizes reduce collision patterns
- **Random number generation:** Primes used in LCG (Linear Congruential Generator) parameters

---

## Greatest Common Divisor (GCD)

$\gcd(a, b)$ is the largest integer that divides both $a$ and $b$.

**Euclidean Algorithm** (efficient GCD computation):

```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Example: gcd(48, 18) → gcd(18, 12) → gcd(12, 6) → gcd(6, 0) = 6
```

**Coprime / Relatively prime:** $\gcd(a, b) = 1$ — they share no common prime factors.

**Applications:** Simplifying fractions, finding modular inverses (Extended Euclidean Algorithm), RSA key generation.

---

## Why Number Theory Matters in SE

| Concept | SE Application |
|---------|---------------|
| Modular arithmetic | Hash tables, circular buffers, clock arithmetic, array index wrapping |
| Prime factorization | RSA public-key cryptography, Diffie-Hellman key exchange |
| GCD / Euclidean algorithm | Cryptographic key generation, fraction simplification |
| Coprime | Choosing modulus for LCG random generators, hash function parameters |
| Congruence | Checksums, error detection, parity bits |
| Modular exponentiation | Fast exponentiation for RSA encryption/decryption |

---

## Sources

- [1*] K. Rosen, *Discrete Mathematics and Its Applications*, 8th ed., McGraw-Hill, 2018.
- SWEBOK v4.0 — Chapter 17: Mathematical Foundations
