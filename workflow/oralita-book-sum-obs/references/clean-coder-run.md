# The Clean Coder — Run Data

> Reference: actual extraction and mapping from the 2026-06-23 run. Use as a template for similar behavioral/professional-development books.

## Book Metadata

- **Title:** The Clean Coder: A Code of Conduct for Professional Programmers
- **Author:** Robert C. Martin
- **Year:** 2011
- **ISBN:** 0-13-708107-3
- **PDF pages:** 244
- **Type:** Behavioral / professional practices (NOT code-heavy)
- **Chapter count:** 14 + Appendix

## PDF-to-Printed Page Offset

Offset: **34** — PDF page N = printed page (N−34).

Formula: PDF p41 = printed p7, so printed_page = pdf_page − 34.

## Chapter Extraction Map

| Ch | Name | PDF Range | Printed Pages | Chars | Est. Tokens |
|----|------|-----------|---------------|-------|-------------|
| 00 | Pre-Requisite Introduction | 35–40 | 1–6 | 10,330 | ~2,582 |
| 01 | Professionalism | 41–56 | 7–22 | 29,404 | ~7,351 |
| 02 | Saying No | 57–78 | 23–44 | 41,584 | ~10,396 |
| 03 | Saying Yes | 79–90 | 45–56 | 18,700 | ~4,675 |
| 04 | Coding | 91–110 | 57–76 | 37,322 | ~9,330 |
| 05 | Test Driven Development | 111–118 | 77–84 | 13,456 | ~3,364 |
| 06 | Practicing | 119–128 | 85–94 | 16,845 | ~4,211 |
| 07 | Acceptance Testing | 129–146 | 95–111 | 29,067 | ~7,266 |
| 08 | Testing Strategies | 147–154 | 113–119 | 9,264 | ~2,316 |
| 09 | Time Management | 155–168 | 121–133 | 22,119 | ~5,529 |
| 10 | Estimation | 169–182 | 135–148 | 22,795 | ~5,698 |
| 11 | Pressure | 183–190 | 149–155 | 10,453 | ~2,613 |
| 12 | Collaboration | 191–200 | 157–166 | 16,501 | ~4,125 |
| 13 | Teams and Projects | 201–206 | 167–171 | 7,460 | ~1,865 |
| 14 | Mentoring, Apprenticeship, Craftsmanship | 207–220 | 173–185 | 24,936 | ~6,234 |
| 99 | Tooling (Appendix A) | 221–238 | 187–204 | 28,828 | ~7,207 |

**Total:** ~345,000 chars, ~86,000 tokens

## Output File Mapping

```
clean-coder/
├── Clean Coder Overview.md        ← Pre-Requisite + master index
├── Professionalism.md
├── Saying No.md
├── Saying Yes.md
├── Coding Discipline.md
├── Test Driven Development.md
├── Practicing.md
├── Acceptance Testing.md
├── Testing Strategies.md
├── Time Management.md
├── Estimation.md
├── Pressure.md
├── Collaboration.md
├── Teams and Projects.md
├── Mentoring & Craftsmanship.md
└── Tooling.md
```

## Batch Dispatch Order

| Batch | Chapters | Rationale |
|-------|----------|-----------|
| 1 | 1, 2, 3 | Foundation chapters — medium size |
| 2 | 4, 5, 6 | Coding practices — medium |
| 3 | 7, 8, 9 | Testing + time — varied size |
| 4 | 10, 11, 12 | Estimation, pressure, collaboration |
| 5 | 13, 14, 99 | Small + large → last batch (heavy chapters don't block) |

## Broken Links Found & Fixed

| File | Broken Link | Fixed To | Reason |
|------|-------------|----------|--------|
| Professionalism.md | `[[Pair Programming]]` | `[[Collaboration]]` | Pairing covered in Collaboration chapter |
| Testing Strategies.md | `[[Continuous Integration]]` | `[[Tooling]]` | CI covered in Tooling appendix |
| Tooling.md | `[[Commitment & SAYING NO]]` | `[[Saying No]]` | Malformed filename from sub-agent |

## Key Differences from Clean Code Run

1. **Behavioral, not code-heavy:** All chapters used Template A. No case studies, no reference catalog.
2. **Smaller book:** 244pp vs 462pp, ~86K tokens vs ~300K input.
3. **Dialogue-heavy:** Sub-agents captured character dialogues (Don/Mike, Sam/Tom, Paula scenarios) rather than ❌/✅ code blocks.
4. **Pre-Requisite merged into Overview:** The intro chapter was short (2.5K tokens) and better served as the Overview opener.
