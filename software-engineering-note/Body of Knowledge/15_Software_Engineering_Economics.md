---
tags:
- software-engineering
- swebok
---

# Software Engineering Economics

> **Purpose:** This knowledge area applies engineering economics to software — the science of choosing how to invest limited resources for maximum value. It covers ROI analysis, estimation, decision-making processes (for-profit, nonprofit, and present-economy), lifecycle costing, and the alignment of technical decisions with business goals across the entire software product life cycle.

## Knowledge Areas

### 1. Software Engineering Economics Fundamentals
- **Proposals & Cash Flow** — A proposal is a single course of action; its cash flow stream is the complete financial picture of money in/out over time. Cash flow diagrams visualize this for comparison.
- **Time-Value of Money & Equivalence** — Money changes value over time (interest). Comparing proposals requires expressing cash flows in the same time frame using equivalence.
- **Bases for Comparison** — Present worth, future worth, annual equivalent, internal rate of return (IRR), and discounted payback period are the standard frames for comparing proposals.
- **Alternatives & Intangible Assets** — Proposals are organized into mutually exclusive alternatives (including the "do-nothing" option). Intangible assets — organizational knowledge, culture, processes — must be identified because they create hidden risks and opportunities.
- **Business Model** — Understanding who the customer is, what they value, how the organization makes money, and the underlying economic logic is essential for evaluating proposals.

### 2. The Engineering Decision-Making Process
A seven-step iterative process: (1) understand the real problem, (2) identify all reasonable technically feasible solutions, (3) define selection criteria (monetary and nonmonetary), (4) evaluate each alternative against those criteria from a consistent viewpoint, (5) select the preferred alternative using sensitivity analysis or decision-making-under-risk/uncertainty techniques when estimates are uncertain, (6) monitor the performance of the selected alternative, and (7) close the loop by comparing estimates to actual outcomes.

### 3. For-Profit Decision-Making
Techniques for organizations pursuing profit. Includes: minimum acceptable rate of return (MARR) as the opportunity-cost interest rate; economic life (the point where frozen-asset costs plus operating costs are minimized); planning horizon for comparing proposals with unequal lifetimes; replacement decisions accounting for sunk cost and salvage value; retirement decisions considering lock-in factors; and advanced considerations like inflation, depreciation, and income taxes.

### 4. Nonprofit Decision-Making
For government and nonprofit organizations. Benefit-cost analysis rejects proposals with a ratio below 1.0. Cost-effectiveness analysis comes in two forms: fixed-cost (maximize benefit within a budget) and fixed-effectiveness (minimize cost to achieve a fixed goal).

### 5. Present Economy Decision-Making
Decisions that do not involve the time-value of money. Break-even analysis finds the point where cost functions of alternatives are equal (e.g., choosing between cloud providers with different fixed/variable cost structures). Optimization analysis finds the point of minimum total cost (e.g., space-time trade-offs).

