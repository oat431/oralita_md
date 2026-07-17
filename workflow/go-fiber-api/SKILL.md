---
name: go-fiber-api
description: "Build Go APIs with Fiber v3 + sqlx. Clean architecture, computed fields, standardized responses."
tags: [go, fiber, api, sqlx, postgres]
---

# Go Fiber v3 API

Build REST APIs with Go + Fiber v3 + sqlx + PostgreSQL. Clean architecture: handler → service → repository.

## Project Structure

```
cmd/server/main.go              ← Entry point. Wires deps, starts server.
internal/
├── config/config.go            ← Env-based config (godotenv for .env loading)
├── database/db.go              ← sqlx connection pool setup
├── model/                      ← Domain types, request/response DTOs
│   ├── {entity}.go
│   └── error.go                ← APIError struct
├── repository/{entity}.go      ← SQL queries via sqlx
├── service/{entity}.go         ← Business logic, ownership checks
├── handler/{entity}.go         ← HTTP handlers, validation, error mapping
└── middleware/middleware.go     ← RequestID, Recover, Helmet, Logger
```

## Fiber v3 Pitfalls (verified v3.4.0)

These fields/methods from v2 or docs examples **do not exist** in Fiber v3:

| What you'd expect | v3 reality |
|---|---|
| `c.UserContext()` | `c.Context()` |
| `fiber.Config{DisableStartupMessage: true}` | Field removed. Startup banner is controlled differently. |
| `fiber.Config{Immutable: true}` | Removed in v3. |

### Verified v3 patterns

```go
// Request context
ctx := c.Context()  // NOT c.UserContext()

// Bind JSON body
var req MyStruct
if err := c.Bind().JSON(&req); err != nil { ... }

// Bind query params
var params MyParams
if err := c.Bind().Query(&params); err != nil { ... }

// Error handler
app := fiber.New(fiber.Config{
    BodyLimit: 10 * 1024 * 1024,
    ErrorHandler: func(c fiber.Ctx, err error) error {
        code := fiber.StatusInternalServerError
        if e, ok := err.(*fiber.Error); ok { code = e.Code }
        return c.Status(code).JSON(fiber.Map{"error": err.Error()})
    },
})
```

## Standardized Response Format

```go
type APIResponse struct {
    Data  any             `json:"data"`
    Error any             `json:"error"`
    Meta  *PaginationMeta `json:"meta"`
}

type PaginationMeta struct {
    Page       int `json:"page"`
    PerPage    int `json:"perPage"`
    Total      int `json:"total"`
    TotalPages int `json:"totalPages"`
}
```

Handlers: `ok(c, data, meta)`, `created(c, data)`, `apiErr(c, status, msg, details...)`.

## Database (sqlx)

```go
// Connection pool
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(10)
db.SetConnMaxLifetime(5 * time.Minute)

// Query with context from Fiber
db.QueryRowContext(ctx, query, args...)
db.GetContext(ctx, &dest, query, args...)
```

### Computed fields (not stored in DB)

