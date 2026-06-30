---
tags:
- api
- programming
- protocols
---

# 01 REST API Design

REST is the dominant API architecture on the web. When done right, it's simple, cacheable, and scalable. When done wrong, it's a mess of inconsistent URLs and broken conventions.

---

## The Six Constraints of REST

| Constraint | What It Means |
|-----------|--------------|
| **Client-Server** | UI is separate from data storage. Client and server evolve independently. |
| **Stateless** | Each request contains all info needed. No server-side session. |
| **Cacheable** | Responses declare whether they can be cached. `Cache-Control` headers. |
| **Uniform Interface** | Resources identified by URIs. Self-descriptive messages. HATEOAS. |
| **Layered System** | Client doesn't know if it's talking to the server or an intermediary. |
| **Code on Demand** (optional) | Server can send executable code (JavaScript) to the client. |

---

## Resource Naming

> **Nouns, not verbs. Collections are plural.**

| ❌ | ✅ |
|----|-----|
| `GET /getOrders` | `GET /orders` |
| `POST /createUser` | `POST /users` |
| `GET /getOrderById?id=123` | `GET /orders/123` |
| `POST /deleteOrder` | `DELETE /orders/123` |

---

## HTTP Methods

| Method | Action | Idempotent? | Example |
|--------|--------|:----------:|---------|
| **GET** | Read | ✅ | `GET /orders/123` |
| **POST** | Create | ❌ | `POST /orders` |
| **PUT** | Replace (full update) | ✅ | `PUT /orders/123` |
| **PATCH** | Partial update | ❌ | `PATCH /orders/123` |
| **DELETE** | Delete | ✅ | `DELETE /orders/123` |
| **HEAD** | Like GET, no body | ✅ | `HEAD /orders/123` |
| **OPTIONS** | What methods are allowed | ✅ | `OPTIONS /orders` |

---

## Status Codes

| Code | Meaning | When |
|:----:|---------|------|
| **200** | OK | Successful GET, PUT, PATCH |
| **201** | Created | Successful POST — include `Location` header |
| **204** | No Content | Successful DELETE |
| **400** | Bad Request | Invalid input, validation error |
| **401** | Unauthorized | Missing or invalid credentials |
| **403** | Forbidden | Authenticated but not allowed |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Duplicate, version conflict |
| **422** | Unprocessable | Semantic error in request body |
| **429** | Too Many Requests | Rate limited |
| **500** | Internal Server Error | Something broke on the server |

---

## Versioning

| Strategy | Example | Pros/Cons |
|----------|---------|-----------|
| **URL path** | `/v1/orders` | Simple, visible. "Violates" REST (URLs identify resources, not versions). |
| **Header** | `Accept: application/vnd.api+json;version=1` | Clean URLs. Harder to test in browser. |
| **Query param** | `/orders?version=1` | Simple. Pollutes query params. |
| **Content negotiation** | `Accept: application/vnd.myapp.v1+json` | Most RESTful. Most complex. |

> **Most teams use URL path versioning.** It's the simplest and clients understand it instantly.

---

## Pagination

```json
// Request: GET /orders?page=2&limit=50

// Response:
{
  "data": [...],
  "meta": {
    "page": 2,
    "limit": 50,
    "total": 1247,
    "totalPages": 25,
    "next": "/orders?page=3&limit=50",
    "prev": "/orders?page=1&limit=50"
  }
}
```

| Pattern | When |
|---------|------|
| **Offset-based** (`page`/`limit`) | Simple, common. Inconsistent if data changes during pagination. |
| **Cursor-based** (`after`/`before`) | Stable. Better for real-time data (Twitter, Slack). |

---

## HATEOAS (Hypermedia as the Engine of Application State)

The API response includes links to related actions. The client navigates the API by following links — no hardcoded URLs.

```json
{
  "id": 123,
  "status": "shipped",
  "_links": {
    "self": { "href": "/orders/123" },
    "cancel": { "href": "/orders/123/cancel" },
    "customer": { "href": "/customers/456" }
  }
}
```

> HATEOAS is the most violated REST constraint. Most APIs skip it. It's powerful but adds complexity. Include it only if clients genuinely benefit from discoverability.

---

## Sources

- Fielding, Roy. *Architectural Styles*, 2000.
- Microsoft REST API Guidelines — https://github.com/microsoft/api-guidelines
