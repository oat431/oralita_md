# Testing and Embedded Architecture

> *Source: Clean Architecture by Robert C. Martin, Chapters 28–29 (pp. 192–208)*

---

## Core Principle

> **Tests are not outside the system — they are first-class system components that must be well-designed. The same architectural discipline that separates software from hardware (HAL, OSAL) also separates tests from volatile implementation details (Testing API).**

Tests follow the Dependency Rule and sit in the outermost architectural circle. In embedded systems, the same principle applies: isolate volatile hardware and OS details behind abstraction layers so the business logic — the actual software — survives hardware evolution. Both chapters converge on the same insight: what you depend on determines how long your code lives.

---

## The Test Boundary (Ch28)

### 1. Tests Are System Components, Not External Artifacts

All tests — unit, integration, acceptance, TDD, BDD — are architecturally equivalent. They are the **outermost circle** in the architecture: nothing in the system depends on them, and they always depend inward toward the code being tested. Tests are independently deployable (often to test systems only), isolated from operation, and exist solely to support development. Despite that isolation, they are no less a system component than any other — in fact, they model what all system components should be: decoupled and independently deployable.

### 2. Design for Testability — The Fragile Tests Problem

Tests that are not well-integrated into the system's design become **fragile**: a trivial production change breaks hundreds or thousands of tests. The root cause is **coupling to volatile things**. The classic example: a test suite that exercises business rules by driving the GUI. Any navigation or layout change cascades into massive test failures. This fragility has a perverse second-order effect: developers become **afraid to change the system**, making it rigid. The first rule of design for testability: **don't depend on volatile things** — test business rules without the GUI.

### 3. The Testing API — Decouple Tests from Application Structure

Create a **specific API** that tests use to verify business rules. This API should have **superpowers**: bypass security constraints, skip expensive resources (databases), force the system into specific testable states. It is a superset of the interactors and interface adapters used by the UI. The goal is deeper than just detaching from the UI — it is to **decouple the structure of the tests from the structure of the application**.

### 4. Structural Coupling — The 1:1 Test-to-Class Anti-Pattern

The most insidious form of test coupling is **structural coupling**: a test class for every production class, a test method for every production method. When any production class changes, many tests break. The Testing API hides the application structure from tests, enabling **bidirectional independent evolution**: production code can be refactored without breaking tests, and tests can grow more concrete while production code becomes more abstract and general.

### 5. Security — Isolate Dangerous Testing Capabilities

The Testing API's superpowers (bypassing security, accessing internals) are dangerous in production. If this is a concern, the Testing API and its dangerous implementation parts should be kept in a **separate, independently deployable component** — deployed only in test environments, never in production.

---

## Clean Embedded Architecture (Ch29)

> *By James Grenning*

### 6. Software vs. Firmware — The Definitions That Matter

Doug Schmidt captures the essential distinction: **"Although software does not wear out, firmware and hardware become obsolete, thereby requiring software modifications."** The accepted definitions (code in ROM, code on a device) are wrong. Firmware is not defined by **where** code lives, but by **what it depends on** and **how hard it is to change as hardware evolves**. The problem: embedded engineers write too much firmware and not enough software. Even non-embedded developers write firmware — any time SQL is embedded in business logic, or Android app logic is tangled with the Android API, that code is firmware by dependency, not by location.

### 7. The App-Titude Test — "Make It Work" Is Not Enough

Kent Beck's three activities: (1) **Make it work**, (2) **Make it right**, (3) **Make it fast**. Most embedded code stops after step 1, with micro-optimizations scattered throughout. Passing the "App-titude test" (getting it to work) is the bare minimum — it produces code where domain logic, hardware ISRs, flash storage, and button handlers are interleaved in a single file with no separation of concerns. This code is untestable off-target and has zero chance of a long useful life unless the hardware never changes.

### 8. The Target-Hardware Bottleneck

Embedded developers face constraints: limited memory, real-time deadlines, limited I/O, unconventional interfaces, sensors, and hardware co-developed with software. When code is structured without Clean Architecture, **testing can only happen on the target hardware**. If the target is the only place testing is possible, development velocity is bottlenecked by hardware availability, hardware bugs, and slow deployment cycles. **A clean embedded architecture is a testable embedded architecture.**

