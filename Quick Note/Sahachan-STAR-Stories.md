# STAR Stories Portfolio — Sahachan Tippimwong

**Created:** 2026-08-11  
**Purpose:** Reusable behavioral interview stories  
**Target:** 8-12 stories covering key behavioral dimensions

---

## Story 1: The CP All Warehouse Migration (Technical Leadership)

**Dimensions covered:** Technical leadership, Legacy modernization, Team coordination, Communication with stakeholders, Onboarding/mentoring

**Estimated answer time:** 3-4 minutes (spoken)

---

### The STAR Structure

**Situation (30 seconds):**

> In 2023, I joined Gosoft Thailand's resource pool team — we were essentially an internal consulting group that CP All would pull from for high-priority projects. I was assigned to the migration of CP All's warehouse management system — the backend system that runs 7-Eleven stores across Thailand.
>
> The legacy system was built in 2004 on Java Struts, running on IBM DB2 with stored procedures everywhere. It had zero test coverage, deployment took a full day, and it was becoming impossible to maintain. The company decided to migrate to Spring Boot 3 microservices on MySQL, and this was a massive 50+ person project.

**Task (15 seconds):**

> I served as a temporary team lead and project coordinator for the backend team of 20+ developers. My job was to coordinate daily progress with service owners, onboard new team members, and personally handle the most technically complex modules — particularly the reporting system.

**Action (2 minutes — the longest section):**

> The migration followed a strangler fig pattern — we replaced the legacy system module by module, with each module going through development, testing, and UAT before cutover.
>
> My most challenging module was the reporting system. It relied on JasperSoft and had deep dependencies on IBM DB2 stored procedures with complex business logic that nobody had documented. I had to go on-site to learn JasperSoft, then systematically reverse-engineer over 10 stored procedures by reading the old code line by line and rebuilding the logic using Spring Boot's ORM layer.
>
> I also made a critical decision: migrate the database from IBM DB2 to MySQL. I validated every report output against the old version to ensure the numbers matched exactly — and wrote comprehensive tests that achieved 90% code coverage, up from literally zero.
>
> On the coordination side, I ran daily text updates and twice-weekly meetings with service owners. When new developers joined, I created onboarding documentation and personally walked them through the project workflow, coding standards, and the migration patterns we were using. Before stepping down as temporary lead, I created detailed maintainer notes so the service owner's team could take over smoothly.
>
> Throughout the project, I also set up the deployment pipeline using Docker and AWS CodeCommit CI/CD, which reduced deployment time from a full day to 3-5 minutes.

**Result (30 seconds):**

> The system went live in 2025. I personally migrated multiple modules with 90% test coverage — up from zero. The deployment pipeline I helped set up reduced deployment time by 95%. And the handoff documentation I created allowed the service owner's team to continue the project independently after my team moved to the next assignment.
>
> On a personal level, this project taught me how to coordinate a 20+ person backend team, communicate technical progress to senior stakeholders, and work with legacy systems at enterprise scale — specifically for one of Thailand's largest retail operations.

---

### Key Talking Points (Quick Reference)

| Detail | Value |
|--------|-------|
| Client | CP All (7-Eleven Thailand) |
| Legacy system | Java Struts (2004), IBM DB2, stored procedures |
| Target system | Spring Boot 3, MySQL, Microservices, Docker, AWS CodeCommit CI/CD |
| Team size | 50+ total, 20+ backend |
| My role | Temporary team lead + project coordinator + backend developer |
| Migration strategy | Strangler fig (module by module) |
| Hero module | JasperSoft reporting system (10+ stored procedures converted) |
| Test coverage | 0% → 90% |
| Deployment time | 1 day → 3-5 minutes (95% reduction) |
| DB migration | IBM DB2 → MySQL |
| Timeline | Jul 2023 - Aug 2024 (my part), go-live 2025 |
| Deliverables | Migrated modules, 90% test coverage, onboarding docs, maintainer notes |

---

### Behavioral Questions This Story Answers

