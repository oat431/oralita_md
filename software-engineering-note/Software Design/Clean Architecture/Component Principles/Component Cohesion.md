# Component Cohesion

> *Source: Clean Architecture by Robert C. Martin, Chapters 12–13 (pp. 88–97)*

---

## Core Principle

> **Components are units of deployment, and their cohesion is governed by three forces in constant tension: what belongs together for reuse (REP), what changes together (CCP), and what is actually used together (CRP). Finding the right balance between these three forces is the architect&rsquo;s job&mdash;and that balance shifts over the life of a project.**

A component is the smallest independently deployable unit (jar, gem, DLL, or aggregate of source files). Well-designed components remain independently developable *and* deployable. Which classes go into which component is a design decision guided by three cohesion principles&mdash;REP, CCP, and CRP&mdash;that pull in opposite directions. Architects must position their component structure within the resulting tension triangle, knowing that the right spot today is probably not the right spot next year.

### History: From Hard-Coded Addresses to Plugin Architecture

Early programs used `*200`-style origin statements to fix code at absolute memory addresses. Libraries were distributed as source decks, compiled monolithically with the application&mdash;and compile times stretched into hours. The invention of **relocatable binaries** and the **linking loader** allowed libraries and applications to be compiled and loaded separately, but link times soon grew to hours again as programs expanded (Murphy&rsquo;s law of program size: *programs grow to fill all available compile and link time*).

The next leap separated linking from loading: a dedicated **linker** produced a linked relocatable that a fast relocating loader could load in seconds. Moore&rsquo;s law eventually outpaced programmer ambition, shrinking link times to seconds by the mid-1990s. This enabled **component plugin architectures**&mdash;jars, DLLs, shared libraries that can be dynamically linked at load time&mdash;the default deployment model we use today.

---

## The Three Principles of Component Cohesion

### 1. REP &mdash; The Reuse/Release Equivalence Principle

> *The granule of reuse is the granule of release.*

Classes grouped into a component must be **releasable together** under a single version number, with proper release tracking and documentation. No one will reuse your component if it is not tracked through a release process. Conversely, you should not force a release cycle onto classes that have no reason to ship together. REP is the **inclusive** principle&mdash;it pushes components to grow larger so that a single version number covers a coherent, useful bundle of functionality. But on its own, REP is weak and hand-wavy (&ldquo;it should make sense&rdquo;); violations are detected only when users object.

---

### 2. CCP &mdash; The Common Closure Principle

> *Gather into components those classes that change for the same reasons and at the same times. Separate into different components those classes that change at different times and for different reasons.*

This is the **Single Responsibility Principle restated for components**. If a requirements change ripples through multiple components, you must revalidate and redeploy all of them. CCP says: gather classes that are closed to the same kinds of changes into one component so that most changes affect a minimal number of components. It is the component-level application of the **Open-Closed Principle (OCP)**&mdash;strategically closing components against the most likely change axes. Like REP, CCP is **inclusive**; it drives components to be larger by pulling together everything that shares a change reason.

> **Sound bite:** Gather together those things that change at the same times and for the same reasons. Separate those things that change at different times or for different reasons.

---

### 3. CRP &mdash; The Common Reuse Principle

> *Don&rsquo;t force users of a component to depend on things they don&rsquo;t need.*

Classes that are reused together belong together (e.g., a container and its iterators). But the stronger directive is about what *not* to put together: classes that are **not** tightly coupled should be separated. If component A uses only one class from component B, then every change to B&mdash;even to unrelated classes&mdash;forces revalidation and redeployment of A. CRP says: **make component dependencies total**. When you depend on a component, you should depend on *every class* in it. Otherwise you ship and revalidate more than necessary.

> This is the **Interface Segregation Principle (ISP) applied to components**: just as ISP says don&rsquo;t depend on classes with unused methods, CRP says don&rsquo;t depend on components with unused classes. CRP is the **exclusive** principle&mdash;it drives components to be *smaller*.

> **Sound bite:** Don&rsquo;t depend on things you don&rsquo;t need.

---

## The Tension Diagram

The three principles pull against each other. REP and CCP are **inclusive** (larger components); CRP is **exclusive** (smaller components). A good architect navigates the triangle of trade-offs:

```
           REP
           /\
          /  \
         /    \
        /      \
     CRP ────── CCP
```

| Corner sacrificed | What you lose |
|---|---|
| Sacrifice **REP** (bottom-left) | Reuse is hard&mdash;too many tiny components, no coherent release units |
| Sacrifice **CRP** (bottom-right) | Too many unneeded releases&mdash;change one thing, redeploy everything that depends on the component |
| Sacrifice **CCP** (top) | Too many components affected by a single change&mdash;maintenance nightmare |

No single corner is &ldquo;correct&rdquo; permanently. **Early in a project** (greenfield), develop-ability dominates&mdash;the triangle leans right (sacrifice REP, favor CCP and CRP). **As the project matures** and other teams depend on it, reuse becomes important&mdash;the triangle slides left (sacrifice CRP, favor CCP and REP). The component structure *jitters and evolves* with time and usage patterns. This is a dynamic balance, not a one-time decision.

---

## Summary Checklist

- [ ] Components are the smallest units of independent deployment and development
- [ ] REP: Only group classes into a component if they can be released and versioned together meaningfully
- [ ] CCP: Place classes that change for the same reasons in the same component (SRP for components)
- [ ] CRP: Don&rsquo;t bundle classes a user doesn&rsquo;t need&mdash;make component dependencies total (ISP for components)
- [ ] Recognize the tension: REP and CCP push components larger; CRP pushes them smaller
- [ ] Position your architecture in the tension triangle based on project maturity (early &rarr; favor CCP+CRP; mature &rarr; favor REP+CCP)
- [ ] Expect component boundaries to shift over time&mdash;this is normal and healthy

---

## Related

- [[Component Coupling]]
- [[Clean Architecture Overview]]
- [[SOLID Design Principles]]
- [[The Clean Architecture]]
- [[Architectural Independence]]