### 9. Three Layers and the Hardware Abstraction Layer (HAL)

Layering is the foundation:

```
┌──────────────────┐
│     Software      │  ← Business logic, long-lived
├──────────────────┤
│     Firmware      │  ← Hardware-coupled, ephemeral
├──────────────────┤
│     Hardware      │  ← Changes inevitably
└──────────────────┘
```

The **Hardware Abstraction Layer (HAL)** is the boundary between software and firmware. Its API is tailored to **software's needs**, not hardware's capabilities. Example: firmware provides `Led_TurnOn(5)` (GPIO-level), but the HAL exposes `Indicate_LowBattery()` (product-level). The HAL hides implementation details — flash memory, GPIO assignments, specific peripherals — so the software never knows them. **A successful HAL provides substitution points for off-target testing.**

### 10. The Processor Is a Detail

Vendor toolchains often extend C with non-standard keywords and register-access "global variables" — convenient but poisonous. Code using these extensions is no longer C; it won't compile for any other processor. The fix: **limit processor-specific knowledge to a processor abstraction layer (PAL)**. Use standard headers like `stdint.h` (write your own if the vendor doesn't provide one, wrapping vendor types). Anything that touches processor registers directly becomes firmware — keep it quarantined.

### 11. The Operating System Is a Detail — The OS Abstraction Layer (OSAL)

For systems with RTOS or embedded Linux/Windows, the OS itself is a volatile dependency (vendor change, licensing cost shift, capability mismatch). The **Operating System Abstraction Layer (OSAL)** isolates software from the OS. OSAL provides a defined interface: message-passing mechanisms, concurrency primitives, and OS services tailored to the application. When you switch RTOS vendors, you rewrite the OSAL — not the application. The OSAL also creates test seams: software can be tested **off-target and off-OS**.

### 12. Programming to Interfaces and Substitutability

Layered architecture works because modules interact through interfaces. A clean embedded architecture is testable **within each layer** because every interface provides a substitution point. Rule of thumb: use header files as interface definitions, but **limit headers to function declarations and only the constants/structs that callers need**. Do not expose implementation details in the interface — they create unwanted dependencies and multiply the blast radius of changes.

### 13. DRY Conditional Compilation — Kill the `#ifdef` Sprawl

Embedded C/C++ code often abuses `#ifdef BOARD_V2`, `#ifdef TARGET_X`, repeated thousands of times — a severe violation of the Don't Repeat Yourself (DRY) principle. The alternative: let the HAL hide hardware type as a detail. Use the linker or runtime binding to connect software to the correct hardware implementation instead of scattering conditional compilation throughout the codebase.

---

## Summary Checklist

- [ ] Are tests treated as first-class system components, not external afterthoughts?
- [ ] Do tests follow the Dependency Rule (inward dependency only)?
- [ ] Is there a Testing API that decouples tests from application structure?
- [ ] Are tests free from structural coupling (no 1:1 test-to-production-class mapping)?
- [ ] Are dangerous Testing API capabilities isolated in a separate, non-production component?
- [ ] Is the codebase clearly separated into software (long-lived) and firmware (hardware-bound)?
- [ ] Can business logic be tested off-target without hardware?
- [ ] Does a Hardware Abstraction Layer (HAL) exist with product-level (not GPIO-level) APIs?
- [ ] Are processor-specific C extensions confined to a processor abstraction layer (PAL)?
- [ ] Does an OS Abstraction Layer (OSAL) insulate software from RTOS/OS dependencies?
- [ ] Are header files limited to caller-facing declarations — no implementation details leaked?
- [ ] Is `#ifdef` for hardware variants replaced with linker/runtime binding through the HAL?

---

## Related

- [[Clean Architecture Overview]]
- [[The Clean Architecture]]
- [[SOLID Design Principles]]
- [[Presenters and Humble Objects]]
- [[Main Component and Services]]
- [[Boundaries]]
