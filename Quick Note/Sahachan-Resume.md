# Resume: Sahachan Tippimwong (2026-08-11 — Synced to Verified Facts)

**Created:** 2026-08-11  
**Last synced:** 2026-08-11 (after fact-verification pass)  
**Source of truth:** `F:\projects\sahachan_resume\resume.yml` (YAMLResume schema)  
**Build:** `bash build.sh` in `F:\projects\sahachan_resume\` → `resume.pdf` (1 page)  
**Target:** Software Engineer / Backend Engineer / System Analyst roles in Thailand

---

## Where the Resume Lives Now

| File | Purpose |
|---|---|
| `F:\projects\sahachan_resume\resume.yml` | **The actual resume** — YAMLResume schema (content → basics/work/education/skills...) |
| `F:\projects\sahachan_resume\build.sh` | Build pipeline: yamlresume → patch fonts/CJK → xelatex → PDF |
| `F:\projects\sahachan_resume\patch_tex.py` | Fixes Times New Roman + disables CJK (English-only resume) |
| `F:\projects\sahachan_resume\spare-parts.yml` | Trimmed sections (awards, certificates, projects, interests) for 2-page variants |
| `F:\obsidian_note\oralita_md\Quick Note\Sahachan.md` | Master profile — ALL career data, metrics, correction history |

---

## Current Resume Content (Verified Facts Only)

### Summary (5 bullets)
- 3+ years building enterprise systems for CP All (7-Eleven), Agoda
- Led 50-person team on legacy migration — 95% deployment reduction, 90% test coverage from zero
- Built observability tooling at Agoda cutting incident detection by 87%+
- Mentored 4 interns across 3 projects; one hired full-time
- Full SDLC across health, HR, logistics, finance, travel

### Work 1: Gosoft (Thailand) Co., Ltd. — Software Engineer (Jul 2023 – Present)
- **Led backend** on 50-person team migrating warehouse system — Java Struts/DB2 → Spring Boot 3/MySQL, 10K–20K daily transactions
- Upgraded legacy Node.js 12→24 across **3 API modules** (zero tests → **90%+ coverage**); guided intern through the same upgrade on the **web module** (Babel→Vite, **100% coverage**)
- **30% API response improvement** on shipment tracking and reporting endpoints
- **Mentored 4 interns** across 3 projects; one hired full-time
- Documentation adopted as official project reference by service owner

### Work 2: Agoda Services Co., Ltd. — Software Engineer Intern (Dec 2022 – Mar 2023)
- Built health-check notification system for internal finance services (Booking, Payment, Tax) using bash cronjobs on Agoda's internal automation platform
- Decommissioned legacy C# finance library — reduced processing time from 15 hours to 2–3 hours (80%+ reduction)

### Education: CMU CAMT — B.Sc. Software Engineering (Aug 2019 – Apr 2023)
- First-Class Honors (GPA 3.58 / 4.00)
- Senior project Transmatter: **1st Place**, SE Show Pro CAMT 14 exhibition

### Languages
- Thai: Native or Bilingual Proficiency
- English: Professional Working Proficiency (B2 — CMU-eGrad 2022)

### Skills (4 balanced categories × 4 keywords)
- **Languages** (Advanced): Java, Golang, TypeScript, JavaScript
- **Frameworks** (Advanced): Spring Boot 3, NestJS, React.js, Node.js
- **Databases** (Advanced): MySQL, PostgreSQL, MongoDB, Redis
- **DevOps & Tools** (Intermediate): Docker, Kubernetes, AWS CodeCommit, Bitbucket, Grafana

---

## Verified Facts & Corrections (2026-08-11)

Do NOT reintroduce these errors:

| Topic | Verified truth |
|---|---|
| **University** | CMU CAMT (Chiang Mai University, College of Arts, Media and Technology). NEVER KMUTNB. |
| **English test** | **CMU-eGrad** B2 (2022) — official CMU Registrar test (reg.cmu.ac.th/egrad-reserve). NOT "CMU TEGS". |
| **English level** | "Professional Working Proficiency" — honest for B2. NOT "Full Professional". |
| **Node 12→24** | Legacy project = 4 modules (3 API + 1 web), all zero tests. **He** did 3 API modules (0→90%+). His **intern** independently did the web module (Babel→Vite, 100%). BOTH claims true — different modules. |
| **IoT platform** | Node.js + Docker. Sahachan only did Node 12→24 upgrade (3 API modules), did NOT build it. Kafka/TimescaleDB/Golang NEVER used. |
| **Version control** | AWS CodeCommit (legacy warehouse project), Bitbucket (all current projects). **NEVER GitLab.** |
| **Agoda company** | Agoda Services Co., Ltd. (full legal name) |
| **Team size** | 50 total (warehouse migration). No "20+ backend" breakdown. |
| **Transmatter** | 1st Place, SE Show Pro CAMT 14 (Sep 28, 2022), team of 2 with Thitisan Chailuek. Verified: cmu.ac.th/th/article/b3fcb584-a65e-4fd8-b297-49756a4eb979. Repo: **github.com/Transmatter** (org, 14 public repos). NOT under oat431/sahachan. |
| **NSTDA** | Never interned/staff there. Part-time programmer elsewhere — story TBD, not on resume. |
| **Dates** | Gosoft 2023-07-01 → present. Agoda Dec 2022 – Mar 2023. |

---

## Why This Resume Works

### Structure Decisions

1. **Single-column layout** — ATS parses cleanly, no jumbled text
2. **Summary first** — 4 lines packed with keywords and numbers. Recruiter sees this in 6 seconds.
3. **Experience before Education** — 3+ years of real work; strongest signal
4. **Gosoft as ONE entry with multiple projects** — versatility without fragmenting the timeline
5. **Every bullet has a number** — 95%, 90%, 10K-20K, 1,000+, 10,000 devices, 87%+
6. **1 page** — for 3 years of experience, 1 page is the standard

### Content Decisions

1. **CP All / 7-Eleven mentioned prominently** — every Thai interviewer recognizes this instantly
2. **"Resource pool" framed as consulting** — "deployed to high-priority projects" sounds better than "outsourced"
3. **Node upgrade bullet does double duty** — his 3 API modules (technical) + intern's web module (mentoring) in one line
4. **Agoda contributions are honest** — "built hourly notification system," not "built observability platform from scratch"
5. **Skills categorized by proficiency** — Advanced/Intermediate tells interviewers where to probe deep vs. light
6. **Award verified** — 1st Place SE Show Pro CAMT 14 has an official CMU news URL as proof

### What Was Cut (And Why)

- ❌ **Keywords blocks under work entries** — redundant; keywords already live in bullets + Skills section (ATS reads all text)
- ❌ **Website/address** — not needed; GitHub/LinkedIn are in profiles
- ❌ **Trivial projects** (Discord bot, Minecraft server, todo apps) — dilute strong projects
- ❌ **TOPCIT score** (478/1000) — below midpoint, hurts more than helps
- ❌ **Detailed coursework list** — real work experience makes coursework noise
- ❌ **Two-column layout** — ATS breaks on it
- ❌ **Kafka, TimescaleDB, GitLab, Scala, GraphQL, AWS** — either never used or not verifiable from work history
- ❌ **Projects section** (moved to `spare-parts.yml`) — work entries already cover them
- ❌ **Interests section** — no hiring value

---

## How to Use This

### Build PDF
```bash
cd F:\projects\sahachan_resume
bash build.sh
# Output: resume.pdf (1 page, Times New Roman, ATS-compatible)
```

### Edit Content
1. Edit `resume.yml` (the actual resume)
2. Rebuild: `bash build.sh`
3. If yamlresume validation complains (summary >1024 chars, invalid dates), fix those warnings

### Tailor Per Application
For each job, adjust:
1. **Summary** — mention the company's industry/domain
2. **Achievement order** — put most relevant bullets first
3. **Skills** — reorder to match JD keywords
4. **2-page variant** — copy sections from `spare-parts.yml` (awards, certificates, projects) when a company asks for a full CV

---

## Next Steps

1. ✅ Build PDF (done — `F:\projects\sahachan_resume\resume.pdf`)
2. ✅ Verify facts (done — correction log above)
3. Update LinkedIn manually using `Sahachan-Linkedin.md`
4. Test resume with an ATS scanner (resumeworded.com) once ready
5. Start applying!
