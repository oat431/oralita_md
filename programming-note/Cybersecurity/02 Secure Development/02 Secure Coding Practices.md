---
tags:
- cybersecurity
- programming
- security
---

# 02 Secure Coding Practices

Most vulnerabilities come from a handful of coding mistakes. Fix these patterns and you eliminate the majority of attack surface.

---

## 1. Input Validation — Never Trust the Client

```java
// ❌ Trusting user input
@PostMapping("/users")
public User createUser(@RequestBody User user) {
    return userRepo.save(user);  // What if email = "<script>..." ?
}

// ✅ Validate EVERY input
@PostMapping("/users")
public User createUser(@Valid @RequestBody CreateUserRequest request) {
    return userService.create(request);
}

public class CreateUserRequest {
    @NotBlank @Email
    private String email;
    
    @NotBlank @Size(min = 8, max = 100)
    private String password;
    
    @NotBlank @Pattern(regexp = "^[a-zA-Z0-9_-]{3,30}$")
    private String username;
}
```

| Rule | Example |
|------|---------|
| **Whitelist, not blacklist** | Allow `[a-zA-Z0-9]`, don't try to block "bad characters" |
| **Validate type, length, range** | Integer? Must be 1–1000. String? Max 255 chars. |
| **Validate at boundary** | API layer validates. Service layer re-validates (defense in depth). |

---

## 2. Output Encoding

```java
// ❌ XSS vulnerability
return "<div>" + userInput + "</div>";

// ✅ Encode for context
// HTML context
return "<div>" + HtmlUtils.htmlEscape(userInput) + "</div>";

// JavaScript context
return "var name = '" + JavaScriptUtils.javaScriptEscape(userInput) + "'";

// URL context
return URLEncoder.encode(userInput, StandardCharsets.UTF_8);
```

---

## 3. Parameterized Queries — ALWAYS

```java
// ❌ SQL Injection
String sql = "SELECT * FROM users WHERE name = '" + name + "'";

// ✅ Parameterized
String sql = "SELECT * FROM users WHERE name = ?";
jdbcTemplate.query(sql, name);

// ✅ JPA / Hibernate
@Query("SELECT u FROM User u WHERE u.name = :name")
User findByName(@Param("name") String name);  // Auto-parameterized

// ✅ Dynamic queries — use Criteria API, never string concatenation
```

---

## 4. File Upload Safety

```java
// ✅ Validate file upload
@PostMapping("/upload")
public String upload(@RequestParam("file") MultipartFile file) {
    // 1. Check file size
    if (file.getSize() > MAX_SIZE) throw new FileTooLargeException();
    
    // 2. Check MIME type (whitelist)
    String contentType = file.getContentType();
    if (!ALLOWED_TYPES.contains(contentType)) throw new InvalidFileException();
    
    // 3. Check magic bytes (not just extension — extension can be faked)
    byte[] magicBytes = Arrays.copyOf(file.getBytes(), 4);
    if (!isAllowedMagicBytes(magicBytes)) throw new InvalidFileException();
    
    // 4. Store OUTSIDE web root with random filename
    String storedName = UUID.randomUUID().toString();
    Path target = Paths.get("/var/uploads/" + storedName);
    file.transferTo(target);
    
    // 5. Never use user-provided filename for storage
    return storedName;  // Return random name, not original
}
```

---

## 5. Error Handling — Don't Leak Internals

```java
// ❌ Leaks stack trace to client
@ExceptionHandler(Exception.class)
public ResponseEntity<String> handle(Exception e) {
    return ResponseEntity.status(500).body(e.getMessage());  // Stack trace exposed!
}

// ✅ Log internally, return safe message to client
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handle(Exception e) {
    log.error("Internal error: {}", e.getMessage(), e);
    return ResponseEntity.status(500)
        .body(new ErrorResponse("Internal server error", referenceId));
}
```

---

## 6. Logging — Log Enough, But Never Secrets

```java
// ✅ Good logging
log.info("Order {} created by user {}", orderId, userId);
log.warn("Failed login attempt for user {}", username);
log.error("Payment failed for order {}", orderId, e);

// ❌ NEVER log secrets
log.info("User login: password={}", password);   // NO
log.info("API key: {}", apiKey);                  // NO
log.info("JWT: {}", token);                       // NO
```

---

## Secure Coding Checklist

- [ ] All inputs validated (type, length, range, format)
- [ ] All database queries parameterized
- [ ] All output encoded for context (HTML, JS, URL)
- [ ] File uploads: size limit, MIME check, magic bytes, random names
- [ ] Errors return safe messages (no stack traces)
- [ ] Logs never contain secrets
- [ ] HTTPS everywhere (HSTS enabled)

---

## Sources

- OWASP Input Validation Cheat Sheet
- OWASP Logging Cheat Sheet
