---
name: full-stack-monorepo
description: "Scaffold full-stack monorepos with Go/Fiber API, React/Vite frontend, PostgreSQL, and Playwright E2E — each as its own project within the repo."
triggers:
  - monorepo setup
  - full-stack project scaffolding
  - Go Fiber + React project
  - interview coding assignment
  - comment board / CRUD app
---

# Full-Stack Monorepo Architecture

Scaffold production-style monorepos with Go API, React frontend, and E2E tests as **three separate projects** sharing one repo.

## When to Use

- Full-stack coding assignments (interview, take-home)
- CRUD apps with Go backend + React frontend
- Projects that need API + Web + E2E in one repo

## Project Structure

```
project-root/
├── api/                              # Go Fiber API (own go.mod)
│   ├── cmd/server/main.go
│   ├── internal/
│   │   ├── config/                   # Env-based config
│   │   ├── handler/                  # HTTP handlers + tests
│   │   ├── middleware/                # CORS, logger
│   │   ├── model/                    # Domain types, DTOs
│   │   └── repository/               # DB access (no migrations here)
│   ├── migrations/                   # SQL migrations (goose, project-level)
│   ├── Makefile
│   ├── Dockerfile
│   └── go.mod
├── web/                              # React + Vite (own package.json)
│   ├── src/
│   │   ├── components/
│   │   │   └── __tests__/            # Component tests colocated
│   │   ├── services/                 # API client
│   │   ├── types.ts
│   │   └── App.tsx
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── package.json
├── e2e/                              # Playwright E2E (own package.json)
│   ├── *.spec.ts
│   ├── playwright.config.ts
│   └── package.json
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Key Decisions

### 1. Go Module Naming (domain-based)

Use domain-style module path, not GitHub path:
```go
// go.mod
module blog.it081.com/api
```

For scoped packages:
```json
// web/package.json
{ "name": "@it081/blog-web" }
```

Docker images: `it081/blog-api`, `it081/blog-web`

### 2. Migrations at Project Level

**Do NOT** put migrations inside `internal/repository/`. Goose with `//go:embed` can't reach parent dirs.

**Do** put them at `api/migrations/` and read from filesystem:
```go
// internal/repository/migrate.go
func RunMigrations(db *sql.DB, migrationsDir string) error {
    goose.SetDialect("postgres")
    return goose.Up(db, migrationsDir)
}

// cmd/server/main.go
repository.RunMigrations(db.DB, "migrations")
```

### 3. E2E as Separate Project

Each project owns its own deps and test runner:
- `api/` → `go test ./...`
- `web/` → `npm test` (Vitest)
- `e2e/` → `npm test` (Playwright)

No root `package.json` needed. Each `cd` into its own dir to run tests.

### 4. Playwright Config References Siblings

```ts
// e2e/playwright.config.ts
webServer: [
  { command: "cd ../api && go run ./cmd/server", port: 8080 },
  { command: "cd ../web && node ./node_modules/vite/bin/vite.js --port 3000", port: 3000 },
]
```

### 5. Vite Proxy for Dev

```ts
// web/vite.config.ts
server: {
  proxy: { "/api": { target: "http://localhost:8080", changeOrigin: true } }
}
```

## Pitfalls

- **MCP filesystem** can't create nested dirs — use `terminal mkdir -p` instead
- **`getByText("Send")`** in Playwright matches comment content like "Clicked send" — use `getByRole("button", { name: "Send" })` for specificity
- **Thai Buddhist Era** — `th-TH` locale renders year 2021 as 2564 — test assertions must use Buddhist year
- **Vite 7** changed CLI — `npx vite test --run` no longer works, use `node ./node_modules/vitest/dist/cli.js --run`
- **goose embed** can't reach `../../migrations` — must use filesystem-based approach when migrations are at project level

## References

- `references/interview-assignment.md` — real-world example: IT 08-1 comment board with requirements checklist
- `references/testing-patterns.md` — Fiber handler mock testing, Vitest component tests, Playwright E2E patterns
