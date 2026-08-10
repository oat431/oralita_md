# Resume: Sahachan Tippimwong (Complete Rewrite)

**Created:** 2026-08-11  
**Format:** YAMLResume (.yml) — ATS-compatible, version-controlled  
**Target:** Software Engineer / Backend Engineer / System Analyst roles in Thailand

---

## The Resume (YAMLResume Format)

Copy this into `resume.yml`:

```yaml
# resume.yml — Sahachan Tippimwong
# Build with: npx yamlresume build resume.yml

personal:
  name: Sahachan Tippimwong
  title: Software Engineer (Full Stack)
  email: oat431@gmail.com
  phone: "+66 83 630 6462"
  location: Thailand
  website: ""
  github: github.com/oat431
  linkedin: linkedin.com/in/sahachan-tippimwong

summary: >
  Full-stack Software Engineer with 3+ years of experience building and 
  modernizing enterprise-scale systems for Thailand's largest enterprises, 
  including CP All (7-Eleven) and Agoda. Led backend teams on legacy 
  migration projects achieving 95% deployment time reduction and 90% test 
  coverage. Built microservices platforms processing 20K+ daily transactions 
  and real-time IoT systems monitoring 10,000 devices. Mentored 4 university 
  interns from beginners to independent production contributors.

experience:
  - company: Gosoft (Thailand) Co., Ltd.
    position: Software Engineer
    location: Bangkok, Thailand (Hybrid)
    startDate: 2023-07
    endDate: Present
    description: >
      Internal consulting team ("resource pool") deployed to high-priority 
      projects across CP All group companies.
    achievements:
      - >
        Led backend coordination (20+ developers) on CP All's warehouse 
        management system migration — the backend running all 7-Eleven stores 
        in Thailand. Migrated 20-year-old Java Struts monolith to Spring Boot 3 
        microservices with strangler fig strategy, achieving 90% test coverage 
        (up from 0%) and reducing deployment time from 1 day to 3-5 minutes (95%).
      - >
        Personally migrated the reporting module: reverse-engineered 10+ IBM DB2 
        stored procedures, rebuilt logic using Spring Boot ORM, and validated 
        output parity against legacy system. Migrated database from IBM DB2 to 
        MySQL with full data integrity validation.
      - >
        Built parcel delivery platform (ALL Speedy) using NestJS microservices 
        and NextJS frontend, processing 10K-20K daily parcels at 99% uptime. 
        Implemented payment processing, order fulfillment, and real-time 
        tracking modules with GitOps deployment via ArgoCD.
      - >
        Developed HR management platform (Spring Boot + ReactJS) serving 1,000+ 
        employees, automating payroll and leave workflows and reducing manual 
        processing time by 30%.
      - >
        Built IoT monitoring platform using Golang, Kafka, and TimescaleDB, 
        ingesting real-time telemetry from 10,000 devices across client sites.
      - >
        Mentored 4 university interns (PIM) from complete beginners to 
        independent feature delivery. Key outcomes: 1 intern built full 
        dashboard independently, 1 intern performed Node 12→24 + Babel→Vite 
        migration with 100% test coverage, at least 1 hired full-time at Gosoft.

  - company: Agoda
    position: Software Engineering Intern
    location: Bangkok, Thailand
    startDate: 2022-12
    endDate: 2023-03
    description: >
      Internal tools and platform engineering team at Thailand's largest 
      online travel platform.
    achievements:
      - >
        Built hourly health-check notification system for internal services 
        (Booking, Payment, Tax) using bash cronjobs on Agoda's internal 
        automation platform. Reduced incident detection time from 8-10 hours 
        (overnight/after-hours) to ~1 hour (87-90% improvement).
      - >
        Implemented firewall health check module with port whitelist system, 
        enabling extensible service monitoring without code changes.
      - >
        Engineered finance summary feature for back-office financial team using 
        Scala Play Framework and GraphQL, reducing manual work from 15 hours 
        to 2-3 hours per cycle.
      - >
        Decommissioned legacy in-house C# package used by 3 internal teams, 
        significantly reducing long-term maintenance costs and technical debt.
      - >
        Stepped in as Scrum Master, facilitating Agile ceremonies and managing 
        team velocity to ensure successful, on-time sprint delivery.

education:
  - institution: Chiang Mai University (CMU) — College of Arts, Media and Technology (CAMT)
    degree: Bachelor of Science in Software Engineering
    startDate: 2019-08
    endDate: 2023-04
    gpa: "3.58 / 4.00"
    honors: First-Class Honors
    highlights:
      - >
        Senior Project: Transmatter — Accessible content-reading platform for 
        visually impaired users using OCR and text-to-speech.
      - >
        Teaching Assistant: Selected as undergraduate TA to mentor students in 
        software engineering coursework.

skills:
  languages:
    expert:
      - Java
    proficient:
      - JavaScript
      - TypeScript
      - Golang
      - Scala
  frameworks:
    proficient:
      - Spring Boot 3
      - NestJS
      - ReactJS
      - NextJS
      - Express.js
      - GraphQL
  databases:
    proficient:
      - PostgreSQL
      - MySQL
      - MongoDB
      - Redis
      - TimescaleDB
    familiar:
      - IBM DB2
  devops:
    proficient:
      - Docker
      - AWS CodeCommit
      - CI/CD Pipelines
    familiar:
      - Kubernetes
      - ArgoCD (GitOps)
      - AWS
      - Azure
  tools:
    proficient:
      - Git
      - Unit Testing (JUnit, Jest)
      - Agile/Scrum
    familiar:
      - Grafana
      - Prometheus
      - JasperSoft
  other:
    - Microservices Architecture
    - REST API Design
    - System Analysis
    - Technical Documentation
    - Team Mentoring

certifications:
  - name: "SQL (Advanced)"
    issuer: HackerRank
    date: 2024
  - name: "SQL (Intermediate)"
    issuer: HackerRank
    date: 2024
  - name: "Java (Intermediate)"
    issuer: HackerRank
    date: 2024
  - name: "Codegoda 2023 — Coding Competition Participant"
    issuer: Codegoda
    date: 2023

awards:
  - title: First-Class Honors — Bachelor of Science in Software Engineering
    issuer: Chiang Mai University (CMU)
    date: 2023
    description: GPA 3.58 / 4.00

languages:
  - language: Thai
    proficiency: Native
  - language: English
    proficiency: Professional Working (B2 — CMU TEGS 2022)
```

