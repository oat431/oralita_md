# Frontend Launch Checklist

> Tick every box before a frontend app hits production. Framework-agnostic. React/Next.js focus but applies to any modern frontend.

---

## Rendering & Performance

- [ ] Rendering model chosen with documented reasoning (SSR/SSG/CSR/ISR) → [[06 Mobile First Design]]
- [ ] Data fetching at the right layer (server components for data, client components for interactivity)
- [ ] Bundle analyzed (no unused dependencies, no duplicated libraries)
- [ ] Images optimized: correct format (WebP/AVIF), responsive sizes, lazy loading
- [ ] Fonts optimized: subset, `font-display: swap`, self-hosted
- [ ] First paint under 1.5s, largest contentful paint under 2.5s

---

## Accessibility

- [ ] Semantic HTML (buttons are `<button>`, not `<div onClick>`) → [[28 Accessibility]]
- [ ] All images have meaningful `alt` text
- [ ] Color contrast meets WCAG AA (4.5:1 for text, 3:1 for large text)
- [ ] Keyboard navigation works (Tab, Enter, Escape, arrow keys)
- [ ] Focus indicators visible (never `outline: none` without replacement)
- [ ] Forms have labels, error messages are descriptive
- [ ] Screen reader tested (at least once with VoiceOver/NVDA)

---

## State & Data

- [ ] Server state cached (React Query, SWR, or framework built-in)
- [ ] Client state minimal (no duplicating server state)
- [ ] Loading states for every async operation
- [ ] Error boundaries for every major section (one component crash ≠ white page)
- [ ] Empty states designed (not just "no results" — guide the user)
- [ ] Form state: submit, loading, success, error — all four states handled

---

## Security

- [ ] No secrets in client-side code (API keys, tokens in env → hidden at build time)
- [ ] Auth tokens: access token in memory, refresh token in httpOnly secure cookie
- [ ] CSRF protection on all state-changing requests
- [ ] Input sanitized before rendering (never `dangerouslySetInnerHTML` with user input)
- [ ] Third-party scripts loaded with `integrity` hashes (SRI)
- [ ] Content Security Policy configured → [[03 API Security]]

---

## UI/UX

- [ ] Responsive: works on mobile, tablet, desktop → [[06 Mobile First Design]]
- [ ] Touch targets ≥ 44×44px (WCAG 2.5.5)
- [ ] Visual hierarchy intentional → [[26 Visual Hierarchy]]
- [ ] Consistent design language (colors, spacing, typography) → [[27 Consistency]]
- [ ] Dark mode: if supported, tested on both themes → [[09 Dark Mode]]
- [ ] Typography: readable line length (45-75 chars), line height ≥ 1.5 → [[07 Typography & Spacing]]
- [ ] Color not the only way to convey information → [[08 Color & Opacity]]

---

## Testing

- [ ] Component tests for critical UI (happy path + error states) → [[03 Frontend Automation]]
- [ ] Critical user flows tested E2E (login → do thing → see result)
- [ ] Visual regression tests if UI changes frequently
- [ ] Tested on: Chrome, Firefox, Safari, mobile Safari/Chrome
- [ ] Tested on actual device (not just DevTools device mode)

---

## SEO & Meta

- [ ] `<title>` unique and descriptive on every page
- [ ] `<meta name="description">` on every page
- [ ] Open Graph tags for social sharing (`og:title`, `og:image`, `og:description`)
- [ ] `robots.txt` and sitemap present
- [ ] Canonical URLs on pages with duplicate content

---

## Deployment

- [ ] Build output tested locally (`next build && next start` or equivalent)
- [ ] Environment variables documented (which are required, which are optional)
- [ ] Cache headers set (static assets: long max-age with content hash)
- [ ] 404 page custom (not the framework default)
- [ ] Error logging (Sentry, LogRocket, or equivalent)
- [ ] Analytics (if used): privacy-compliant, cookie consent if required

---

## Sources

- Distilled from: HCI vault, [[Cybersecurity Overview]], [[API Overview]].
- Original deep reference: `../react-js.md`, `../web.md`
