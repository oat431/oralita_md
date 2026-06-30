---
tags:
- api
- programming
- protocols
---

# 02 GraphQL

GraphQL flips REST on its head: instead of the server defining fixed endpoints, the client asks for exactly the data it needs — no over-fetching, no under-fetching, one request.

---

## REST vs GraphQL

| | REST | GraphQL |
|---|------|---------|
| **Endpoint** | Many (`/users`, `/users/1/posts`) | One (`/graphql`) |
| **Data shape** | Server decides | Client decides |
| **Over-fetching** | Common (user endpoint returns 20 fields, you need 3) | Never |
| **Under-fetching** | Common (need user + posts → 2 requests) | Never (nested queries in one request) |
| **Caching** | HTTP caching built-in | Requires custom solution (Apollo, Relay) |
| **Versioning** | URL/header versioning | No versioning — add fields, deprecate old ones |

---

## Core Concepts

### Query — Read Data

```graphql
# Client asks for exactly what it needs
query {
  user(id: "123") {
    name
    email
    posts(last: 3) {
      title
      comments {
        author { name }
        text
      }
    }
  }
}
```

### Mutation — Write Data

```graphql
mutation {
  createOrder(input: {
    userId: "123"
    items: [{ productId: "abc", quantity: 2 }]
  }) {
    id
    status
    total
  }
}
```

### Subscription — Real-Time

```graphql
subscription {
  orderStatusChanged(orderId: "456") {
    status
    updatedAt
  }
}
```

---

## Schema-First Design

Define the schema before writing code. The schema is the contract.

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts(last: Int = 10): [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
}

type Query {
  user(id: ID!): User
  users: [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(name: String!, email: String!): User!
  createPost(title: String!, content: String!, authorId: ID!): Post!
}

type Subscription {
  postCreated: Post!
}
```

---

## The N+1 Problem — And DataLoader

```graphql
# Query returns 10 posts. Each post needs its author.
# Naive: 1 query for posts + 10 queries for authors = 11 queries
```

**DataLoader** batches and caches requests:

```java
// DGS (Netflix GraphQL) — DataLoader example
@DgsData(parentType = "Post", field = "author")
public CompletableFuture<User> author(DgsDataFetchingEnvironment dfe) {
    Post post = dfe.getSource();
    return dataLoaderRegistry.getDataLoader("users")
        .load(post.getAuthorId());
}
```

DataLoader collects all author IDs, makes ONE batch query, and distributes results back.

---

## Tools

| Tool | What It Does |
|------|-------------|
| **Apollo Server/Client** | JavaScript GraphQL ecosystem |
| **Netflix DGS** | GraphQL framework for Spring Boot |
| **Relay** | Facebook's GraphQL client (with strict schema conventions) |
| **GraphQL Code Generator** | Generate TypeScript/Java types from schema |
| **Apollo Studio** | Schema registry, explorer, metrics |
| **GraphiQL** | In-browser IDE for exploring GraphQL APIs |

---

## When NOT to Use GraphQL

| Scenario | Better Alternative |
|----------|-------------------|
| Simple CRUD API | REST — less complexity |
| High-performance service-to-service | gRPC — smaller payload, faster |
| File uploads | REST — GraphQL adds no value here |
| Public API with heavy caching needs | REST — HTTP caching is battle-tested |

---

## Sources

- GraphQL Spec — https://spec.graphql.org/
- Netflix DGS — https://netflix.github.io/dgs/
- Apollo — https://www.apollographql.com/
