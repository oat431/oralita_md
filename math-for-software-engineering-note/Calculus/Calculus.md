---
tags:
- calculus
- math
- software-engineering
---

# Topic 12: Calculus

Calculus studies continuous change — how functions grow, shrink, and accumulate. Essential for optimization, computer graphics, physics simulation, machine learning, and understanding performance curves.

---

## 1. Limits

A **limit** describes what value a function approaches as the input approaches some point.

$$\lim_{x \to a} f(x) = L$$

Means: "$f(x)$ gets arbitrarily close to $L$ as $x$ gets close to $a$."

**Example:** $\lim_{x \to 2} (3x + 1) = 7$ — as $x \to 2$, $3x + 1 \to 7$.

**In code:** Limits formalize "as input grows..." for Big-O analysis:
$$\lim_{n \to \infty} \frac{n\log n}{n^2} = 0 \implies O(n \log n) \subset O(n^2)$$

---

## 2. Continuity

A function is **continuous** at $a$ if:
$$\lim_{x \to a} f(x) = f(a)$$

No gaps, no jumps — you can draw it without lifting the pen. Most real-world functions are continuous; discrete jumps appear at boundaries (e.g., step functions, conditionals).

---

## 3. Differentiation

The **derivative** measures the instantaneous rate of change — the slope of the tangent line.

$$f'(x) = \frac{dy}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

### Key Rules

| Rule    | Formula                                       |
| ------- | --------------------------------------------- |
| Power   | $\frac{d}{dx} x^n = nx^{n-1}$                 |
| Sum     | $\frac{d}{dx}[f + g] = f' + g'$               |
| Product | $\frac{d}{dx}[fg] = f'g + fg'$                |
| Chain   | $\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)$ |

### What Derivatives Tell You

- $f'(x) > 0$ → function is increasing
- $f'(x) < 0$ → function is decreasing
- $f'(x) = 0$ → critical point (potential max/min)
- $f''(x)$ (second derivative) → concavity, acceleration

**In code:** Gradient descent in ML uses derivatives to find minima. Backpropagation is the chain rule applied to neural networks.

---

## 4. Integration

The **integral** measures accumulation — area under a curve.

$$\int_a^b f(x) \, dx$$

### Fundamental Theorem of Calculus

Differentiation and integration are inverse operations:
$$\frac{d}{dx} \int_a^x f(t) \, dt = f(x)$$

### Types

| Type | Formula | Use |
|------|---------|-----|
| Definite integral | $\int_a^b f(x) dx$ | Exact area between $a$ and $b$ |
| Indefinite integral | $\int f(x) dx = F(x) + C$ | Antiderivative — reverse of differentiation |

**In code:** Integrals appear in:
- Physics engines (position = integral of velocity)
- Signal processing (area under frequency spectrum)
- Statistics (CDF is integral of PDF)
- Computer graphics (rendering equation solves integrals)

---

## 5. Vector Calculus

Extends calculus to 3D space. Key operations on vector fields:

| Operation | Notation | Meaning |
|-----------|----------|---------|
| Gradient | $\nabla f$ | Direction and rate of steepest increase |
| Divergence | $\nabla \cdot \mathbf{F}$ | Net flow out of a point |
| Curl | $\nabla \times \mathbf{F}$ | Rotation at a point |

**Applications:** Fluid simulation, electromagnetic field modeling, 3D graphics lighting.

---

## 6. Transcendental Functions

Functions that "transcend" algebra — cannot be expressed as finite polynomials:

| Function | Notation | Key property |
|----------|----------|-------------|
| Exponential | $e^x$ | $\frac{d}{dx} e^x = e^x$ (its own derivative) |
| Natural logarithm | $\ln x$ | $\frac{d}{dx} \ln x = \frac{1}{x}$ |
| Trigonometric | $\sin x, \cos x$ | $\frac{d}{dx}\sin x = \cos x$ |

---

## Why Calculus Matters in SE

| Concept | SE Application |
|---------|---------------|
| Derivatives | Gradient descent (ML/DL optimization), rate-of-change monitoring |
| Chain rule | Backpropagation in neural networks |
| Integrals | Physics engines, signal processing, probability CDFs |
| Limits | Algorithmic complexity (Big-O), convergence of iterative methods |
| Maxima/Minima | Optimization problems, cost function minimization |
| Vector calculus | 3D graphics, fluid simulation, robotics |
| Exponential/log | Growth modeling (user growth, Moore's law), entropy/information theory |

---

## Sources

- [2*] E.W. Cheney and D.R. Kincaid, *Numerical Mathematics and Computing*, 7th ed., Addison Wesley, 2020.
- SWEBOK v4.0 — Chapter 17: Mathematical Foundations
