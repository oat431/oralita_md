# 01 OpenAPI & Documentation

An undocumented API is a private API — even if it's publicly accessible. OpenAPI (formerly Swagger) is the standard for describing REST APIs in a machine-readable format that generates docs, client SDKs, and tests.

---

## OpenAPI Specification

A single YAML/JSON file that describes your entire API:

```yaml
openapi: 3.0.3
info:
  title: Order Service API
  version: 1.0.0
paths:
  /orders:
    get:
      summary: List all orders
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, shipped, cancelled]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Order'
    post:
      summary: Create an order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: Created
  /orders/{orderId}:
    get:
      summary: Get order by ID
      parameters:
        - name: orderId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
        '404':
          description: Not found
```

---

## The Toolchain

```
OpenAPI Spec ──→ Swagger UI (interactive docs)
              ──→ Codegen (generate client SDKs in 40+ languages)
              ──→ Prism (mock server for testing)
              ──→ Dredd / Schemathesis (contract testing)
              ──→ Stoplight / Redocly (developer portals)
```

---

## Code-First vs Design-First

| Approach | How | Best For |
|----------|-----|----------|
| **Code-First** | Write code, generate spec from annotations | Existing projects, fast iteration |
| **Design-First** | Write spec, generate code from spec | New APIs, cross-team coordination |

### Code-First (Spring Boot + SpringDoc)

```java
@RestController
@RequestMapping("/orders")
public class OrderController {
    
    @Operation(summary = "Get order by ID")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "OK"),
        @ApiResponse(responseCode = "404", description = "Not found")
    })
    @GetMapping("/{orderId}")
    public Order getOrder(@PathVariable String orderId) {
        return orderService.findById(orderId);
    }
}
```

```yaml
# application.yml — Swagger UI at /swagger-ui.html
springdoc:
  api-docs:
    path: /api-docs
  swagger-ui:
    path: /swagger-ui.html
```

---

## What Every API Doc Needs

| Section | Why |
|---------|-----|
| **Authentication** | How to get a token, where to put it |
| **Endpoints** | Methods, paths, parameters, request/response bodies |
| **Error codes** | What each code means and what to do |
| **Rate limits** | How many requests, what happens when exceeded |
| **Examples** | Real request/response pairs — not just schemas |
| **Changelog** | What changed, when, migration guide |

---

## Sources

- OpenAPI Spec — https://spec.openapis.org/oas/latest.html
- Swagger — https://swagger.io/
- SpringDoc — https://springdoc.org/