When a field is derived from other tables (e.g., todolist status from tasks):
- Mark with `db:"-"` in the struct (skip sqlx scanning)
- Compute in service layer after fetching
- For SQL-side computation, use `CASE WHEN ... END` with aggregates
- For filtering computed fields: fetch all, compute, filter in app (ponytail: SQL can't filter computed fields)

## Validation (go-playground/validator)

Fiber v3 has no built-in validator. Wire `go-playground/validator/v10` as `StructValidator`:

```go
// internal/middleware/validator.go
type FiberValidator struct {
    validate *validator.Validate
}

func NewValidator() *FiberValidator {
    return &FiberValidator{validate: validator.New()}
}

func (v *FiberValidator) Validate(out any) error {
    return v.validate.Struct(out)
}
```

Register in app wiring:
```go
f := fiber.New(fiber.Config{
    StructValidator: mw.NewValidator(),
    // ...
})
```

Use struct tags on request DTOs:
```go
type CreateRequest struct {
    Title string `json:"title" validate:"required,max=255"`
    Desc  string `json:"description" validate:"max=1000"`
}
```

`c.Bind().JSON(&req)` automatically calls `Validate()` — returns error if validation fails.

## CORS

```go
import "github.com/gofiber/fiber/v3/middleware/cors"

app.Use(cors.New(cors.Config{
    AllowOrigins:     []string{"*"}, // tighten to gateway origin in production
    AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
    AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
    AllowCredentials: false,
}))
```

Note: `AllowMethods` and `AllowHeaders` are `[]string`, not comma-separated strings.

## Middleware Order

```
RequestID → Recover → Helmet → Logger → Routes
```

Use `fiber/middleware/requestid`, `recover`, `helmet`. Custom logger skips health check noise.

## Graceful Shutdown

```go
go func() {
    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
    <-sigCh
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    _ = app.ShutdownWithContext(ctx)
}()
```

## Testing (mock-based, no DB needed)

### Service interfaces for testability

Define interfaces in the **service** package (consumer defines interface, Go idiom):

```go
// internal/service/interfaces.go
type TodolistRepo interface {
    Create(ctx context.Context, tl *model.Todolist) error
    GetByID(ctx context.Context, id string) (*model.Todolist, error)
    // ...
}

type TaskRepo interface {
    Create(ctx context.Context, t *model.Task) error
    GetByID(ctx context.Context, id string) (*model.Task, error)
    // ...
}
```

Services accept interfaces, not concrete types:
```go
func NewTodolistService(repo TodolistRepo) *TodolistService { ... }
func NewTaskService(taskRepo TaskRepo, todoRepo TodolistRepo) *TaskService { ... }
```

### Mock stores + test app

Create `internal/testutil/helpers.go` with:
- In-memory mock stores (maps + mutex)
- Mock repo adapters that implement the service interfaces
- `NewTestApp()` that wires a Fiber app with mocks (no DB)

```go
func NewTestApp() (*fiber.App, *MockTodolistStore, *MockTaskStore) {
    todoStore := NewMockTodolistStore()
    taskStore := NewMockTaskStore()
    todoRepo := &MockTodoRepo{Store: todoStore, TaskStore: taskStore}
    taskRepo := &MockTaskRepo{Store: taskStore, TodoRepo: todoRepo}
    todoSvc := service.NewTodolistService(todoRepo)
    taskSvc := service.NewTaskService(taskRepo, todoRepo)
    // wire handlers + routes...
}
```

### Handler tests (table-driven)

Use `httptest.NewRequest` (not `http.NewRequest`) — single return value, matches Fiber's `app.Test()`:

```go
func TestCreateTodolist(t *testing.T) {
    app, _, _ := testutil.NewTestApp()
    tests := []struct {
        name       string
        body       map[string]string
        wantStatus int
    }{
        {"valid", map[string]string{"title": "Grocery", "sourceService": "todolist"}, 201},
        {"missing title", map[string]string{"sourceService": "todolist"}, 400},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            body, _ := json.Marshal(tt.body)
            req := httptest.NewRequest("POST", "/api/v1/todolists", bytes.NewReader(body))
            req.Header.Set("Content-Type", "application/json")
            resp, err := app.Test(req)
            require.NoError(t, err)
            assert.Equal(t, tt.wantStatus, resp.StatusCode)
        })
    }
}
```

### Verification

```bash
go build ./cmd/server/   # compiles
go vet ./...             # static analysis
go test ./...            # tests
make test                # all three via Makefile
```

## Dependencies

```
github.com/gofiber/fiber/v3          # HTTP framework
github.com/jmoiron/sqlx              # SQL extensions
github.com/lib/pq                    # Postgres driver
github.com/go-playground/validator/v10 # Struct validation (wire as StructValidator)
github.com/joho/godotenv             # .env file loading (one-liner in config.Load())
```

## Wiring Pattern (internal/app/)

Keep main.go thin (~30 lines). All wiring lives in `internal/app/app.go`:

```go
// Single entity
func New(cfg config.Config) (*App, error) {
    db, _ := database.Connect(cfg.DBUrl)
    repo := repository.NewRepo(db)
    svc := service.NewService(repo)
    h := handler.NewHandler(svc)
    // ...
}

// Multiple entities with shared deps (e.g., todolist + task)
func New(cfg config.Config) (*App, error) {
    db, _ := database.Connect(cfg.DBUrl)
    todoRepo := repository.NewTodolistRepository(db)
    taskRepo := repository.NewTaskRepository(db)
    todoSvc := service.NewTodolistService(todoRepo)
    taskSvc := service.NewTaskService(taskRepo, todoRepo) // task needs todoRepo for ownership checks
    todoH := handler.NewTodolistHandler(todoSvc)
    taskH := handler.NewTaskHandler(taskSvc)
    // ...
}
```

**Ownership pattern:** child entity (task) verifies ownership via parent (todolist). Service layer calls parent repo's `GetByID` and checks `ownedBy`.

Main becomes: load config → `app.New(cfg)` → listen → graceful shutdown.

## Makefile

Template at `templates/Makefile`. Copy and adjust. Targets: `run`, `build`, `test`, `vet`, `lint`, `dev` (air), `clean`.

## v2 → v3 Migration

See `references/fiber-v3-migration.md` for confirmed breaking changes.

## Spec-Driven Development Workflow

When user provides numbered spec docs (00 Overview, 01 Data Model, 02 API Spec, 03 Logic):

1. **Read all specs first** — understand scope, data model, endpoints, business rules
2. **Check DB schema** — verify tables match spec (use Postgres MCP if available). Check column types, constraints, indexes, FK cascades.
3. **Review checklist** — load the framework-specific checklist (e.g., `fiber-v3-api.md`) to know what's expected
4. **Plan PRs** — group related changes into logical PRs. Present the plan to the user before implementing.
5. **Create issues for future work** — create GitHub issues for out-of-scope items. User decides priority.
6. **Implement per PR** — branch → code → build → vet → test → commit → push → create PR → switch back to main
7. **Verify after each PR** — `make build && make vet && make test` must pass

Key rules:
- MVP scope is defined by the spec. Don't implement out-of-scope features unless asked.
- When user says "create issue", create the issue — don't implement it.
- Group related checklist items into PRs (e.g., "mvp polish" = validation + CORS + linter + hot reload).
- Each PR body should reference which checklist items it covers and which issues it closes.

### PR Grouping Strategy

Group by theme, not by individual checklist item:

| PR | Theme | Typical items |
|----|-------|---------------|
| #1 | MVP Polish | Validation, CORS, linter, hot reload, context propagation |
| #2 | Production Readiness | Migrations, Dockerfile, health check, logging |
| #3 | Tests | Handler tests, service tests, test helpers |
| #N | Features | One feature per PR (e.g., tasks CRUD) |
| #X | Auth + Observability | JWT, rate limiter, Swagger, OpenTelemetry |

### Concrete Example (tiny-mchwa-api)

| PR | Title | Issue Closed |
|----|-------|-------------|
| #1 | feat: mvp polish | — |
| #6 | feat: tasks CRUD + computed status | #4 |
| #7 | feat: add tests + refactor services to interfaces | #3 |
| — | feat: production readiness | #2 (pending) |
| — | feat: auth + observability | #5 (pending) |

PRs #1, #6, #7 ship independently. Issues #2, #5 are future work.

### Issue Template for Feature Work

```markdown
## Tasks
- [ ] Task 1 — description
- [ ] Task 2 — description

## Related
Spec: [[02 API Spec]], checklist section name
```

## See Also

- User's checklist: `F:\projects\orlita_md\project-checklist\backend-checklist\fiber-v3-api.md`
- Fiber v3 docs: https://docs.gofiber.io/
- **Frontend:** When user wants a React frontend for the API, see `references/bun-react-frontend.md`
- **GitHub MCP:** When GitHub MCP is available, use it for branch/PR/issue creation. See `references/github-mcp-workflow.md`