1. **"Tell me about a time you led a technical project."** ✅
2. **"Describe a time you worked with legacy code."** ✅
3. **"How do you handle coordinating a large team?"** ✅
4. **"Tell me about a time you had to learn something new quickly."** (JasperSoft) ✅
5. **"Describe a time you communicated with stakeholders."** ✅
6. **"Tell me about a time you onboarded or mentored someone."** ✅
7. **"How do you handle complex, ambiguous projects?"** ✅
8. **"Tell me about a time you improved a development process."** (CI/CD pipeline) ✅

---

### Interview Tips for This Story

- **Lead with CP All / 7-Eleven** — this is a brand every Thai interviewer recognizes instantly
- **Emphasize the "resource pool" model** — frame it as "internal consulting team trusted for high-priority projects" (NOT as "we were just outsourced workers")
- **The report module is your hero moment** — spend the most time here
- **90% coverage from 0%** is the headline number — say it clearly
- **The onboarding docs** show leadership maturity — you didn't just do the work, you made sure others could continue it
- **Don't apologize for not making architecture decisions** — you were a team lead and coordinator, which is impressive at your experience level

### ⚠️ Watch Out For

- Interviewer might ask: *"What would you have done differently?"*
  - Good answer: "I would have invested more in automated integration tests earlier. We caught some issues in UAT that could have been caught sooner with better test infrastructure."
- Interviewer might ask: *"Why were you only a temporary lead?"*
  - Good answer: "The resource pool model means teams rotate based on project needs. My leadership period covered the critical migration phase. Once the system was stable, the service owner's permanent team took over — which was always the plan."
- Interviewer might probe DB2 → MySQL: *"How did you handle data type differences?"*
  - Be ready to discuss specific DB2 → MySQL gotchas you encountered

---

## Story 2: Mentoring 4 Interns at Gosoft (Leadership & Teaching)

**Dimensions covered:** Mentoring, teaching, adapting to individuals, feedback, delegation, documentation

**Estimated answer time:** 3-4 minutes (spoken)

---

### The STAR Structure

**Situation (30 seconds):**

> At Gosoft, I was assigned by my manager to mentor university interns from PIM — CP All's own university. These students do year-long part-time internships at CP All subsidiary companies while studying. I mentored 4 interns across 3 different projects over 2-6 months each: 3 interns on the legacy Java Struts refactoring project for CP All's warehouse system, and 1 intern who worked on both the ALL Speedy parcel delivery platform and the IoT monitoring system.

**Task (15 seconds):**

> My job was to take complete beginners and get them to the point where they could independently deliver production features. I needed to balance teaching them fundamentals while keeping the projects moving forward.

**Action (2 minutes — the longest section):**

> I developed a structured onboarding approach. The projects already had documentation, so I created navigation notes — essentially a map telling them "this doc covers X, ask person Y if you're stuck." I taught them Git workflow, unit testing, code readability patterns, and programming fundamentals from day one.

> My regular routine was a weekly standup where I reviewed their code and gave honest, direct feedback — what they did well, what needed improvement. No sugar-coating, but no harsh language either. I also shared online resources for them to study further. I didn't expect them to read all of it, but they did.

> My teaching methodology was "learn by doing with safety nets." For example, one intern on ALL Speedy was struggling with Next.js. Instead of throwing them into production code, I pulled their task, assigned them a practice project — build a todo list app in Next.js — and reviewed it at the end of the week. Once they understood the framework basics, I gave them the real task. They ended up building the **entire dashboard** for the parcel delivery system independently.

> I also adapted to each person. Some interns didn't want to code — they preferred documentation and analysis work. So I assigned them documentation tasks instead of forcing them into development. The documentation they wrote was so thorough that the **service owner adopted it as official project documentation**.

**Result (30 seconds):**

> All 4 interns went from complete beginners to independently delivering production features. The most impressive outcome: one intern on the IoT monitoring web module independently upgraded the project from **Node 12 to Node 24**, migrated the build system from **Babel to Vite**, and achieved **100% test coverage**. That's a level of ownership and technical maturity that most junior engineers don't reach in their first year.

