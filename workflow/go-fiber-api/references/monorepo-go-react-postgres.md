# Mono-repo: Go Fiber API + React Web + PostgreSQL

When the user wants API and web in a single repository (interview tasks, small projects, demos).

## Directory Structure

```
project-root/
├── api/                          ← Go Fiber API
│   ├── cmd/server/main.go
│   ├── internal/
│   │   ├── config/config.go
│   │   ├── handler/
│   │   ├── middleware/
│   │   ├── model/
│   │   └── repository/
│   ├── migrations/               ← SQL migrations (project level, easy to find)
│   │   └── 001_create_*.sql
│   ├── go.mod
│   ├── go.sum
│   ├── .env.example
│   └── Dockerfile
├── web/                          ← React (Vite + TypeScript)
│   ├── src/
│   │   ├── components/
│   │   ├── services/api.ts       ← Typed fetch wrapper
│   │   ├── types.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   ├── .env.example
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── nginx.conf                ← For Docker production build
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## docker-compose.yml (minimal)

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: ./api
    image: company/api        # tag for registry
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: "postgres://postgres:postgres@postgres:5432/app_db?sslmode=disable"
    depends_on:
      postgres:
        condition: service_healthy

  web:
    build: ./web
    image: company/web
    ports:
      - "5173:80"
    depends_on:
      - api

volumes:
  pgdata:
```

**Pattern:** Only Postgres in compose for dev. API and web run locally via `go run` / `npm run dev`. Add api+web to compose for production-like environments only.

### Port Conflict Pre-check

Before `docker compose up`, check if 5432 is already in use:
```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}' | grep 5432
```
If an existing Postgres is running, either:
- Reuse it: `docker exec <container> psql -U postgres -c "CREATE DATABASE dbname;"`
- Change the compose port mapping (e.g. `"5433:5432"`)

Don't let `docker compose up` fail on bind — bad first impression in interviews.

## Naming Convention (company-style)

When the project is for a company or interview, use domain-style naming instead of generic names:

| Component | Generic (bad) | Company-style (good) |
|---|---|---|
| Go module | `interview-question-009/api` | `blog.4h4p.com/api` |
| npm package | `interview-question-009-web` | `@4h4p/blog-web` |
| Docker images | _(none)_ | `4h4p/blog-api`, `4h4p/blog-web` |
| README title | "interview-question-009" | "blog.4h4p.com — Comment Board" |

The Go module path should look like a real company monorepo. `domain.com/project` is the standard pattern.

### Renaming an existing module

When you need to rename a Go module (e.g., from generic to domain-style):

1. Update `go.mod` module line
2. Find-and-replace all imports: `grep -r "old/module/path" --include="*.go" -l`
3. Update each file's imports
4. `go mod tidy` to verify
5. Update `package.json` name, docker-compose image tags, README

```bash
# Find all files with old import
grep -r "interview-question-009/api" --include="*.go" -l
# Returns: cmd/server/main.go, internal/handler/..., internal/repository/..., internal/middleware/...
```

Typical files that need import updates: `cmd/server/main.go`, `internal/handler/*.go`, `internal/repository/*.go`, `internal/middleware/*.go`.

## Go Module Init

```bash
cd api && go mod init domain.com/project
```

For mono-repo, use the project's domain as the module path (e.g. `blog.4h4p.com/api`). This looks professional and follows Go conventions.

## Goose Migrations — Two Approaches

### Option A: Filesystem path (preferred for mono-repo / interviews)

Migrations live at `api/migrations/` (project level, easy for reviewers to find):

```
api/
├── migrations/001_create_comments.sql   ← visible, reviewable
└── internal/repository/migrate.go       ← reads from filesystem
```

```go
// internal/repository/migrate.go
func RunMigrations(db *sql.DB, migrationsDir string) error {
    if err := goose.SetDialect("postgres"); err != nil { return err }
    if err := goose.Up(db, migrationsDir); err != nil { return err }
    return nil
}
```

Called from `main.go`:
```go
if err := repository.RunMigrations(db.DB, "migrations"); err != nil { ... }
```

Goose resolves the path relative to the working directory, so `go run ./cmd/server` from `api/` picks up `api/migrations/` automatically.

