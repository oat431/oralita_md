# Master Profile: Sahachan Tippimwong

**Created:** 2026-08-11  
**Purpose:** Single source of truth for all job application artifacts  
**Usage:** Reference this file when creating resumes, cover letters, LinkedIn updates, interview prep

---

## Block 1: Core Identity

**Full Name:** Sahachan Tippimwong  
**Preferred Name:** Sahachan  
**Email:** oat431@gmail.com
**Phone:** +66 83 xxx xxxx
**Location:** Thailand  
**Languages:**
- Thai: Native
- English: Professional working proficiency (B2)

**LinkedIn:** linkedin.com/in/sahachan-tippimwong  
**GitHub:** [oat431 (Oralita)](https://github.com/oat431)


---

## Block 2: Professional Narrative

**Headline:**  
Software Engineer (Full Stack) | Java Spring Boot · NestJS · ReactJS · Golang | Microservices & GitOps | 3+ Years Building Scalable Systems for Thailand's Largest Enterprises

**Professional Summary:**  
Full-stack Software Engineer with 3+ years of experience building and modernizing enterprise-scale systems for Thailand's largest retail and travel companies. Led architectural migrations that reduced deployment time by 95% and improved system performance by 30%+. Mentored 4 university interns who went from beginners to independently delivering production features. Proven track record working on mission-critical systems serving thousands of daily users across retail, logistics, HR, and finance domains.

**Elevator Pitch (30 seconds):**  
"I'm a full-stack software engineer with over 3 years of experience, currently at Gosoft Thailand. My biggest project was leading the backend team on a 50-person migration of CP All's warehouse management system — the system that runs 7-Eleven stores across Thailand. I took it from a 20-year-old Java Struts monolith with zero tests to Spring Boot 3 microservices with 90% test coverage, reducing deployment time from a full day to 3-5 minutes. I also did an internship at Agoda where I helped build an observability system that reduced incident detection time by 90%. I'm looking for my next challenge where I can continue building scalable systems and mentoring junior developers."

---

## Block 3: Experience Database

### Current Role: Gosoft Thailand (Jul 2023 - Present)

**Title:** Software Engineer  
**Company Context:** Internal consulting/resource pool team for CP All (7-Eleven Thailand parent company)  
**Team Model:** "Resource pool" — pulled into high-priority projects as needed

#### Project 1: CP All Warehouse Management System Migration
**Timeline:** July 2023 - August 2024 (my part), go-live 2025  
**Role:** Temporary Team Lead + Project Coordinator + Backend Developer  
**Team Size:** 50 total  
**Role:** Backend Developer
**Client:** CP All (7-Eleven Thailand)  
**Tech Stack:** Java Spring Boot 3, MySQL, Docker, AWS CodeCommit CI/CD, JasperSoft  
**Migration Strategy:** Strangler fig (module by module)

**Key Achievements:**
- Led backend team coordination for 50+ person legacy migration project
- Personally migrated reporting module: converted 10+ DB2 stored procedures to Spring Boot ORM
- Achieved 90% test coverage (up from 0%) on migrated modules
- Reduced deployment time from 1 day to 3-5 minutes (95% reduction)
- Migrated database from IBM DB2 to MySQL with validated data integrity
- Created onboarding documentation and maintainer notes for service owner handoff
- Set up CI/CD pipeline using Docker and AWS CodeCommit

**Metrics:**
- Legacy system age: 20 years (built 2004)
- Test coverage: 0% → 90%
- Deployment time: 1 day → 3-5 minutes (95% reduction)
- API response time improvement: ~30%
- Team size: 50 total (verified — user confirmation 2026-08-11; earlier "20+ backend" breakdown was imprecise)
- Stored procedures migrated: 10+

#### Project 2: ALL Speedy (Parcel Delivery Platform)
**Timeline:** 2023-2024  
**Role:** Backend Developer  
**Tech Stack:** NestJS, NextJS, TypeScript, PostgreSQL, MongoDB, Redis, Docker, GitOps (ArgoCD)  
**Users:** 10,000+ daily parcels processed  
**Uptime:** 99%

**Key Achievements:**
- Built microservices architecture for parcel delivery platform
- Implemented payment processing and order fulfillment modules
- Achieved 99% uptime serving 10K-20K daily transactions
- Upgraded legacy Node.js 12→24 on all 3 API modules (zero tests → 90%+ coverage); guided intern through the same upgrade on the web module (Babel→Vite, 100% coverage)
- Mentored 1 intern who built the full dashboard independently (Next.js)

#### Project 3: HR Platform
**Timeline:** 2023-2024  
**Role:** Full-Stack Developer  
**Tech Stack:** Spring Boot, ReactJS, PostgreSQL, Docker  
**Users:** 1,000+ employees  
**Impact:** 30% reduction in manual processing time

**Key Achievements:**
- Built HR management platform serving 1,000+ employees
- Automated payroll and leave management workflows
- Reduced manual processing time by 30%

#### Project 4: Maintenance Platform
**Timeline:** 2023-2024  
**Role:** Frontend + Backend Developer  
**Tech Stack:** ReactJS, NestJS, PostgreSQL, Docker  
**Impact:** 3x page load improvement, 20% reduction in bug reports

**Key Achievements:**
- Optimized frontend performance: 3x faster page loads
- Implemented code quality improvements: 20% fewer bug reports

#### Project 5: IoT Monitoring Platform
**Timeline:** 2023-2024  
**Role:** Backend Developer  
**Tech Stack:** Node.js, Docker  
**Scale:** 10,000 devices monitored

**Key Achievements:**
- Upgraded Node.js 12→24 on the platform, building test coverage from zero to 90%+
- Monitored 10,000 IoT devices across client sites
- Mentored 1 intern who built the full parcel delivery dashboard in Next.js

> Note (2026-08-11, corrected again): IoT platform is Node.js, NOT Golang. Sahachan only contributed the Node 12→24 upgrade (his 3 API modules) + mentored an intern on the web module. He did NOT build the platform. Kafka + TimescaleDB were a learning plan, never used.

#### Mentoring Responsibilities (Ongoing)
**Total Interns Mentored:** 4 (PIM university students, part-time year-long internships)  
**Duration per Intern:** 2-6 months  
**Teaching Methods:** Weekly standups, code reviews, practice projects, onboarding documentation  
**Outcomes:**
- All 4 interns went from beginners to independently delivering production features
- 1 intern built full ALL Speedy dashboard independently (Next.js)
- 1 intern independently did Node 12→24 + Babel→Vite upgrade on the web module with 100% test coverage
- Documentation interns' work adopted as official project documentation
- At least 1 intern hired full-time as Software Engineer at Gosoft

> Note (2026-08-11, user correction): The Node 12→24 upgrade spans a legacy project with 4 modules (3 API + 1 web), all starting from zero tests. Sahachan personally upgraded the 3 API modules (0 → 90%+ coverage); his intern independently upgraded the web module (Babel→Vite, 100% coverage). Both claims are true — they're different modules of the same project.

---

### Previous Role: Agoda (Dec 2022 - Mar 2023, Internship)

**Title:** Software Engineering Intern  
**Company Context:** Major online travel platform (Thailand's largest tech company)  
**Team:** Internal tools and platform engineering

#### Project 1: Internal Observability System
**Timeline:** 2 months (within 4-month internship)  
**Role:** Contributor (helped complete system started by another intern)  
**Services Monitored:** Booking, Payment, Tax (3 during my time; 5 after I left)  
**Tech Stack:** Bash scripts, internal automation platform (like n8n), Grafana, internal database

**Key Achievements:**
- Built hourly email notification cronjob for service health checks
- Implemented firewall health check module with port whitelist system
- Made minor Grafana dashboard improvements (cell organization)
- Reduced incident detection time from 8-10 hours to ~1 hour (87-90% improvement)
- System continued post-internship, rewritten in Python with same logic

#### Project 2: Finance Feature Enhancement
**Impact:** Reduced manual work from 15 hours to 2-3 hours for finance team

#### Project 3: Legacy C# Service Decommission
**Impact:** Saved ~30 hours annually in maintenance

#### Additional Contribution:
- Stepped in as temporary Scrum Master during team's transition period

---

### Previous Role: National Science and Technology Development Agency (NSTDA) — Part-time Programmer

**Title:** Part-time Programmer  
**Note:** This was a part-time role, not an internship or staff position. Details to be added in a future session.

---

## Block 4: Education & Credentials

### Education

**Chiang Mai University (CMU) — College of Arts, Media and Technology (CAMT)**  
Bachelor of Science in Software Engineering  
Graduation: April 2023  
GPA: 3.58 / 4.00  
Honors: First-Class Honors  
Relevant Coursework: Software Engineering, Database Systems, Web Development, Software Design, A.I. Agents, DevOps, Backend Development

**Senior Project:** Transmatter  
- Accessible content-reading platform for visually impaired users using OCR and text-to-speech
- GitHub: github.com/Transmatter (org repo — 14 public repos, verified live)

**Teaching Assistant:** Selected as undergraduate TA to mentor students in software engineering coursework

### Certifications

1. **HackerRank SQL (Advanced)** - 2024
2. **HackerRank SQL (Intermediate)** - 2024
3. **HackerRank Java (Intermediate)** - 2024
4. **Codegoda 2023** - Coding Competition Participant
5. **Hackathon Participant** - Health Data Science Hackathon 2023

### English Proficiency
- **CMU-eGrad:** B2 (Upper-Intermediate) — 2022 (official English proficiency test, CMU Registrar: reg.cmu.ac.th/egrad-reserve)
- **Future:** Planning to take TOEIC for additional certification
- Note (2026-08-11): earlier drafts said "CMU TEGS" — wrong name, corrected to CMU-eGrad after checking the official CMU registrar site.

### Awards

- **1st Place, SE Show Pro CAMT 14 senior project exhibition (Sep 2022)** — Transmatter Platform (team with Thitisan Chailuek). Verified via official CMU article: cmu.ac.th/th/article/b3fcb584-a65e-4fd8-b297-49756a4eb979
- First-Class Honors, Software Engineering (GPA 3.58)
- Health Data Science Hackathon Participant

> Note (2026-08-11): Earlier drafts said "2nd place, KMUTNB competition" — wrong on both count and university. Verified correct version: 1st place at CMU CAMT's SE Show Pro CAMT 14 (Sep 28, 2022), confirmed by official CMU news article.

---

## Block 5: Skills Inventory

### Programming Languages
| Skill | Proficiency | Notes |
|-------|-------------|-------|
| Java | Expert | Primary language, 2+ years production experience |
| JavaScript | Proficient | Full-stack usage |
| TypeScript | Proficient | NestJS, NextJS, ReactJS |
| Golang | Proficient | HR management platform |
| Scala | Familiar | Exposure through Agoda codebase |

### Frameworks & Libraries
| Skill | Proficiency | Notes |
|-------|-------------|-------|
| Spring Boot | Proficient | Spring Boot 3, used in 4+ projects |
| NestJS | Proficient | Parcel delivery platform |
| ReactJS | Proficient | HR platform, maintenance platform |
| Express.js | Proficient | Various projects |
| NextJS | Proficient | ALL Speedy dashboard |
| GraphQL | Proficient | API design |

### Databases
| Skill | Proficiency | Notes |
|-------|-------------|-------|
| PostgreSQL | Proficient | Primary relational DB |
| MySQL | Proficient | DB2 migration project |
| MongoDB | Proficient | Document storage |
| Redis | Proficient | Caching layer |
| IBM DB2 | Familiar | Legacy system (migrated away from) |
| TimescaleDB | Learning plan | Not yet used in production — do not list on resume/LinkedIn |

### DevOps & Infrastructure
| Skill | Proficiency | Notes |
|-------|-------------|-------|
| Docker | Proficient | Containerization across all projects |
| Kubernetes | Familiar | Exposure through GitOps |
| GitOps (ArgoCD) | Familiar | Parcel delivery deployment |
| AWS CodeCommit | Proficient | CI/CD for warehouse system (legacy project) |
| Bitbucket | Proficient | Current repo hosting for all Gosoft projects |
| Azure | Proficient | Some project exposure |
| AWS | Familiar | General AWS services |

### Monitoring & Observability
| Skill | Proficiency | Notes |
|-------|-------------|-------|
| Grafana | Familiar | Agoda observability project |
| Prometheus | Familiar | Exposure |
| Custom monitoring | Proficient | Built internal monitoring at Agoda |

### Tools & Methodologies
| Skill | Proficiency | Notes |
|-------|-------------|-------|
| Git | Expert | Daily usage, taught to interns |
| Agile/Scrum | Proficient | Scrum Master experience at Agoda |
| JasperSoft | Familiar | Report module migration |
| Unit Testing | Proficient | JUnit, Jest, 90% coverage achieved |
| Code Review | Proficient | Weekly reviews with interns |

### Soft Skills
- Team leadership (temporary team lead on 50+ person project)
- Mentoring and teaching (4 interns over 2+ years)
- Stakeholder communication (project coordinator role)
- Technical documentation (onboarding notes, maintainer notes)
- Adaptability (worked across 5+ different projects and tech stacks)

---

## Block 6: Projects Portfolio

### Featured Project 1: CP All Warehouse Management System Migration
**Type:** Enterprise migration project  
**Scale:** 50+ person team, 20-year legacy system  
**Impact:** 95% deployment time reduction, 0% → 90% test coverage  
**Tech:** Java Spring Boot 3, MySQL, Docker, AWS CodeCommit, JasperSoft  
**Role:** Temporary team lead + backend developer  
**Status:** Go-live 2025

### Featured Project 2: ALL Speedy (Parcel Delivery Platform)
**Type:** Greenfield microservices platform  
**Scale:** 10K-20K daily transactions, 99% uptime  
**Tech:** NestJS, NextJS, TypeScript, PostgreSQL, MongoDB, Redis, Docker, GitOps  
**Role:** Backend developer + mentor  
**Status:** Production

### Featured Project 3: IoT Monitoring Platform
**Type:** Real-time data platform  
**Scale:** 10,000 devices monitored  
**Tech:** Node.js, Docker  
**Role:** Backend developer  
**Status:** Production

### Featured Project 4: Transmatter (Senior Project)
**Type:** Accessibility tool  
**Impact:** 🏆 1st Place, SE Show Pro CAMT 14 senior project exhibition (Sep 2022) — verified via official CMU article. Microservices architecture (Spring Boot, Vue, Python, C++, Docker), 14 public repos  
**Tech:** OCR, text-to-speech, Spring Boot, Vue, microservices  
**Role:** Co-lead developer (team of 2: Sahachan + Thitisan Chailuek)  
**Status:** GitHub: github.com/Transmatter (org repo, verified live 2026-08-11)

### Other Projects:
- HR Platform (1,000+ employees)
- Maintenance Platform (3x performance improvement)
- Agoda Observability System (87-90% detection time reduction)
- Agoda Finance Feature (15hrs → 2-3hrs manual work)

---

## Block 7: STAR Stories

**Reference:** See `Sahachan-STAR-Stories.md` for full interview-ready stories

### Story 1: CP All Warehouse Migration
**Dimensions:** Technical leadership, Legacy modernization, Team coordination, Stakeholder communication  
**Key Metrics:** 50+ person team, 0% → 90% test coverage, 1 day → 3-5 min deployment  
**Use For:** "Tell me about a time you led a technical project"

### Story 2: Mentoring 4 Interns
**Dimensions:** Mentoring, Teaching, Adapting to individuals, Feedback  
**Key Metrics:** 4 interns, Node 12→24 migration, 100% test coverage, 1 full-time hire  
**Use For:** "Tell me about a time you mentored someone"

### Story 3: Agoda Observability System
**Dimensions:** Initiative, Technical execution, Collaboration, Working within constraints  
**Key Metrics:** 8-10hrs → 1hr detection time, 87-90% improvement  
**Use For:** "Tell me about a time you took initiative"

### Stories 4-8: To Be Developed
Potential stories:
- Stepping in as Scrum Master at Agoda
- Building Parcel Delivery Platform from scratch
- Health Data Science Hackathon
- Teaching Assistant experience
- Transmatter senior project

---

## Block 8: Job Search Parameters

### Target Roles (in priority order)
1. Software Engineer (Full Stack)
2. System Analyst
3. Backend Engineer

### Target Industries
- Health industry
- Insurance industry
- Finance industry
- (Open to other industries as well)

### Target Market
- **Primary:** Thailand (Bangkok-based or remote)
- **Secondary:** Remote international (if opportunities arise)

### Salary Expectations
- **Current salary:** 32,000 - 50,000 THB/month
- **Minimum acceptable:** 40,000 THB/month
- **Target range:** 50,000 - 70,000 THB/month (based on market research for mid-level SE in Thailand)

### Work Arrangement Preferences
- **Preferred:** Hybrid work
- **Acceptable:** On-site, remote, hybrid (all work)
- **Location:** Open to anywhere (no geographic restrictions)

### Company Size
- **Open to:** Small to large companies
- **No preference:** Startup vs. enterprise

### Technical Deal-Breakers
- **None:** "This is the A.I. era, I can work with any tech as long as they have spec"
- **Preference:** Modern tech stacks (but flexible)

### Deal-Breakers (Non-Technical)
- (None specified yet)

---

## Quick Reference: Key Metrics

| Metric | Value | Context |
|--------|-------|---------|
| Years of experience | 3+ years | Agoda intern (4 months) + Gosoft (Jul 2023 - present) |
| Largest team size | 50+ people | CP All warehouse migration |
| Interns mentored | 4 | Across 3 projects |
| Deployment time reduction | 95% | 1 day → 3-5 minutes |
| Test coverage achieved | 90% | Up from 0% |
| Daily transactions | 10K-20K | Parcel delivery platform |
| Employees served | 1,000+ | HR platform |
| IoT devices | 10,000 | Monitoring platform |
| Detection time reduction | 87-90% | Agoda observability (8-10hrs → 1hr) |
| API response improvement | ~30% | Warehouse system |
| Page load improvement | 3x | Maintenance platform |
| Bug report reduction | 20% | Maintenance platform |

---

## Usage Notes

### For Resume Creation:
- Pull from Block 3 (Experience) with quantified achievements
- Tailor Block 5 (Skills) based on job description
- Use Block 2 (Narrative) for professional summary

### For Cover Letters:
- Use Block 2 (Narrative) for opening hook
- Pull 2-3 relevant achievements from Block 3
- Reference Block 8 (Job Search Parameters) for targeting

### For LinkedIn Updates:
- Block 2 (Narrative) → Headline and About section
- Block 3 (Experience) → Experience entries with metrics
- Block 5 (Skills) → Skills section (prioritize top 10)

### For Interview Prep:
- Block 7 (STAR Stories) → Behavioral question answers
- Block 3 (Experience) → Technical deep-dive preparation
- Block 2 (Narrative) → "Tell me about yourself" answer

---

## Last Updated
2026-08-11 — Initial creation after resume review, LinkedIn audit, and 3 grill-me sessions
