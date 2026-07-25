# Interview Assignment Example — IT 08-1 Comment Board

Real-world example of applying `full-stack-monorepo` to a coding assignment.

## Assignment Requirements

- Backend: Go (latest) with Fiber v3
- Frontend: React.js with Vite + TypeScript
- Database: PostgreSQL
- Mono-repo: API and Web in single repository
- Bonus: Unit tests earn additional points
- Naming: Production-style (no placeholder names like "ThaiBev", "TCCtech")

## What We Built

A comment board where:
- User "Change can" has an image post with timestamp
- User "Blend 285" posts comments via Enter or Send button
- Comments persist in PostgreSQL, display newest first

## Key Naming Decisions

- Go module: `blog.it081.com/api` (domain-based, not GitHub path)
- npm package: `@it081/blog-web` (scoped)
- Docker images: `it081/blog-api`, `it081/blog-web`
- E2E package: `@it081/e2e`

## Test Coverage (Bonus Points)

| Layer | Tool | Tests |
|-------|------|-------|
| API | Go testify | 8 handler tests with mock repo |
| Web | Vitest + RTL | 17 component tests |
| E2E | Playwright | 5 integration tests |

## Checklist Pattern for Interview README

```markdown
### Requirements
- [x] Backend API — Go with Fiber v3
- [x] Frontend — React.js with Vite + TypeScript
- [x] Database — PostgreSQL with proper schema
- [x] Mono-repo structure
- [x] Production-style naming
- [x] No placeholder names in code

### Bonus
- [x] API unit tests (8 tests)
- [x] Web component tests (17 tests)
- [x] E2E integration tests (5 tests)
```

## UI Structure

```
┌─────────────────────────────┐
│         IT 08-1             │  ← Navbar (centered title)
├─────────────────────────────┤
│  ┌ C ┬ Change can          │
│  │   │ 16 ตุลาคม 2564 16:00│  ← PostCard (image + author + date)
│  ├─ ┴──────────────────────┤
│  │    /post_image.jpg      │
├─────────────────────────────┤
│  ความคิดเห็น                │
│  ┌ B ┬ Blend 285           │  ← CommentBox (name above input)
│  │   │ [input...] [Send]   │
│  ├─ ┴──────────────────────┤
│  ┌ B ┬ Blend 285  │ time │ │  ← CommentList
│  │   │ comment text        │
│  └───┴─────────────────────┘
└─────────────────────────────┘
```