**Why this over embed:** Migrations are a project-level concern. Burying them in `internal/repository/migrations/` makes them invisible to reviewers. The filesystem approach is simpler, more discoverable, and works fine for any project that runs from its source directory.

**Pitfall — sqlx vs stdlib DB:** Goose's `Up()` takes `*sql.DB`, not `*sqlx.DB`. When using sqlx, pass `db.DB`:
```go
// ✅ correct
repository.RunMigrations(db.DB, "migrations")
// ❌ wrong — type mismatch
repository.RunMigrations(db, "migrations")
```

### Option B: embed.FS (for standalone binary distribution)

Use when you need a single binary with no external files (e.g., `scratch` Docker image):

```go
// internal/repository/migrate.go
//go:embed migrations/*.sql
var embedMigrations embed.FS

func RunMigrations(db *sqlx.DB) error {
    goose.SetBaseFS(embedMigrations)
    if err := goose.SetDialect("postgres"); err != nil { return err }
    if err := goose.Up(db.DB, "migrations"); err != nil { return err }
    return nil
}
```

**Pitfall:** The `migrations/` directory must be inside the package directory containing the `//go:embed` directive (e.g. `internal/repository/migrations/`), NOT at the project root. Go embed is relative to the source file, not the module root.

### Migration file (both approaches)

`api/migrations/001_create_comments.sql`:
```sql
-- +goose Up
CREATE TABLE IF NOT EXISTS comments (
    id         BIGSERIAL    PRIMARY KEY,
    user_name  VARCHAR(100) NOT NULL,
    content    TEXT         NOT NULL,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_comments_created_at ON comments (created_at DESC);

-- +goose Down
DROP INDEX IF EXISTS idx_comments_created_at;
DROP TABLE IF EXISTS comments;
```

Add indexes that match your query patterns (e.g., `ORDER BY created_at DESC` needs an index on `created_at DESC`).

This runs automatically on server startup — no manual migration step needed.

## Vite Proxy Config (web → api)

```ts
// web/vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',  // match your API PORT env
        changeOrigin: true,
      },
    },
  },
})
```

## API CORS for Dev

```go
app.Use(cors.New(cors.Config{
    AllowOrigins: []string{"http://localhost:5173"},
    AllowMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
    AllowHeaders: []string{"Origin", "Content-Type", "Authorization"},
}))
```

## .env Setup (all three projects)

Each project in the mono-repo has its own `.env` + `.env.example`:

```bash
api/.env.example     # PORT, DATABASE_URL, FRONTEND_URL
web/.env.example     # IT081_API_URL
e2e/.env.example     # API_URL, WEB_URL
```

Add all to `.gitignore`:
```
api/.env
web/.env
e2e/.env
```

### API: godotenv

`os.Getenv()` does NOT read `.env` files — it only reads shell environment variables. Add `godotenv`:

```go
import "github.com/joho/godotenv"

func Load() *Config {
    _ = godotenv.Load()  // ignore error if missing
    return &Config{
        Port: getEnv("PORT", "8080"),
        // ...
    }
}
```

**Pitfall:** `godotenv.Load()` does NOT override existing env vars. This is useful — Playwright can pass `PORT=8080` as an env var and it takes precedence over `.env`'s `PORT=8000`.

### Web: Vite proxy reads from env

Don't hardcode the proxy target — read from the env var so changing ports only requires editing `.env`:

```ts
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "IT081_");
  const apiUrl = env.IT081_API_URL || "http://localhost:8080";

  return {
    envPrefix: "IT081_",
    server: {
      proxy: { "/api": { target: apiUrl, changeOrigin: true } },
    },
  };
});
```

### Custom Env Prefix

Replace the default `VITE_` prefix with a company/project prefix:

```ts
envPrefix: "IT081_",  // import.meta.env.IT081_API_URL
```

Only variables with this prefix are exposed to the client bundle.

### E2E: dotenv for Playwright

Playwright doesn't auto-load `.env`. Add `dotenv`:

```bash
cd e2e && npm install dotenv
```