### 6. Multiple-Attribute Decision-Making
When nonmonetary criteria must be factored in. Compensatory techniques (nondimensional scaling, additive weighting, AHP, ATAM, Gilb's Impact Estimation) collapse all criteria into a single figure of merit allowing trade-offs. Non-compensatory techniques (dominance, satisficing, lexicography) treat each criterion independently without trade-offs.

### 7. Identifying and Characterizing Intangible Assets
The SIPAC (Strategic Intangible Process Assets Characterization) method: identify business processes and goals, identify intangible assets linked to them (using the 11 Generic Intangible Assets taxonomy), identify software products supporting those assets, define and measure quality/impact indicators, characterize assets into states (Warning, Replaceable, Evolving, Stable), link assets to the business model, and make decisions prioritizing products that serve the best-characterized assets.

### 8. Estimation
Estimation analytically predicts unknown quantities (size, cost, schedule) to enable decision-making. All estimates carry inherent uncertainty — they need only be good enough to lead to the right decision. Five general techniques: expert judgment (simplest, least accurate; improved by Wide Band Delphi/Planning Poker), analogy (based on similar known results), decomposition/bottom-up (breaking into estimable pieces), parametric/statistical (using validated mathematical models — most accurate and defendable), and multiple estimates (looking for convergence/divergence across techniques).

### 9. Practical Considerations
The business case consolidates cost/benefit/risk information for decision-makers. Multiple-currency analysis addresses cross-border exchange rate variation. Systems thinking provides a holistic view of the client's complex ecosystem to identify value-adding scenarios.

### 10. Related Concepts
Accounting, cost/costing (including total cost of ownership — TCO), finance, controlling, efficiency vs. effectiveness, productivity (with rework as the single largest resource consumer), product vs. service, project/program/portfolio distinctions, the software product life cycle (SPLC) vs. project life cycle, price and pricing, and prioritization.

## Essential Concepts

- **Engineering economics = the science of choice**, not the science of money — it asks "would this investment produce a higher return elsewhere?"
- **Value-based software engineering** is non-negotiable for long-term sustainability; neutral or negative value is not sustainable.
- **Every technical decision has economic implications** — build vs. buy, scope inclusion, architecture choices, refactoring vs. living with technical debt, cloud deployment strategies, risk-based testing depth.
- **Cash flow streams** are the complete financial view of a proposal; equivalence lets you compare them in the same time frame.
- **Time-value of money** is fundamental — a dollar today is worth more than a dollar tomorrow due to opportunity cost.
- **MARR (Minimum Acceptable Rate of Return)** represents the organization's opportunity cost; proposals must beat it to be viable.
- **The "do-nothing" alternative** must always be considered — sometimes the best course is to invest resources elsewhere.
- **All estimates are inherently uncertain**; use ranges, sensitivity analysis, and multiple estimation techniques (expert judgment → analogy → decomposition → parametric, in order of increasing accuracy).
- **Close the estimation loop** — compare estimates against actual outcomes to improve future accuracy (required by the Code of Ethics §3.09).
- **Intangible assets** (organizational knowledge, culture, processes) are usually hidden like an iceberg and must be explicitly characterized to avoid building software that doesn't fit the client.
- **Total Cost of Ownership (TCO)** extends far beyond development — acquire, activate, and keep running. SPLC operate-maintain-retire phases consume more resources than the SDLC.
- **Rework is the single largest resource consumer** in most software organizations; reducing it via proactive quality actions is the most effective productivity improvement.
- **For-profit vs. nonprofit vs. present-economy** decision contexts require different analytical frameworks (IRR/present worth vs. benefit-cost ratio vs. break-even/optimization).
- **Multiple-attribute decisions** use compensatory techniques (trade-offs allowed, e.g., AHP, ATAM) or non-compensatory techniques (trade-offs not allowed, e.g., dominance, lexicography) when money isn't the only criterion.
- **Economic life** is the point where frozen-asset costs + operating/maintenance costs are minimized — the optimal replacement timing.

## Tools & Techniques Mentioned

- **Cash Flow Diagrams** — visualize proposals' financial picture over time
- **Bases for Comparison** — Present Worth, Future Worth, Annual Equivalent, IRR, Discounted Payback Period
- **Benefit-Cost Analysis & Cost-Effectiveness Analysis** — for nonprofit/government decisions
- **Break-Even Analysis & Optimization Analysis** — for present-economy decisions
- **Compensatory MCDA Techniques** — Nondimensional Scaling, Additive Weighting, Analytic Hierarchy Process (AHP), ATAM (SEI Architecture Tradeoff Analysis Method), Gilb's Impact Estimation
- **Non-Compensatory MCDA Techniques** — Dominance, Satisficing, Lexicography
- **SIPAC (Strategic Intangible Process Assets Characterization)** — 7-step method for identifying, measuring, and characterizing intangible assets using the 11 Generic Intangible Assets taxonomy
- **Sensitivity Analysis, Decision Trees, Monte Carlo Analysis, Expected Value of Perfect Information** — for decision-making under risk
- **Laplace Rule, Maximin, Maximax, Hurwicz Rule, Minimax Regret Rule** — for decision-making under uncertainty
- **Estimation Techniques** — Expert Judgment, Wide Band Delphi, Planning Poker, Analogy, Decomposition (Bottom-Up), Parametric (Statistical), Multiple Estimates
- **Systems Thinking** — for holistic understanding of client ecosystems
- **Business Model Canvas / Value Proposition Design (Osterwalder)** — for mapping products to intangible assets

## Related SWEBOK Chapters

- [[09_Software_Engineering_Management]] — Project economic decisions, program/portfolio management, business case development
- [[14_Software_Engineering_Professional_Practice]] — Code of Ethics §3.09 on estimation obligations, economic impact of professional decisions
- [[07_Software_Maintenance]] — Maintenance cost dominance in SPLC; operate-maintain-retire consumes more resources than SDLC
- [[12_Software_Quality]] — Quality actions that reduce rework (the largest resource consumer), defect cost growth
- [[10_Software_Engineering_Process]] — Software life cycle models (SDLC vs. SPLC), iterative/Agile economics
- [[01_Software_Requirements]] — Requirements prioritization as an economic decision, value-based feature selection
- [[02_Software_Architecture]] — ATAM for architecture tradeoff analysis as compensatory MCDA