> At least one intern was hired full-time as a Software Engineer at Gosoft after their internship ended — a direct result of the foundation we built together.

---

### Key Talking Points (Quick Reference)

| Detail | Value |
|--------|-------|
| Interns mentored | 4 total (PIM university students) |
| Duration per intern | 2-6 months |
| Projects | Legacy refactor (3), ALL Speedy + IoT monitoring (1) |
| My role | Assigned mentor (also volunteered beyond requirement) |
| Teaching methods | Onboarding notes, weekly standups, code review, practice projects |
| Hero outcome #1 | Intern built full ALL Speedy dashboard independently |
| Hero outcome #2 | Intern did Node 12→24, Babel→Vite migration with 100% test coverage |
| Hero outcome #3 | Documentation interns' work adopted as official project docs |
| Hero outcome #4 | At least 1 intern hired full-time as SE at Gosoft |
| Feedback style | Direct, honest, constructive — no mean words |

---

### Behavioral Questions This Story Answers

1. **"Tell me about a time you mentored or coached someone."** ✅
2. **"How do you adapt your style to different people?"** ✅ (coding vs. documentation interns)
3. **"Tell me about a time you gave difficult feedback."** ✅
4. **"Describe a time you delegated effectively."** ✅ (practice project → real task)
5. **"How do you onboard new team members?"** ✅
6. **"Tell me about a time you invested in someone's growth."** ✅

---

### Interview Tips for This Story

- **Lead with the Node 12→24 + Vite + 100% test coverage** — this is a jaw-dropping outcome for an intern
- **The "todo list first, then real work" approach** shows pedagogical maturity — interviewers love this
- **Adapting to non-coding interns** shows emotional intelligence — you didn't force everyone into your mold
- **Full-time hire** is the ultimate proof of mentoring success — always mention this
- **Frame the documentation interns positively**: "I recognized their strengths and channeled them into work where they excelled" — NOT "they couldn't code so I gave them docs"

### ⚠️ Watch Out For

- Interviewer might ask: *"How did you balance mentoring with your own development work?"*
  - Good answer: "The weekly standup and structured code reviews kept it efficient. I blocked 2-3 hours per week specifically for mentoring. The time invested paid back because within 2-3 months they were delivering features independently, which reduced my workload."
- Interviewer might ask: *"What would you do differently?"*
  - Good answer: "I'd create a more formal curriculum upfront rather than adapting on the fly. The todo list approach worked great but I discovered it reactively. Next time I'd build practice exercises for each major concept from day one."

---

## Story 3: Agoda Observability System (Technical Execution as Intern)

**Dimensions covered:** Initiative, technical execution, collaboration, working within constraints, delivering impact as junior contributor

**Estimated answer time:** 3-4 minutes (spoken)

---

### The STAR Structure

**Situation (30 seconds):**

> During my 4-month Software Engineering internship at Agoda (December to March), I was assigned to help complete an internal observability system for their core services — Booking, Payment, and Tax. The system was about 60% done when I joined, built by another intern under my mentor's guidance. The problem it solved was critical: before this system, when internal APIs went down overnight or after work hours, nobody knew until someone manually tested them the next day — sometimes 8-10 hours later. That meant entire workdays could be lost before incidents were detected.

**Task (15 seconds):**

> My mentor asked me to help finish the system and add missing features. As an intern with limited access and permissions, I couldn't change the entire infrastructure, but I could build specific modules that would reduce incident detection time dramatically.

**Action (2 minutes — the longest section):**

> I took ownership of two critical modules: the **hourly notification system** and the **firewall health checks**.

> For the notification system, I wrote a bash script that ran hourly via cronjob, hitting health endpoints on each service and checking uptime status. The script was deployed to Agoda's internal automation platform — essentially their version of n8n where you can schedule and run scripts. When a service was down, it sent an email to a specific user group so they'd see it first thing in the morning, or even check their work email from home and know immediately.

