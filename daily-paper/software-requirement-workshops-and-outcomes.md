---
title: "Software Requirement Workshops and Outcomes Experienced from Software Requirement Analysis Course for Undergraduate"
tags: [paper, requirements-engineering, education, active-learning, software-engineering-education]
created: 2026-09-21
revised: 2026-09-29
source: "Longani, Singjai, Sitthithanasakul; Computing Conference 2017, 18–20 July 2017, London, UK, pp. 936–944; IEEE 978-1-5090-5443-5/17; PDF: F:/papers/Software Requirement Workshops and Outcomes Experienced from software requirement analysis course for undergraduate.pdf"
---

# Software Requirement Workshops and Outcomes Experienced from Software Requirement Analysis Course for Undergraduate

> *Paper: Pattama Longani, Apitchaka Singjai, Supavas Sitthithanasakul (Software Engineering (International), College of Arts, Media and Technology, Chiang Mai University, Thailand). "Software Requirement Workshops and Outcomes Experienced from Software Requirement Analysis Course for Undergraduate." Computing Conference 2017, 18–20 July 2017, London, UK, pp. 936–944 (IEEE). Page numbers below are the proceedings pages (936–944); PDF page = printed page − 935. Plain-language body first; the dense detail (the 15-week course map, all twelve activities, the classification data, verbatim quotes) lives in the Appendix at the end.*

## What Is This Paper, In Plain Words

This one is personal: it was written at your own university. The Software Engineering (International) program at Chiang Mai University describes how it runs SE321, the required third-year course on software requirement analysis, and the authors are your professor's teaching group.

The paper's core belief is simple. Learning to gather software requirements is like learning to ride a bicycle: nobody gets there by listening to a lecture about balance. So the instructors turned a whole semester into a string of twelve hands-on workshops, and used the workshops as the teaching material itself. Forty-two students went through the course in the first semester of 2016, three hours a week for fifteen weeks.

Here is the flavor of what those students actually did. One week the lecturer plays a picky customer who wants to buy a present for her boyfriend, and each student team has to interview her, sketch ideas, negotiate, write the requirements down, and get her signature, exactly like a real software project in miniature. Another week a student named Win describes a cake he wants while classmates draw it, then picks his favorite; the punchline is that Win picks a cake that contradicts his own description, because people want things they never say out loud. Another week everyone hears the same description of Spongebob and produces wildly different Spongebobs, which teaches that word choice, ordering, and small details decide whether a requirement survives translation. Students design dream houses on paper to learn project sizing, brainstorm a shared house with sticky notes to learn facilitation, and then leave the classroom to interview real shop owners, where they get interrupted, underprepared, and sent back for second visits. Later they classify non-functional requirements, check their own work against a quality gateway checklist, build paper and software prototypes and negotiate change requests for points, attend an industry workshop run by Softsquare Group, and finish with a capstone: write the requirement specification and prototype for an E-tourism website whose real clients are students from another class.

Two findings run through the paper. The first is the pedagogical claim, repeated at the end: students may forget the lecture content, but they remember the activities, so every new lesson is hung on an activity the class already lived through. The second is an honest negative result that most course papers bury. When students sorted 53 non-functional requirements into 8 categories, fewer than half the classifications were correct (39.39%), because students were matching keywords instead of analyzing meaning. The paper reports this plainly, per category and per requirement, and treats it as the reason the lecturer had to teach analysis explicitly rather than vocabulary.

## The Key Ideas, In Normal Words

**1. Activities are memory anchors.** The authors observed that when a new lecture refers back to an activity students did weeks earlier, the students visibly remember what happened, and the new content lands faster. The workshop is not a break from teaching; it is the storage format for the teaching.

**2. Customers do not know what they want until they see something.** The cake game is the proof: Win asked for maximum macarons and flowers, then chose a cake with fewer, because he also cared about things he never mentioned. The practical conclusion is to prototype early and treat what the customer said as a starting hypothesis, not a contract.

**3. Facilitation is the hidden curriculum.** During the sticky-note house workshop, one talkative student steamrolled the group ("I think this one is good, everyone should choose it. Do you agree with me, right?", p. 940), and the quiet students stopped contributing. The lecturer had to stop him, explain why, and change the voting procedure. A workshop that looks easy on paper silently fails without an active mentor.

**4. The messy parts cannot be simulated.** The real shop-owner interviews produced failures no role play can: unprepared questions that drew customer complaints, coverage gaps that forced re-interviews, and busy owners who get interrupted by their own customers. The students' workaround, booking appointments when the shop is closed, is the kind of lesson only reality teaches.