```ts
// e2e/playwright.config.ts
import dotenv from "dotenv";
import path from "path";
dotenv.config({ path: path.resolve(__dirname, ".env") });

const apiUrl = process.env.API_URL || "http://localhost:8000";
```

Same pattern in test files that need the API URL (e.g., cleanup functions).

## Startup Order

```bash
# 1. Database
docker compose up -d db    # or reuse existing local-postgres

# 2. API (terminal 1)
cd api && go run ./cmd/server

# 3. Web (terminal 2)
cd web && npm run dev
```

## Interview / Small Project Adjustments

When using this for an interview or demo (not production):

- **Skip:** OpenTelemetry, Prometheus, Sentry, Playwright E2E, Swagger, rate limiter
- **Keep:** Error handler, CORS, basic validation, health endpoint, structured responses
- **Simplify:** No auth unless required. No pagination unless list is long.
- **Focus on:** Working UI that matches the reference screenshot, clean code structure, proper DB schema
- **Database:** One table is fine. `id`, user name, content, `created_at`. Don't over-normalize.
- **Architecture:** For tiny projects, skip the service layer. Handler calls repository directly: `handler → repository → DB`. The three-layer pattern (handler → service → repository) is for projects with business logic between HTTP and data access. A comment board has none.

## Extracting UI Reference from .docx

Interview tasks often include a .docx with embedded screenshots:

```python
import zipfile
with zipfile.ZipFile('task.docx', 'r') as z:
    media = [f for f in z.namelist() if f.startswith('word/media/')]
    for m in media:
        z.extract(m, 'extracted/')
        print(f'Extracted: {m}')
```

Always check the extracted image — it defines the acceptance criteria.

## Testing (three layers — each as its own project)

For interview projects, three test layers score bonus points and show systems thinking. Each layer is its own project within the monorepo:

```
├── api/       → go test ./...
├── web/       → npm test (Vitest)
└── e2e/       → npm test (Playwright) — own package.json, own deps
```

No root `package.json` needed. Each project owns its deps and test runner.

### Layer 1: Go API unit tests (testify)

Test handlers with a mock repository — no DB needed:

```go
// internal/handler/comment_handler_test.go
type mockRepo struct {
    comments []model.Comment
    nextID   int64
    err      error // inject for negative tests
}

func (m *mockRepo) List(_ context.Context) ([]model.Comment, error) {
    if m.err != nil { return nil, m.err }
    return m.comments, nil
}
```

Key patterns:
- Use `fiber.Config{ErrorHandler}` in test app setup (matches production)
- `httptest.NewRequest` + `app.Test(req)` — no real server needed
- Table-driven tests for CRUD: empty list, create success, create validation, delete success, delete not found, delete invalid ID
- **Pitfall:** Use `repository.ErrNotFound` for 404 tests, NOT `assert.AnError` — the handler checks for the sentinel error specifically

**Pitfall — nil slice → JSON null:** `var s []T` stays nil when `sqlx.SelectContext` returns no rows. JSON serializes `nil` as `null`, not `[]`. Use `make([]T, 0)`:

```go
// ❌ returns null when empty
func (r *repo) List(ctx context.Context) ([]model.Comment, error) {
    var comments []model.Comment
    err := r.db.SelectContext(ctx, &comments, "SELECT ...")
    return comments, err
}

// ✅ returns [] when empty
func (r *repo) List(ctx context.Context) ([]model.Comment, error) {
    comments := make([]model.Comment, 0)
    err := r.db.SelectContext(ctx, &comments, "SELECT ...")
    return comments, err
}
```

This matters for E2E cleanup — the test's `clearComments` function iterates the response with `for...of`, and `null` throws `TypeError: not iterable`.

```bash
cd api && go test ./internal/handler/ -v -count=1
```

### Layer 2: React component tests (Vitest + RTL)

