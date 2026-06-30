---
tags:
- programming
- qa
- testing
---

# 03 Frontend Automation

Frontend tests validate what users actually see and interact with. They're slower and flakier than backend tests — use them sparingly at the E2E level, heavily at the component level.

---

## The Frontend Testing Pyramid

```
        ┌──────────┐
        │   E2E    │  ← Cypress / Playwright (few, slow)
       ┌┴──────────┴┐
       │ Integration │  ← Testing Library + real browser (medium)
      ┌┴────────────┴┐
      │  Component   │  ← Jest + Testing Library (many, fast)
     ┌┴─────────────┴┐
     │   Unit        │  ← Jest / Vitest (most, fastest)
     └──────────────┘
```

---

## Component Testing (React + Testing Library)

```jsx
// OrderCard.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { OrderCard } from './OrderCard';

test('displays order details', () => {
    const order = { id: '123', status: 'CONFIRMED', total: 34.98 };
    
    render(<OrderCard order={order} />);
    
    expect(screen.getByText('#123')).toBeInTheDocument();
    expect(screen.getByText('CONFIRMED')).toBeInTheDocument();
    expect(screen.getByText('$34.98')).toBeInTheDocument();
});

test('calls onCancel when cancel button clicked', () => {
    const handleCancel = jest.fn();
    render(<OrderCard order={sampleOrder} onCancel={handleCancel} />);
    
    fireEvent.click(screen.getByRole('button', { name: /cancel/i }));
    
    expect(handleCancel).toHaveBeenCalledWith('123');
});
```

---

## E2E Testing — Playwright

```javascript
// checkout.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Checkout Flow', () => {
    
    test('user can complete checkout', async ({ page }) => {
        // Login
        await page.goto('/login');
        await page.fill('[data-testid="email"]', 'test@example.com');
        await page.fill('[data-testid="password"]', 'password123');
        await page.click('[data-testid="login-button"]');
        
        // Add to cart
        await page.click('[data-testid="add-to-cart-1"]');
        
        // Checkout
        await page.click('[data-testid="checkout"]');
        await page.fill('[data-testid="card-number"]', '4242424242424242');
        await page.click('[data-testid="place-order"]');
        
        // Verify
        await expect(page.locator('[data-testid="order-confirmed"]'))
            .toBeVisible();
        await expect(page.locator('[data-testid="order-status"]'))
            .toHaveText('CONFIRMED');
    });
});
```

---

## Cypress vs Playwright vs Selenium

| | Cypress | Playwright | Selenium |
|---|:---:|:---:|:---:|
| **Speed** | Fast | Fastest | Slower |
| **Browser support** | Chrome-family + Firefox | Chrome, Firefox, Safari, Edge | All |
| **Auto-wait** | ✅ | ✅ | ❌ |
| **Parallel** | Paid | Free | Free (Grid) |
| **Mobile** | Limited | ✅ Emulation | ✅ Appium |
| **Best for** | Developer-focused, single-browser | Cross-browser, modern apps | Legacy, cross-browser grid |

> **2024 recommendation:** Playwright for new projects. Cypress if your team already knows it. Selenium only for legacy maintenance.

---

## Test IDs — The `data-testid` Pattern

Never use CSS classes or text content as selectors — they change.

```jsx
// ❌ Fragile — breaks when text changes
await page.click('text=Add to Cart');

// ✅ Stable — survives redesign
<button data-testid="add-to-cart">Add to Cart</button>
await page.click('[data-testid="add-to-cart"]');
```

---

## Sources

- Playwright — https://playwright.dev/
- Testing Library — https://testing-library.com/
- Cypress — https://www.cypress.io/
