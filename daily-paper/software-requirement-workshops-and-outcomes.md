---
title: "Software Requirement Workshops and Outcomes Experienced from Software Requirement Analysis Course for Undergraduate"
tags: [paper, requirements-engineering, education, active-learning, software-engineering-education]
created: 2026-09-21
source: "Longani, Singjai, Sitthithanasakul; Computing Conference 2017, 18–20 July 2017, London, UK, pp. 936–944; IEEE 978-1-5090-5443-5/17; PDF: F:/papers/Software Requirement Workshops and Outcomes Experienced from software requirement analysis course for undergraduate.pdf"
---

# Software Requirement Workshops and Outcomes Experienced from Software Requirement Analysis Course for Undergraduate

> *Paper: Pattama Longani, Apitchaka Singjai, Supavas Sitthithanasakul (Software Engineering (International), College of Arts, Media and Technology, Chiang Mai University, Thailand). "Software Requirement Workshops and Outcomes Experienced from Software Requirement Analysis Course for Undergraduate." Computing Conference 2017, 18–20 July 2017, London, UK, pp. 936–944 (IEEE). Page numbers below are the proceedings pages (936–944); PDF page = printed page − 935.*

## TL;DR

An experience report from SE321, the Software Requirement Analysis course at Chiang Mai University: the course was turned into a sequence of twelve hands-on workshops (a gift-buying simulation, a cake-description game, a Spongebob drawing exercise, dream houses, sticky-note brainstorming, real shop-owner interviews, non-functional requirement classification, prototyping and negotiation, an industry workshop, and a cross-class E-tourism case study). The pedagogical claim is simple and repeated throughout: students may not remember lecture content, but they remember activities, and the activities become anchor points for later lessons. The paper also reports an honest negative result: when students classified 53 non-functional requirements into 8 categories, fewer than half of the classifications were correct (39.39%), because students mapped keywords instead of analyzing (pp. 936–944).

## Why This Paper Matters