Install deps:
```bash
cd web && npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

Vite 7 config with Vitest:
```ts
// vite.config.ts — note: vitest config goes IN the same file
/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
    css: true,
  },
});
```

Setup file:
```ts
// src/test/setup.ts
import "@testing-library/jest-dom/vitest";
```

Run command — Vite 7 broke `vite test`, use vitest directly:
```bash
node ./node_modules/vitest/dist/cli.js --run
```

**Pitfall — Vite 7 CLI:** `npx vite test --run` throws `CACError: Unknown option`. The `vitest` binary is separate from `vite` in v7. Use `node ./node_modules/vitest/dist/cli.js --run`.

**Pitfall — Thai Buddhist Era:** `th-TH` locale renders year as Gregorian + 543. A date `2021-10-16` renders as "16 ตุลาคม **2564**" not "2021". Tests expecting `/2021/` will fail.

Test patterns:
- Mock API module: `vi.mock("../../services/api", () => ({ createComment: vi.fn() }))`
- Use `userEvent.type(input, "Hello{enter}")` for Enter-to-submit tests
- Check `input.toHaveValue("")` after submit to verify clearing

### Layer 3: E2E (Playwright — separate project)

E2E lives in `e2e/` as its own project with its own `package.json`:

```
e2e/
├── comment-flow.spec.ts
├── playwright.config.ts    ← references sibling dirs with ../
└── package.json            ← own deps (@playwright/test)
```

Install:
```bash
cd e2e && npm install && npx playwright install chromium
```

Playwright config — uses `cd ../` to reach sibling projects:
```ts
// e2e/playwright.config.ts
export default defineConfig({
  testDir: ".",
  use: { baseURL: "http://localhost:3000" },
  webServer: [
    {
      command: "cd ../api && go run ./cmd/server",
      port: 8080,
      reuseExistingServer: true,
      env: { PORT: "8080", DATABASE_URL: "postgres://..." },
    },
    {
      command: "cd ../web && node ./node_modules/vite/bin/vite.js --port 3000",
      port: 3000,
      reuseExistingServer: true,
    },
  ],
});
```

E2E test patterns:
- **Cleanup before each test** — stale data from prior runs causes strict mode violations. Add a `beforeEach` that clears the DB via API:
  ```ts
  async function clearComments(request: APIRequestContext) {
    const res = await request.get(`${API_URL}/api/v1/comments`);
    if (res.ok()) {
      const comments = await res.json();
      if (Array.isArray(comments)) {
        for (const c of comments) {
          await request.delete(`${API_URL}/api/v1/comments/${c.id}`);
        }
      }
    }
  }
  test.beforeEach(async ({ request }) => { await clearComments(request); });
  ```
- Use `getByRole("button", { name: "Send" })` not `getByText("Send")` — stale data causes strict mode violations
- Use `getByRole("heading", { name: "ความคิดเห็น" })` not `getByText("ความคิดเห็น")` — the empty state text also contains the substring
- Test: page loads, post comment via Enter, post via click, verify order (newest first), delete comment
- `reuseExistingServer: true` — reuses your local dev servers if already running

```bash
npx playwright test --reporter=list
```

### Running all tests

Each project runs independently — no root package.json needed:
```bash
cd api && go test ./...
cd web && npm test
cd e2e && npm test
```

Or add a root `package.json` with scripts if you prefer one-command orchestration.

## Tool Pitfalls (Windows / Hermes-specific)

### MCP filesystem `create_directory` fails on nested paths

The MCP filesystem tool can't create nested directories when parent doesn't exist (unlike `mkdir -p`). Use terminal instead:

```bash
mkdir -p api/cmd/server api/internal/handler api/internal/repository web/src/components
```

### `vite build` triggers "long-lived process" detection

The Hermes terminal tool detects `vite` or `npx vite` as a dev server and blocks the command. Workaround — invoke the binary directly:

```bash
cd web && node ./node_modules/vite/bin/vite.js build
```

### TypeScript CSS import error (TS2307)

`import './index.css'` fails with `Cannot find module './index.css'` in strict TS. Fix: create `src/vite-env.d.ts`:

```ts
/// <reference types="vite/client" />
```

This tells TypeScript that `.css` files are valid Vite-importable modules.

### `go mod tidy` pulls goose's transitive deps

`goose/v3` v3.27+ requires Go 1.25+ (it pulls SQLite + MySQL drivers). This auto-upgrades the `go` directive in `go.mod`. Not a problem — just let it happen. The final binary is still `CGO_ENABLED=0` if you only use Postgres.
