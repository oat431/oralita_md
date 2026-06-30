---
tags:
- book-summary
- professionalism
- software-engineering
- uncle-bob
---

# Mentoring & Craftsmanship

> *Source: The Clean Coder by Robert C. Martin, Chapter 14 (pp. 173–185)*

---

## Core Principle

> **The discipline, practice, and skill of being a software craftsman cannot be taught by universities — they are acquired through years of personal tutelage, mentoring, and supervised practice. It falls to industry practitioners, not academia, to guide the next generation of developers to professional maturity.**

---

## The Rules

### 1. The Failure of CS Education

University computer science programs suffer from two fundamental problems:

- **Graduates can avoid programming entirely.** Martin recounts interviewing a master's candidate in CS who admitted she "didn't really write code" and had taken no programming courses. While extreme, this is symptomatic of a system that allows students to earn diplomas without practical competence.

- **Even strong programs don't prepare graduates for industry.** What you learn in school and what you find on the job are often very different. This is true across disciplines, but software suffers acutely because CS curricula focus on theory while industry demands disciplined practice.

The graduates who *do* succeed share a common trait: **they taught themselves to program before university and continued teaching themselves despite it.** Their competence came from self-directed learning and mentorship outside the classroom, not from the degree program itself.

### 2. The Mentoring Model

Martin draws on his own formative experiences to illustrate that mentoring takes many forms — not just the traditional master-apprentice relationship:

- **Written mentorship** — At age twelve, Martin learned boolean algebra and finite state machines from the manual that came with his Digi-Comp I kit. The authors, though he never knew their names, wrote a treatise accessible to a child that connected mathematical theory to the pragmatics of the machine. This was mentorship through the written word.

- **Observational mentorship** — In high school, Martin watched technicians and teachers operate an ECP-18 educational computer. Though they largely ignored him, he absorbed instruction codes, memory architecture, and debugging techniques simply by observing. He learned that even a correct program can have profound usability flaws (a mysterious five-second pause before the final digit).

- **Unconventional mentors** — A neighbor who gave him telephone relays, a ham operator who taught him to use a multimeter, an office supply store owner who let him "play" with an expensive programmable calculator, and DEC sales offices that allowed access to PDP-8 and PDP-10 machines.

- **Direct mentorship** — Big Jim Carlin, a BAL programmer, saved Martin from being fired from his first job by helping him debug a Cobol program. He taught Martin to read core dumps, format code with blank lines and comments, and gave him his first push toward craftsmanship.

Despite these experiences, Martin laments that for most of his early career he was the senior person in the room. There was no role model to teach him professional behavior or values — those he had to learn the hard way.

### 3. The Apprenticeship Path

The software industry should adopt a structured progression modeled on the medical profession:

| Stage | Description |
|-------|-------------|
| **Apprentice / Intern** | Recent graduates with **no autonomy**. Closely supervised by journeymen through intense pair-programming. They provide assistance while learning design principles, patterns, TDD, refactoring, estimation, and professional disciplines. Duration: approximately **one year**. |
| **Journeyman** | Trained, competent, energetic programmers (~5 years average experience). They work well in teams, may lead small teams, and are knowledgeable about current technology but lack breadth across diverse systems. Their work is supervised by masters or senior journeymen, transitioning from close scrutiny to peer review as experience grows. |
| **Master** | Programmers with **10+ years** of experience across multiple systems, languages, and operating systems. They lead and coordinate multiple teams, are proficient architects and designers, and maintain their technical edge through reading, studying, practicing, and teaching. Masters hold technical responsibility for projects. (Think "Scotty.") |

**The reality gap:** Most companies already have a hierarchy — graduates supervised by team leads, supervised by project leads. But this supervision is almost never *technical*. Programmers advance through the ranks simply because "that's what you do with programmers," not because anyone is teaching professional values or technical acumen. What's missing is the **responsibility of the elders to teach the young**.

The medical profession requires internship, residency, and fellowship — years of supervised practice before board certification. When the stakes are high (and software now runs civilization — bank balances, car brakes, medical devices, communications), we should demand no less.

### 4. Craftsmanship as Identity

**Craftsmanship** is the *mindset* held by craftsmen — a meme containing values, disciplines, techniques, attitudes, and answers.

A craftsman:
- Works quickly but without rushing
- Provides reasonable estimates and meets commitments
- Knows when to say no, but tries hard to say yes
- Embodies skill, quality, experience, and competence
- Is, fundamentally, a *professional*

**How the meme spreads:** Craftsmanship is a contagion — a "mental virus" transmitted from person to person. It is taught by elders to the young, exchanged between peers, and relearned as elders observe the young. **It cannot be imposed through argument, data, or case studies.** The acceptance of the craftsmanship meme is an emotional decision, not a rational one.

**The only effective strategy:** Become a craftsman yourself. Act as a role model. Make the meme observable. Let your craftsmanship show, and let the contagion do the rest.

---

## Summary Checklist
- [ ] Recognize that CS degrees alone do not produce professional programmers — self-teaching and mentorship fill the gap
- [ ] Seek out mentors in whatever form they appear: authors, colleagues, open-source contributors, or senior developers willing to review your work
- [ ] Embrace the apprentice/journeyman/master progression as a framework for career growth
- [ ] If you are experienced, take responsibility for teaching the young — technical supervision is the missing piece in most organizations
- [ ] Cultivate the craftsmanship mindset: skill, quality, reasonable estimates, the courage to say no, and relentless professionalism
- [ ] Spread the craftsmanship meme by being an observable role model, not by argument

---

## Related
- [[Professionalism]]
- [[Practicing]]
- [[Collaboration]]
- [[Teams and Projects]]