- **A complete, copyable activity kit.** Every activity lists its instruction, materials, and reflection, so another lecturer can lift any of them directly into a syllabus.
- **The honesty is the useful part.** The NFR classification data and the "students seem to understand, but understand nothing" observation are the findings that most course papers smooth over.
- **Practice-first evidence for active learning in requirements engineering**, a subject usually taught from textbooks (Robertson & Robertson's "Mastering the Requirements Process" is the backbone reference [2]).
- **Local provenance.** It documents the requirements course at your own university, from your professor's group, and shows how CMU's SE International program taught elicitation in 2016.

## The Course: SE321

A required third-year course in the Software Engineering (International) Program, Chiang Mai University, with Computers and Programming and Introduction to Software Engineering as prerequisites. The primary objective: students must be able to produce well-documented specifications for software development projects. In the first semester of 2016, 42 students enrolled; the class ran 3 hours per week for 3 credits and 45 hours, arranged over 15 weeks (pp. 936–937):

| Week | Focus | Activity |
|---|---|---|
| 1 | Understanding Requirement | A: the requirements process as a gift-buying simulation |
| 2 | Business Case Competition | B: student pitches of business processes, voted into projects |
| 3–6 | Inception, Elicitation, Elaboration | C–G: cake game, Spongebob, dream house, sticky-note house, real interviews |
| 7–8 | Requirement Analysis and Specification | H: non-functional classification (midterm exam) |
| 9 | Requirement Review | I: quality gateway and fit criteria |
| 10–11 | Prototyping and Negotiation | J: low- and high-fidelity prototypes, change requests |
| 13 | Requirement Reused and Management | K: industry workshop (Softsquare Group) |
| 14–15 | Case Study | L: E-tourism website for another class (final exam) |

## The Activity Toolkit

### Elicitation games

- **A. Understanding Requirement (pp. 937–938).** The lecturer plays a customer who wants to buy a present for her boyfriend; students must elicit (by asking, drawing, showing product photos), elaborate in their groups, negotiate, specify on paper, and have the lecturer validate by signing. Materials: marker pens and colored pencils. The worked example: the lecturer wants a vintage-style shirt for a boyfriend who rides a Vespa. One group returned a set without the requested shirt and was rejected, which maps directly to real projects: "a customer is always the one who accept or reject the program" (p. 938).
- **C. What a customer want? (pp. 938–939).** A student ("Win") describes the cake he wants without preparation; classmates draw it; Win then picks the one he likes best. He chose a cake that did not match his own description: he asked for maximum macarons and flowers, then picked a cake with fewer, because he also cared about things he never mentioned. The lesson, in the paper's words: "Customer may not understand himself about the things that he wants until he sees somethings." (p. 939). This is their argument for prototyping before agreement.
- **D. Draw a picture (p. 939).** Win describes a Spongebob picture while classmates draw, and everyone hears the same words yet produces different Spongebobs. The takeaways are elicitation craft, not art: word choice matters, ordering matters (describe fingers before the hand's position), small parts matter (a Spongebob needs fingers and eyebrows), listeners must focus, and analysts who know the domain will ask about the components a customer forgets to mention.

### Scoping and negotiation

- **E. Building a Dreamed House (pp. 939–940).** Project size mapped to houses: a cabin is a one-person job, while a department store needs many specialists and real management. Students draw their dream house (30 minutes) and answer planning questions. The closer: would Superman want Batman's house? Build for the user's needs, not the builder's taste.
- **F. House to Stay Together (p. 940).** Sticky-note brainstorming for a shared house: write ideas silently, stick them up, group them, discuss, negotiate. The paper's facilitation warning is specific: a talkative student dominated ("I think this one is good, everyone should choose it. Do you agree with me, right?"), quiet students stopped contributing, so the lecturer had to stop him, explain why, and switch to hand votes before giving reasons. Sticky-note workshops look easy but need an active mentor.

### Real-world practice

- **G. Interview and Present Real Case (pp. 940–941).** After teaching open- and closed-ended questions, project scope, and URS, students interviewed real business owners. The reported failures are the lessons: unprepared questions drew complaints from customers; coverage gaps forced re-interviews; busy shop owners interrupt, so students learned to make appointments when the shop is closed. Sharing each team's experience in class captures "diversity unexpected situation" (p. 941).

### Specification quality

- **H. Non-Functional Classification (pp. 941–942).** Students classify 53 non-functional requirements (from Robertson & Robertson [2]) into 8 groups: look and feel, usability and humanity, performance, operational and environmental, maintainability and support, security, cultural and political, and legal. The honest result: fewer than half were matched correctly. Overall the class scored 39.39% correct against 60.61% incorrect (Table II, p. 942); by category: performance 50.00%, cultural and political 50.00%, security 43.75%, legal 41.67%, look and feel 37.50%, usability 37.50%, operational 25.00%, maintainability 15.63%. Some items were matched correctly by every group (Ex15, Ex47) and some by no group at all (Ex2, Ex6, Ex9). The diagnosis: students used keyword matching only, so the lecturer had to teach analysis of each requirement rather than vocabulary alone.
- **I. Enhance the requirements (p. 943).** Students write the rationale and fit criteria for chosen requirements, then self-check against a quality gateway checklist covering Completeness, Traceability, Consistency, Relevancy, Correctness, Viability, Being solution-bound, Gold Plating, and Creep, followed by lecturer feedback.

### Prototyping, industry, capstone

- **J. Prototype & Negotiation (p. 943).** Low-fidelity prototypes are drawn on paper in class, missing requirements are caught, and a change request form is introduced; then students spend a week building high-fidelity prototypes, present them, and other groups suggest changes. Accepted suggestions earn points and become requirement changes, so negotiation is practiced for real.
- **K. Requirement Reused and Management Workshop (p. 943).** An industry workshop from Softsquare Group. The practical notes for lecturers: contact the company early, agree the topic and available time, expect the session to run longer than a regular class (or on a weekend), and secure university budget for the guest.
- **L. Case Study (pp. 943–944).** Students are re-clustered into new groups and must produce the requirement specification and prototype of an E-tourism website for students of the Innovation for E-tourism class, with points awarded on document quality. Real stakeholders, real negotiation, and a full review of everything taught.

## Results and Reflections

- **Activities outlast content.** "even the students cannot remember the content of the class, but students can remember class activities" (p. 944). Referring back to a past activity when teaching new content makes the new lesson easier to grasp.
- **Collaboration and questions predict learning.** Students who communicate in groups and ask lecturers questions gain more understanding than those who work alone (p. 944).
- **Frequent checking is non-negotiable.** "Many times that students seem to understand, but when the authors check their work it reflects that he/she understand nothing." (p. 944)
- The paper ends by framing itself as a deliverable: a repeatable workshop set for other requirement classes, with an open invitation to email the authors with suggestions (p. 944).

## Takeaways (synthesis)

1. **The gift-shop simulation is a full requirements-process microcosm** (inception, elicitation, elaboration, negotiation, specification, validation, management) that runs in one session with marker pens and paper.
2. **Use the cake and Spongebob games to teach the hardest truth:** users often do not know their own requirements until they see something concrete, so prototype early and treat "what they said" as a starting hypothesis.
3. **Facilitation is the hidden curriculum.** The sticky-note dominance episode shows that even a simple workshop can silently exclude quiet students unless the facilitator manages turn-taking.
4. **Treat NFR classification as an analytical skill, not vocabulary.** A 39.39% baseline with keyword matching means students need explicit training in fit criteria, quality gateways, and the reasoning behind each category.
5. **Real interviews beat role play for the messy parts:** interruptions, unprepared questions, and re-visits are exactly the experiences a classroom cannot simulate.
6. **The 15-week map is a ready-made requirements syllabus**, with a real-project backbone and workshops as the delivery vehicle.

## Memorable Quotes

> "Software requirement is the first part of software engineering life cycle and is the primary success factor for a software acceptance." (p. 936)

> "Customer may not understand himself about the things that he wants until he sees somethings." (p. 939)

> "even the students cannot remember the content of the class, but students can remember class activities" (p. 944)

> "Many times that students seem to understand, but when the authors check their work it reflects that he/she understand nothing." (p. 944)

## Related

- Source PDF: `F:/papers/Software Requirement Workshops and Outcomes Experienced from software requirement analysis course for undergraduate.pdf`
- More paper summaries in this folder: [[programming-with-abstract-data-types]], [[examining-brain-activity-while-playing-computer-games]], [[deepseek-llm-scaling-with-longtermism]], [[spec-driven-development-from-code-to-contract]], [[understanding-specification-driven-code-generation-with-llms]], [[qwen-technical-report/00_Overview]]

---

*Summary written 2026-09-21. Page numbers are the proceedings pages (936–944), footer-verified against the PDF. Quotes are verbatim, preserving the authors' wording; everything else is own-words paraphrase.*
