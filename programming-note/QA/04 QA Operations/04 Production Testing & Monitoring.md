---
tags:
- programming
- qa
- testing
---

# 04 Production Testing & Monitoring

Testing doesn't stop at deployment. Production is the ultimate test environment — real users, real data, real edge cases. Production testing catches what pre-production testing misses.

---

## Testing in Production (Yes, Really)

| Technique | What It Does | Risk |
|-----------|-------------|:----:|
| **Canary Release** | Deploy to 5% of users, monitor, ramp up | Low (auto-rollback) |
| **Feature Flags** | Toggle features on/off for specific users | Low |
| **A/B Testing** | Compare two versions with real traffic | Low |
| **Smoke Tests** | Run critical-path tests against production | Low (read-only) |
| **Chaos Engineering** | Deliberately break things to test resilience | Medium (controlled) |

---

## Synthetic Monitoring

Simulated users running critical flows 24/7 from multiple locations.

```javascript
// Playwright synthetic monitor (runs every 5 min)
const { test, expect } = require('@playwright/test');

test('Checkout flow is healthy', async ({ page }) => {
    const start = Date.now();
    
    await page.goto('https://shop.example.com');
    await page.click('[data-testid="add-to-cart"]');
    await page.click('[data-testid="checkout"]');
    await expect(page.locator('.order-confirmed')).toBeVisible();
    
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(10000);  // Must complete < 10s
});
```

| Tool | Description |
|------|------------|
| **Checkly** | Playwright-based synthetic monitoring |
| **Datadog Synthetics** | API + browser tests |
| **Grafana Cloud** | Multi-location probes |

---

## Real User Monitoring (RUM)

Track actual user experiences — not simulated ones.

```javascript
// Web Vitals + custom metrics
import { onLCP, onFID, onCLS } from 'web-vitals';

onLCP(metric => sendToAnalytics('LCP', metric.value));  // Largest Contentful Paint
onFID(metric => sendToAnalytics('FID', metric.value));  // First Input Delay
onCLS(metric => sendToAnalytics('CLS', metric.value));  // Cumulative Layout Shift
```

| Metric | What It Measures | Good | Poor |
|--------|-----------------|:----:|:----:|
| **LCP** | Loading speed | < 2.5s | > 4.0s |
| **FID** | Interactivity | < 100ms | > 300ms |
| **CLS** | Visual stability | < 0.1 | > 0.25 |

---

## Error Tracking

Every production error must be captured, grouped, and alerted.

| Tool | Best For |
|------|----------|
| **Sentry** | Frontend + Backend error tracking |
| **Datadog APM** | Full-stack observability |
| **Grafana + Loki** | Log aggregation + alerting |

```java
// Backend error tracking
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handle(Exception e) {
        Sentry.captureException(e);  // Send to Sentry
        return ResponseEntity.status(500)
            .body(new ErrorResponse("Internal error", UUID.randomUUID().toString()));
    }
}
```

---

## Production QA Checklist

- [ ] Synthetic monitors running on critical flows
- [ ] Error tracking configured (Sentry / Datadog)
- [ ] RUM metrics collected (Web Vitals)
- [ ] Alert thresholds defined (error rate > 1%, p95 > 1s)
- [ ] Feature flags for kill switches
- [ ] Rollback plan documented and tested
- [ ] On-call rotation established

---

## Sources

- Sentry — https://sentry.io/
- Checkly — https://www.checklyhq.com/
- Web Vitals — https://web.dev/vitals/