> For the firewall checks, I built a module that verified services were accessible through the correct ports. I created a whitelist system — if someone wanted to monitor a new service, they'd follow a workflow to request port access, and once approved, the script could detect that service. This was standard security practice, but it made the system extensible without requiring code changes every time.

> I also made minor improvements to the Grafana dashboard — organizing the visualization cells to make it easier for the team to scan at a glance. The system used Agoda's internal database for monitoring rather than Prometheus, which was the existing infrastructure choice.

**Result (30 seconds):**

> The system reduced incident detection time from **8-10 hours to approximately 1 hour** — an 87-90% improvement. Instead of discovering outages mid-morning when someone manually tested APIs, the team would check their email first thing and know immediately if something was down overnight.

> After my internship ended, the team continued using the system and eventually rewrote it in Python, but the core logic I built — the hourly checks, notification flow, and firewall whitelist approach — remained the same.

---

### Key Talking Points (Quick Reference)

| Detail | Value |
|--------|-------|
| Role | Software Engineering Intern at Agoda |
| Duration | 4-month internship, 2 months on observability project |
| Services monitored | Booking, Payment, Tax (3 during my time; 5 after I left) |
| System state when I joined | 60% complete |
| My specific contributions | Hourly email notification cronjob, firewall health check module, minor Grafana improvements |
| Tech stack | Bash scripts, internal automation platform (like n8n), Grafana, internal database |
| Before | 8-10 hour detection time (overnight/after-work incidents) |
| After | ~1 hour detection time (morning email check) |
| Improvement | 87-90% reduction in detection time |
| Legacy | System continued post-internship, rewritten in Python with same logic |

---

### Behavioral Questions This Story Answers

1. **"Tell me about a time you took initiative."** ✅ (built missing modules as intern)
2. **"Describe a time you delivered impact with limited resources/access."** ✅ (intern constraints)
3. **"Tell me about a time you collaborated on a technical project."** ✅ (worked with other intern + mentor)
4. **"How do you approach building systems for reliability?"** ✅
5. **"Tell me about a time you solved a problem that improved efficiency."** ✅

---

### Interview Tips for This Story

- **Frame honestly**: "I helped complete an observability system" — NOT "I built an observability system from scratch"
- **Own your modules**: You built the hourly notification and firewall checks. That's real, production code that reduced detection time by 87-90%.
- **Lead with the impact**: 8-10 hours → 1 hour is the headline number
- **The "legacy" detail is gold**: "They rewrote it in Python but kept my logic" proves your work was solid and reusable
- **Emphasize intern constraints**: You had limited access and permissions, but still delivered production features that solved a real pain point
- **Don't oversell**: If interviewer probes "did you architect this?" — honest answer: "No, the architecture was already 60% done. I built specific modules within that architecture."

### ⚠️ Watch Out For

- Interviewer might ask: *"Why bash scripts instead of Python?"*
  - Good answer: "That was the existing infrastructure choice. The internal automation platform supported bash scripts well, and I was working within the existing tech stack. After I left, they rewrote it in Python for maintainability, but the logic remained the same."
- Interviewer might ask: *"How did you ensure the cronjob itself was reliable?"*
  - Good answer: "The internal platform handled scheduling and execution reliability. My focus was on the health check logic and notification flow. If the cronjob itself failed, that would have been a platform-level issue, not something I could control as an intern with limited access."
- Interviewer might probe Grafana: *"What specific improvements did you make?"*
  - Be honest: "Minor organization improvements — grouping related metrics, making it easier to scan. The other intern built the initial template; I refined it for usability."

---

## Story 4-8: To Be Developed

Potential stories to extract:
- Stepping in as Scrum Master at Agoda (Agile leadership)
- Transmatter senior project (accessibility + innovation)
- Building the Parcel Delivery Platform from scratch (greenfield project)
- The IoT monitoring migration (real-time systems)
- Health Data Science Hackathon (collaboration under pressure)