---

## Why This Resume Works

### Structure Decisions

1. **Single-column layout** — ATS parses cleanly, no jumbled text
2. **Summary first** — 4 lines packed with keywords and numbers. Recruiter sees this in 6 seconds.
3. **Experience before Education** — You have 2+ years of real work; that's your strongest signal
4. **Gosoft as ONE entry with multiple projects** — Shows versatility without fragmenting your timeline
5. **Every bullet has a number** — 95%, 90%, 10K-20K, 1,000+, 10,000 devices, 87-90%

### Content Decisions

1. **CP All / 7-Eleven mentioned prominently** — Every Thai interviewer recognizes this instantly
2. **"Resource pool" framed as consulting** — "Internal consulting team deployed to high-priority projects" sounds much better than "we were outsourced workers"
3. **Mentoring outcomes are specific** — Not "mentored interns" but "1 intern did Node 12→24 with 100% test coverage"
4. **Agoda contributions are honest** — "Built hourly notification system" not "Built observability platform from scratch"
5. **Skills categorized by proficiency** — Expert/Proficient/Familiar tells interviewer where to probe deep vs. light

### What Was Cut (And Why)

- ❌ **Personal traits** ("quick learner", "friendly") — No evidence, wastes space
- ❌ **Trivial projects** (Discord bot, Minecraft server, todo apps) — Dilutes strong projects
- ❌ **TOPCIT score** (478/1000) — Below midpoint, hurts more than helps
- ❌ **Detailed coursework list** — You have real work experience now; coursework is noise
- ❌ **Two-column layout** — ATS breaks on it

---

## How to Use This

### Build PDF
```bash
# Install yamlresume
npx create-yamlresume my-resume
cd my-resume

# Copy the YAML above into resume.yml
# Then build:
npx yamlresume build resume.yml

# Output: resume.pdf (clean, ATS-compatible)
```

### Version Control
```bash
git init
git add resume.yml
git commit -m "Initial resume v1.0"

# For each job application, create a branch:
git checkout -b apply-agoda
# Edit resume.yml to tailor for Agoda
git commit -m "Tailored for Agoda SWE role"
npx yamlresume build resume.yml
# Save as resume-agoda.pdf
```

### Tailor Per Application
For each job, adjust:
1. **Summary** — mention the company's industry/domain
2. **Achievement order** — put most relevant bullets first
3. **Skills** — reorder to match JD keywords
4. **Keywords** — mirror the job description language

---

## Next Steps

1. Install yamlresume and build your first PDF
2. Review the output visually — adjust template if needed
3. Test with an ATS scanner (resumeworded.com)
4. Get feedback from 2-3 peers
5. Start applying!
