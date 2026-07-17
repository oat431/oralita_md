# Fiber v3 Migration: Breaking Changes from v2

## Confirmed (tested with v3.4.0)

### Context
```go
// v2: c.UserContext()
// v3: c.Context()
```

### Body Binding
```go
// v2: c.BodyParser(&req)
// v3: c.Bind().JSON(&req)
```

### Query Binding
```go
// v2: c.QueryParser(&params)
// v3: c.Bind().Query(&params)
```

### Shutdown
```go
// v2: app.Shutdown()
// v3: app.ShutdownWithContext(ctx)
```

### Config Fields Removed
- `DisableStartupMessage` — removed, no replacement
- `Immutable` — removed

### Middleware Imports
```go
// v2: "github.com/gofiber/fiber/v2/middleware/cors"
// v3: "github.com/gofiber/fiber/v3/middleware/cors"
```

## Unchanged in v3
- `c.Params("id")`, `c.SendStatus(204)`, `c.Status(code).JSON(data)`
- `fiber.New(fiber.Config{ErrorHandler: ...})`
- `app.Get()`, `app.Post()`, `app.Group()`