**5. Classification is an analytical skill, not vocabulary.** The 39.39% result showed students mapping keywords to categories. Some requirements were classified correctly by every group, some by no group at all. The fix was to teach students to reason about each requirement, which is also what the later quality gateway and fit criteria workshop drills.

**6. End with a real client.** The final case study re-clusters students into new groups and pairs each with students from the Innovation for E-tourism class, who genuinely want a travel website. Real stakeholders, real negotiation, graded on document quality: the whole course in one exercise.

## Why You Should Care

1. **It is your own department's teaching, documented.** If you ever want to know how CMU's SE International program taught requirements elicitation in 2016, or want to talk to the people who designed your curriculum, this is the primary source.
2. **It is a complete, copyable activity kit.** Every one of the twelve workshops lists its instruction, materials, and reflection, so a lecturer (or a team lead running an internal workshop) can lift any activity directly into a syllabus with marker pens, sticky notes, and paper.
3. **The honesty is the useful part.** The NFR classification data and the finding that students "seem to understand" until the authors check their work are exactly the findings that most course papers smooth over. They tell you what to test for after any training you run.
4. **It is practice-first evidence for active learning in requirements engineering**, a subject usually taught from textbooks (Robertson & Robertson's *Mastering the Requirements Process* is the backbone reference).

---

# Appendix: The Dense Details

> *Everything below is the reference layer: the course map, all twelve activities with materials and reflections, the classification data, and verbatim quotes, all page-cited to the proceedings (936–944). Read the body above first.*

## A. TL;DR

An experience report from SE321, the Software Requirement Analysis course at Chiang Mai University: the course was turned into a sequence of twelve hands-on workshops (a gift-buying simulation, a business case competition, a cake-description game, a Spongebob drawing exercise, dream houses, sticky-note brainstorming, real shop-owner interviews, non-functional requirement classification, quality gateway checking, prototyping and negotiation, an industry workshop, and a cross-class E-tourism case study). The pedagogical claim is simple and repeated throughout: students may not remember lecture content, but they remember activities, and the activities become anchor points for later lessons. The paper also reports an honest negative result: when students classified 53 non-functional requirements into 8 categories, fewer than half of the classifications were correct (39.39%), because students mapped keywords instead of analyzing (pp. 936–944).

## B. The Course: SE321

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

Course objectives beyond the primary one (p. 936): explain the requirements process; use methodologies, techniques, and tools appropriate to each requirement activity; find and elicit requirements using formal and informal techniques; organize and prioritize requirements; negotiate among stakeholders and handle conflicts; specify requirements and fit criteria; reuse and manage requirements.

## C. The Activity Toolkit

### Elicitation games

- **A. Understanding Requirement (pp. 937–938).** The lecturer plays a customer who wants to buy a present for her boyfriend; students must elicit (by asking, drawing, showing product photos), elaborate in their groups, negotiate, specify on paper, and have the lecturer validate by signing. All seven requirement processes are covered: inception, elicitation, elaboration, negotiation, specification, validation, and management. Materials: marker pens ("Maji pen" in the paper) and colored pencils. The worked example: the lecturer wants a vintage-style shirt for a boyfriend who rides a Vespa. The first group returned a vintage shirt with a t-shirt and was accepted within budget; the second added a vest, flat cap, and optional Oxford leather shoes and was also accepted; the last group returned a jeans jacket with no shirt and was rejected, which maps directly to real projects: "a customer is always the one who accept or reject the program" (p. 938).
- **B. Business Case Competition (p. 938).** Each group presents a business process from a given topic list: coffee shop, bank, restaurant, airport, pharmacy, clothing store, cinema, dog grooming shop, and car rental shop. Students then choose the three business cases they like best (the chosen ones, used later in Activity I, were coffee shop, dog grooming shop, and cinema), because student interest is a factor in efficient learning. The lecturer also photographs presentations and coaches delivery (e.g., do not ignore the audience while reading).
- **C. What a customer want? (pp. 938–939).** A student ("Win") describes the cake he wants without preparation; classmates draw it; Win then picks the one he likes best. He wanted a double layer cake with macarons and flowers as much as possible and the message "I love you my angle WIN." He chose a cake that did not match his own description: he asked for maximum macarons and flowers, then picked a cake with fewer, because he also cared about things he never mentioned. The lesson, in the paper's words: "Customer may not understand himself about the things that he wants until he sees somethings." (p. 939). This is their argument for submitting a prototype to a customer before making an agreement to build the real program.
- **D. Draw a picture (p. 939).** Win describes a Spongebob picture (hidden from the class) while classmates draw and may ask questions, and everyone hears the same words yet produces different Spongebobs. The takeaways are elicitation craft, not art: word choice matters (different description, different meaning, incorrect requirement); ordering matters (describe fingers before the hand's position); small parts matter (a Spongebob cannot look perfect without fingers and eyebrows); listeners must focus; and analysts who know the domain (or have seen a Spongebob before) will ask about the components a customer forgets to mention.

### Scoping and negotiation

- **E. Building a Dreamed House (pp. 939–940).** Project size mapped to houses, following the textbook's comparison of project sizes to three animals, "a rabbit, a horse, and an elephant" (p. 939): resources, cost, and time differ per size. Because students' prior knowledge can help learning, the authors use houses, which students are more familiar with. A cabin is a one-person job (John alone, or John and Mary in a day), while a department store takes one person years, so finishing within a year needs people with different career paths plus real management. Students draw their dream house (30 minutes) and answer planning questions: how does it look, how to build it, how many people to hire, what are their responsibilities. The closer: would Superman want Batman's house, and would he use it? Build for the user's needs, not the builder's taste.
- **F. House to Stay Together (p. 940).** Sticky-note brainstorming for a shared house: everyone gets sticky notes, writes ideas silently without talking, sticks them on a board, groups them (students produced categories: pets, plants, facility, material, rooms), discusses, and negotiates accept/reject. The paper's facilitation warning is specific: a talkative student dominated ("I think this one is good, everyone should choose it. Do you agree with me, right?"), laconic students lost their chance to speak and others feared opposing a friend, so requirements would not meet the team's real need. The lecturer had to stop him, explain why to everybody, and switch to hand votes before giving reasons. Sticky-note workshops look easy but need an active mentor watching and advising.

### Real-world practice

- **G. Interview and Present Real Case (pp. 940–941).** After teaching open- and closed-ended questions, project scope, and URS (user requirement specification), and showing that an interviewer must prepare questions and verify they cover everything that can be a requirement, students went out and interviewed real business owners, wrote the URS, then shared their experience in class while lecturers and other students asked questions. The reported failures are the lessons: unprepared questions drew complaints from customers; coverage gaps forced re-interviews; busy shop owners get interrupted by their own customers, so students learned to make appointments when the shop is closed or outside the shop. Sharing each team's experience in class captures "diversity unexpected situation" (p. 941).

### Specification quality

- **H. Non-Functional Classification (pp. 941–942).** Students classify 53 non-functional requirements (taken from Robertson & Robertson [2], Table I) into 8 groups: look and feel, usability and humanity, performance, operational and environmental, maintainability and support, security, cultural and political, and legal. Each group gets a different sticky-note color, writes each requirement on a note, and sticks it on the wall under its category; every group then presents its reasoning and the class reaches consensus per requirement. Category ranges in Table I: Ex1–3 look and feel, Ex4–13 usability and humanity, Ex14–28 performance, Ex29–36 operational and environmental, Ex37–40 maintainability and support, Ex41–46 security, Ex47–50 cultural and political, Ex51–53 legal. The honest result: fewer than half were matched correctly. Overall the class scored 39.39% correct against 60.61% incorrect (Table II, p. 942); by category: performance 50.00% (15 req), cultural and political 50.00% (4 req), security 43.75% (6 req), legal 41.67% (3 req), look and feel 37.50% (3 req), usability and humanity 37.50% (10 req), operational and environmental 25.00% (8 req), maintainability and support 15.63% (4 req). Some items were matched correctly by every group (Ex15, Ex47, both 100%) and some by no group at all (Ex2, Ex6, Ex9, Ex11, Ex16, Ex17, Ex28, Ex39, Ex50 at 0%). The authors' diagnosis: the requirements came from business areas unfamiliar to software engineering students, and many students used keyword matching only, so the lecturer had to teach analysis of each requirement rather than vocabulary alone. The midterm exam fell at the end of week 8; results after midterm were not yet available at writing time (p. 943).
- **I. Enhance the requirements (p. 943).** Students (8 groups across the 3 chosen projects: coffee shop, dog grooming shop, cinema) receive chosen requirements from their earlier documents and must write the rationale and fit criteria for each, then self-check against a quality gateway checklist (Table III) covering Completeness, Traceability, Consistency, Relevancy, Correctness, Viability, Being solution-bound, Gold Plating, and Creep, rewrite better requirements, and receive lecturer feedback. The activity also makes students review team members' work again. Materials: checklist form, pen, paper.

### Prototyping, industry, capstone

- **J. Prototype & Negotiation (p. 943).** Low-fidelity prototypes are drawn with pen and paper in class; students may find missing requirements, and the lecturer introduces a change request form for adding or changing requirements. Then students get a suggested high-fidelity prototyping program and a week to use it, present the result to other groups, and other groups suggest changes. If the presenting group accepts a suggestion, the suggesting group earns points and the accepting group must write a requirement change, so negotiation to accept or reject requirements is practiced for real. Materials: pen, paper.
- **K. Requirement Reused and Management Workshop (p. 943).** An industry workshop from Softsquare Group giving students real cases and motivation from a company. The practical notes for lecturers: contact the company early, inform them of the topic and available time, expect the session to run longer than a regular class (or to be held on a weekend), and secure university budget for facilitating the guest lecturer. Materials: company contact, budgets.
- **L. Case Study (pp. 943–944).** Students are re-clustered into new groups (so individual points are more independent from group points) and each group is paired with a group of students from the Innovation for E-tourism class, who are learning tourism business processes and want a travel website. SE321 students must use everything they learned to elicit requirements and produce the requirement specification document and prototype of the E-tourism website, with points awarded on document quality. Real stakeholders, real negotiation, and a full review of everything taught. This is the final exam. Materials: pen, paper, prototype program.

## D. Results and Reflections (Section IV, p. 944)

- **Activities outlast content.** "even the students cannot remember the content of the class, but students can remember class activities" (p. 944). When lecturers talk back to an activity from a previous class, students seem to remember what happened at that time, which makes the content of the new class easier to understand.
- **Collaboration and questions predict learning.** Students who like to communicate with others in the group and ask questions to lecturers gain more understanding than the ones who like working alone (p. 944).
- **Frequent checking is non-negotiable.** "Many times that students seem to understand, but when the authors check their work it reflects that he/she understand nothing." (p. 944) Lecturers must check student work as frequently as possible and care very much about feedback.
- The paper ends by framing itself as a deliverable: the authors believe active learning, project-based learning, collaborative work, teacher reflection, and industry inspiration help students understand requirement eliciting, and they hope their repeatable workshop will increase the efficiency of other requirement classes, with an open invitation to email the authors with suggestions (p. 944).

## E. Takeaways (synthesis)

1. **The gift-shop simulation is a full requirements-process microcosm** (inception, elicitation, elaboration, negotiation, specification, validation, management) that runs in one session with marker pens and paper.
2. **Use the cake and Spongebob games to teach the hardest truth:** users often do not know their own requirements until they see something concrete, so prototype early and treat what they said as a starting hypothesis.
3. **Facilitation is the hidden curriculum.** The sticky-note dominance episode shows that even a simple workshop can silently exclude quiet students unless the facilitator manages turn-taking.
4. **Treat NFR classification as an analytical skill, not vocabulary.** A 39.39% baseline with keyword matching means students need explicit training in fit criteria, quality gateways, and the reasoning behind each category.
5. **Real interviews beat role play for the messy parts:** interruptions, unprepared questions, and re-visits are exactly the experiences a classroom cannot simulate.
6. **The 15-week map is a ready-made requirements syllabus**, with a real-project backbone and workshops as the delivery vehicle.

## F. Memorable Quotes

> "Software requirement is the first part of software engineering life cycle and is the primary success factor for a software acceptance." (p. 936)

> "a customer is always the one who accept or reject the program" (p. 938)

> "Customer may not understand himself about the things that he wants until he sees somethings." (p. 939)

> "I think this one is good, everyone should choose it. Do you agree with me, right?" (p. 940)

> "diversity unexpected situation" (p. 941)

> "even the students cannot remember the content of the class, but students can remember class activities" (p. 944)

> "Many times that students seem to understand, but when the authors check their work it reflects that he/she understand nothing." (p. 944)

## Related

- Source PDF: `F:/papers/Software Requirement Workshops and Outcomes Experienced from software requirement analysis course for undergraduate.pdf`

---

*Summary written 2026-09-21, restructured 2026-09-29 into plain-language body + appendix format. Page numbers are the proceedings pages (936–944), footer-verified against the PDF. Quotes are verbatim, preserving the authors' wording; everything else is own-words paraphrase.*
