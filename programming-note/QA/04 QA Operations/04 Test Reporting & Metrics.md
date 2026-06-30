---
tags:
- programming
- qa
- testing
---

# 04 Test Reporting & Metrics

Testing without reporting is invisible. Stakeholders don't read test code — they need high-level visibility into quality. Metrics and dashboards turn test results into actionable information.

---

## Key Quality Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| **Pass rate** | % of tests passing | > 99% on main branch |
| **Code coverage** | % of code exercised by tests | > 80% line, > 90% for critical paths |
| **Defect density** | Bugs per 1000 lines of code | < 1 (industry avg ~15-50) |
| **Defect escape rate** | % of bugs found in production | < 5% |
| **Mean Time to Detect (MTTD)** | How long to find a bug | < 1 hour (critical), < 24 hours (normal) |
| **Mean Time to Repair (MTTR)** | How long to fix a bug | < 4 hours (critical), < 48 hours (normal) |
| **Test execution time** | Total test suite runtime | < 10 minutes (unit+integration), < 30 min (full) |

---

## Code Coverage

| Coverage Type | What It Measures | Tool |
|--------------|-----------------|------|
| **Line** | % of lines executed | JaCoCo, Istanbul |
| **Branch** | % of if/else branches tested | JaCoCo |
| **Function** | % of functions called | Jest, JaCoCo |
| **Mutation** | % of mutants (code changes) caught by tests | Pitest (Java), Stryker (JS) |

```java
// JaCoCo Maven config
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
        <execution>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
    </executions>
</plugin>
```

### Coverage Targets

| Component | Line Coverage | Branch Coverage |
|-----------|:-----------:|:--------------:|
| Business logic / domain | 90%+ | 90%+ |
| Controllers | 80%+ | 80%+ |
| DTOs / getters/setters | Excluded | Excluded |
| Config classes | Excluded | Excluded |

> **Don't chase 100% coverage.** Coverage measures what's tested, not what's tested well. 100% coverage with no assertions = false confidence.

---

## Test Reports

### JUnit XML → Dashboard

```
JUnit XML ──→ CI platform (GitHub Actions, Jenkins)
           ──→ Allure / ExtentReports (rich HTML reports)
           ──→ SonarQube (trends over time)
```

### Allure Report

```java
@Feature("Orders")
@Story("Create Order")
@Test
void shouldCreateOrder() {
    Allure.step("Given a valid order request", () -> {
        // setup
    });
    Allure.step("When the order is submitted", () -> {
        // execute
    });
    Allure.step("Then the order is confirmed", () -> {
        assertEquals("CONFIRMED", order.getStatus());
    });
}
```

---

## Dashboard & Trend Analysis

```
SonarQube Dashboard:
  ├── Code Coverage: 87% ▲ (was 85% last sprint)
  ├── Duplications: 3% ▼ (was 5%)
  ├── Bugs: 12 (2 critical, 5 major, 5 minor)
  ├── Code Smells: 47
  └── Technical Debt: 3d 4h
```

---

## Sources

- JaCoCo — https://www.jacoco.org/
- SonarQube — https://www.sonarsource.com/products/sonarqube/
- Allure — https://docs.qameta.io/allure-report/
