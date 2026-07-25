# Testing Patterns for Full-Stack Monorepo

## Go API — Handler Tests with Mock Repository

Create a mock that implements the repository interface:

```go
type mockRepo struct {
    comments []model.Comment
    nextID   int64
    err      error // inject for negative tests
}

func (m *mockRepo) List(_ context.Context) ([]model.Comment, error) {
    if m.err != nil { return nil, m.err }
    return m.comments, nil
}

func (m *mockRepo) Create(_ context.Context, c *model.Comment) error {
    if m.err != nil { return m.err }
    m.nextID++
    c.ID = m.nextID
    c.CreatedAt = time.Date(2021, 10, 16, 16, 0, 0, 0, time.UTC)
    m.comments = append(m.comments, *c)
    return nil
}
```

Use Fiber's `app.Test(httptest.NewRequest(...))` — no real server needed:
```go
app := fiber.New()
h := NewCommentHandler(mockRepo)
api := app.Group("/api/v1")
api.Get("/comments", h.List)
api.Post("/comments", h.Create)

resp, _ := app.Test(httptest.NewRequest("POST", "/api/v1/comments", payload))
assert.Equal(t, 201, resp.StatusCode)
```

For 404 tests, return `repository.ErrNotFound` (not `assert.AnError`).

## React — Vitest + React Testing Library

Setup (`vite.config.ts`):
```ts
test: {
  globals: true,
  environment: "jsdom",
  setupFiles: "./src/test/setup.ts",
  css: true,
}
```

Setup file (`src/test/setup.ts`):
```ts
import "@testing-library/jest-dom/vitest";
```

Mock API calls:
```ts
vi.mock("../../services/api", () => ({
  createComment: vi.fn(),
}));
```

Test user interactions with `@testing-library/user-event`:
```ts
await userEvent.type(input, "Hello{enter}");
expect(mockCreate).toHaveBeenCalledWith("Blend 285", "Hello");
```

## Playwright E2E

Use role-based selectors over text selectors:
```ts
// BAD — matches "Clicked send" comment content
await page.getByText("Send").click();

// GOOD — matches only the button
await page.getByRole("button", { name: "Send" }).click();
```

Playwright starts both API and Web via `webServer` config:
```ts
webServer: [
  { command: "cd ../api && go run ./cmd/server", port: 8080 },
  { command: "cd ../web && node ./node_modules/vite/bin/vite.js --port 3000", port: 3000 },
]
```

## Locale Gotcha — Thai Buddhist Era

`th-TH` locale adds 543 to the year:
- 2021 → 2564
- 2026 → 2569

Test assertions must use Buddhist year:
```ts
expect(screen.getByText(/16 ตุลาคม 2564/)).toBeInTheDocument();
```

Date format output:
```ts
d.toLocaleDateString("th-TH", { day: "numeric", month: "long", year: "numeric" })
// "16 ตุลาคม 2564"
```
