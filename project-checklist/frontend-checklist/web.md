# Web Frontend Checklist

> Framework-agnostic checklist for production web applications.
> React, Vue, Svelte, Angular, or vanilla — the principles are the same. The tools change.
> Last updated: 2026-06-11

---

## 1. Framework & Project Setup

- [ ] **Pick what the team knows** — React (biggest ecosystem, most hires), Vue (gentle learning curve, great docs), Svelte (least boilerplate, compiles away), Angular (batteries included, enterprise), or Solid/Qwik (cutting edge). Not what's trending on Twitter.
- [ ] **Rendering strategy first** — SPA (internal dashboards, no SEO). SSR (content sites, e-commerce). SSG (blogs, docs, marketing). Hybrid (most real apps — static shell + dynamic islands). This decision shapes everything else.
- [ ] **TypeScript strict mode** — `"strict": true`, plus `noUncheckedIndexedAccess`, `noUnusedLocals`, `noUnusedParameters`. Regardless of framework.
- [ ] **Package manager** — pnpm (strict, fast, disk-efficient) or npm. Lockfile committed. No `yarn` unless migrating legacy.
- [ ] **Linting & formatting** — Biome (fastest, single tool) or ESLint + Prettier. Pre-commit hook (lint-staged + husky/lefthook). CI blocks on lint failures.
- [ ] **Monorepo if multi-app** — pnpm workspaces + Turborepo/Nx. Shared types, validators, config between frontends. Not needed for single-app projects.

## 2. Rendering Strategy (The Critical Decision)

- [ ] **SPA (Single Page Application)** — CSR-only. Best for: internal dashboards, admin panels, apps behind login. No SEO needed. Fast after initial load. Example: Vite + any framework.
- [ ] **SSR (Server-Side Rendering)** — Server renders HTML per request. Best for: user-specific content, frequently-changing data, SEO-critical pages. Higher server cost per request.
- [ ] **SSG (Static Site Generation)** — Pre-render at build time. Best for: blogs, docs, marketing pages, changelogs. Fastest to serve (just HTML), but rebuild on content change.
- [ ] **ISR (Incremental Static Regeneration)** — Static with cache-based revalidation. Best hybrid: static speed, near-dynamic freshness. Revalidate every N seconds or on-demand.
- [ ] **Islands Architecture** — Static shell with dynamic interactive islands. Astro, Fresh (Deno), or framework-level partial hydration. Minimal JS shipped to browser.
- [ ] **Streaming** — Send HTML as it's ready, don't wait for everything. Users see content faster. Suspend/await boundaries at component level. All major meta-frameworks support this now.
- [ ] **Don't over-complicate it** — SPA for internal tools. SSG for blogs. SSR for e-commerce. You don't need every strategy in one app.

## 3. Data Fetching & Server State

- [ ] **Server state library** — Every async read through a query, every async write through a mutation. This pattern is universal: TanStack Query (React/Vue/Svelte/Solid), RTK Query, Apollo Client (GraphQL), or SWR.
- [ ] **Query key conventions** — Hierarchical, granular, cache-friendly. `['users', userId, 'posts', { status: 'draft' }]`. Invalidating `['users']` clears all user queries.
- [ ] **Stale time & cache eviction** — `staleTime` controls refetch triggers. Cache eviction time controls memory. Default staleTime is usually 0 (too aggressive for semi-static data). Tune per query.
- [ ] **Smooth pagination** — Keep previous page visible while loading next. `placeholderData` / `keepPreviousData` pattern. No layout shift between pages.
- [ ] **Optimistic updates** — Update UI immediately, rollback on error. `onMutate` → snapshot previous → set optimistic → `onError` → restore snapshot. Feels instant.
- [ ] **Prefetching** — Prefetch on hover, on focus, on intent. Data ready before the user clicks.
- [ ] **Every async view has 4 states** — Loading (skeleton/spinner), Empty ("No items yet"), Error (with retry), Loaded (the actual content). Never just 2 out of 4.

## 4. Client State Management

- [ ] **Server state ≠ client state** — Server cache (TanStack Query) for data from the API. Client state for ephemeral UI: open modals, active tab, form drafts, theme. Don't put API data in client stores.
- [ ] **Client state library** — Lightweight, no boilerplate. Zustand (React), Pinia (Vue), Svelte stores (built-in), signals (Solid/Preact/Qwik), or Jotai for atomic reactivity.
- [ ] **URL as state** — Search params, filters, pagination, selected item → in the URL. Shareable, bookmarkable, back-button friendly. `useSearchParams()`, `useRouter()`, or framework equivalent.
- [ ] **Form state** — Separate from app state. Form library handles values, validation, submission, dirty/pristine, errors. Don't wire forms to global stores.
- [ ] **Context/injection only for truly global concerns** — Auth, theme, locale, feature flags. Not for frequently-changing state (re-renders all consumers).
- [ ] **No heavy state management unless justified** — Redux, NgRx, Vuex (deprecated) are overkill for most apps. Server cache + lightweight client state covers 95% of cases with less code.

## 5. Performance

- [ ] **Core Web Vitals** — LCP < 2.5s (loading), INP < 200ms (interactivity), CLS < 0.1 (visual stability). These are Google ranking factors as well as UX. Measure with Lighthouse CI in pipeline.
- [ ] **Code splitting** — Route-level (every router does this). Component-level for heavy widgets (charts, editors, media players): dynamic import with loading fallback. Don't ship 500KB of chart library on the homepage.
- [ ] **Image optimization** — Responsive sizes, modern formats (WebP/AVIF), lazy loading (`loading="lazy"`), LCP image eager with `fetchpriority="high"`. Use framework image component or `<picture>` with multiple sources.
- [ ] **Font optimization** — Self-host fonts (not Google Fonts CDN). `font-display: swap` (or `optional`). Subset to needed characters. WOFF2 format. Preload critical fonts.
- [ ] **No waterfall data fetching** — Fetch in parallel: `Promise.all([getUsers(), getPosts()])`. Or co-locate data fetching with the component that needs it.
- [ ] **Large lists → virtualize** — Don't render 10,000 DOM nodes. `@tanstack/virtual`, `vue-virtual-scroller`, or framework equivalent. Only render what's in/near the viewport.
- [ ] **Debounce user input** — Search inputs, filter changes, resize handlers. Not `onInput` → API call. `onInput` → local state → debounce 300ms → API call.
- [ ] **Bundle analysis** — Know what's in your bundle. Catch accidentally-imported heavy deps. `vite-bundle-visualizer`, `webpack-bundle-analyzer`, or framework plugin.
- [ ] **Tree shaking** — ES modules, side-effect-free packages, granular imports (`import { debounce } from 'lodash-es'`, not `import _ from 'lodash'`).
- [ ] **CDN for static assets** — Serve JS, CSS, images, fonts from CDN. Immutable cache headers for content-hashed files. Different origin (or subdomain) to skip cookie headers.

## 6. Styling & Design

- [ ] **Utility-first CSS** — Tailwind CSS (framework-agnostic), UnoCSS (faster, flexible), or vanilla CSS with utility classes. Consistent spacing, typography, colors, without naming 500 classes.
- [ ] **Component primitives** — Don't build your own modal, dropdown, tooltip, or combobox. Use headless, accessible components: Radix (React), Headless UI (React/Vue), Melt UI (Svelte), Floating UI for positioning. Copy-paste styled versions (shadcn/ui pattern) over npm dependency.
- [ ] **Design tokens** — CSS custom properties for colors, spacing, radius, shadows, typography. Single source of truth. Dark mode via `prefers-color-scheme` or class toggle.
- [ ] **Responsive design** — Mobile-first breakpoints. Test at actual device widths (375px, 414px, 768px, 1024px, 1440px). `min-width` media queries, not `max-width`.
- [ ] **Layout primitives** — `<Container>`, `<Stack>`, `<Grid>`, `<Flex>` wrapper components. Consistent max-widths, gutters, alignment. Not ad-hoc margins on every element.
- [ ] **Animation with intent** — `prefers-reduced-motion` respected. Hardware-accelerated properties only (`transform`, `opacity`). Not `height`/`width` transitions (layout thrashing).

## 7. Forms

- [ ] **Form library** — Every framework has one: React Hook Form (React), FormKit/VeeValidate (Vue), Felte (Svelte), Angular Reactive Forms. Uncontrolled/lightweight by default for performance.
- [ ] **Schema validation** — Zod, Valibot, Yup, Joi. Define the schema once, derive TypeScript type from it. Reuse schemas with backend if shared package.
- [ ] **Server-side validation too** — Client validation is UX, server validation is security. Always validate on the server regardless of client validation.
- [ ] **Form states** — Idle (ready to fill), submitting (disable button + spinner), success (redirect or confirmation), error (inline field errors + form-level message). Every state is rendered.
- [ ] **Accessible forms** — Labels associated with inputs (`<label for="...">`). Error messages linked via `aria-describedby`. Required fields marked. Submit with Enter key.
- [ ] **File uploads** — Preview before upload, progress indicator, drag-and-drop, size/type validation client-side. Chunked upload for large files.

## 8. Routing & Navigation

- [ ] **Router choice** — File-system router (Next.js App Router, Nuxt, SvelteKit, Analog) or programmatic router (React Router, Vue Router). File-system is simpler for most apps.
- [ ] **Nested layouts** — Persistent layout across child route navigations. Sidebar stays mounted while content changes. Avoid full-page remounts.
- [ ] **Route-level loading states** — Automatic loading UI per route while data fetches. Not a blank page.
- [ ] **Route-level error handling** — Error boundary per route. Fallback UI with retry button. Not white screen or full-page crash.
- [ ] **Route guards** — Auth gates, role checks, redirects — enforced at the router level, not in every component. One place to check.
- [ ] **Scroll restoration** — Back/forward navigation restores scroll position. Anchor links work. Framework router should handle this.
- [ ] **404 & error pages** — Helpful, not default framework page. Links to homepage, search, or sitemap. Different 404 for different sections.
- [ ] **SEO metadata per route** — `<title>`, `<meta name="description">`, Open Graph, canonical URL. Generated from data, not hard-coded.

## 9. Testing

- [ ] **Unit tests** — Vitest (fast, Vite-native, Jest-compatible) or framework-native runner. For utils, hooks/composables, pure functions, state logic.
- [ ] **Component tests** — Testing Library (framework-specific adapters available for all major frameworks). Test behavior, not implementation: `screen.getByRole('button', { name: /submit/i })`, not `screen.getByTestId('submit-btn')`. Use `userEvent`, not `fireEvent`.
- [ ] **API mocking** — MSW (Mock Service Worker) — framework and protocol agnostic. Intercept at network level, components test against realistic responses. Works with REST, GraphQL, any protocol.
- [ ] **E2E tests** — Playwright (multi-browser, modern, fast) or Cypress. Critical user flows: login → navigate → create → edit → delete. Visual regression with `toHaveScreenshot()`.
- [ ] **Accessibility tests** — `axe-core` (framework-agnostic) in unit tests and E2E. Catch violations in CI. Block merges on critical a11y regressions.
- [ ] **Test what matters** — Happy path, error states, empty states, loading states, auth guard redirects. Not 100% coverage of trivial getters.

## 10. Accessibility (a11y)

- [ ] **Semantic HTML** — `<button>` for actions, `<a>` for navigation, `<nav>` for navigation regions, `<main>` for primary content, `<form>` for forms, `<table>` for tabular data. Not `<div>` with click handlers.
- [ ] **Heading hierarchy** — One `<h1>` per page, logical `<h2>` → `<h3>` → `<h4>` nesting. Not skipping levels to match visual size.
- [ ] **Keyboard navigation** — All interactive elements reachable and operable via keyboard. Logical tab order. Visible focus indicators (`:focus-visible` ring). Skip-to-content link as first tab stop.
- [ ] **ARIA — last resort** — `aria-label` on icon-only buttons. `aria-expanded` on toggles. `aria-describedby` on error messages. `role` only when HTML semantics can't express it. No ARIA is better than wrong ARIA.
- [ ] **Color contrast** — WCAG AA minimum: 4.5:1 for normal text, 3:1 for large text (≥18px or ≥14px bold). Don't rely on color alone to convey information (add icons, text).
- [ ] **Screen reader testing** — Spot-check with VoiceOver (macOS), NVDA (Windows), or Android TalkBack. Navigate by headings, landmarks, links. Fill a form. Complete a flow.
- [ ] **Motion safety** — Respect `prefers-reduced-motion`. No auto-playing video with audio. Pause/stop controls for animations. No flashing content (< 3 flashes/second — epilepsy risk).

## 11. Security (Frontend-Specific)

- [ ] **XSS prevention** — Never inject unsanitized HTML. If you must render HTML (user-generated content), sanitize with DOMPurify. Template engines auto-escape by default — don't disable it.
- [ ] **Never `eval`, never `new Function`** — In client code. CSP should block these anyway.
- [ ] **No secrets in client code** — Every env var with a public prefix (`NEXT_PUBLIC_*`, `VITE_*`, `PUBLIC_*`) is bundled to the browser. Private env vars stay server-side. No API keys, no tokens, no secrets in the bundle.
- [ ] **Auth token storage** — HTTP-only, Secure, SameSite cookies (inaccessible to JS, no XSS risk). If forced to use localStorage or sessionStorage: accept the XSS risk and keep token lifetime short.
- [ ] **CSP (Content Security Policy)** — Work with backend/devops to set restrictive CSP. No `unsafe-inline`, no `unsafe-eval`. Start in `Content-Security-Policy-Report-Only` mode to gather violations first.
- [ ] **CORS** — Configured on the backend, but frontend needs to understand it. Credentialed requests (`withCredentials: true`) need explicit CORS allowlist. No `Access-Control-Allow-Origin: *` with credentials.
- [ ] **Dependency audit** — `npm audit` / `pnpm audit` in CI. Dependabot or Renovate for automated security patches. Frontend has hundreds of transitive dependencies — most CVEs aren't exploitable in browser context, but patch them anyway.
- [ ] **Subresource Integrity (SRI)** — For CDN-loaded third-party scripts. Hash mismatch → browser rejects. Don't blindly trust third-party CDNs.
- [ ] **CSRF protection** — If using cookie-based auth: SameSite=Lax minimum, CSRF token for mutation endpoints. SPA with token in header (`Authorization: Bearer ...`) is CSRF-immune since browser doesn't auto-attach it.

## 12. Build & Deploy

- [ ] **Environment variables** — Client-safe vars: explicitly prefixed, bundled at build time. Server-only vars: no prefix, only accessible in server-side code. No mixing.
- [ ] **CI/CD pipeline** — Lint → type-check → unit test → build → deploy preview → E2E → promote to production. Every PR gets a preview URL.
- [ ] **Preview deployments** — Every PR/commit gets a unique URL (Vercel, Netlify, Cloudflare Pages, or custom). Shareable with stakeholders. Environment matches production as closely as possible.
- [ ] **Static assets with content-hash** — Build tool does this automatically (Vite, webpack, Rollup). Immutable cache headers (`Cache-Control: public, max-age=31536000, immutable`). Fingerprinted filenames make cache invalidation free.
- [ ] **Bundle analysis in CI** — Block on bundle size regressions. Set budgets (total JS < 200KB gzipped initial, total CSS < 50KB). Catch the moment-moment someone adds moment.
- [ ] **Feature flags** — LaunchDarkly, Vercel Flags, Unleash, or simple config. Deploy code dark, enable in production. Kill broken features without redeploy. Not the same as environment variables (flags are runtime, env vars are build-time).
- [ ] **Blue-green or canary deploys** — Zero-downtime. Shift traffic gradually to new version. Health check new instances before routing to them. Static sites: atomic deploys (CDN swap).

## 13. Error Handling & Observability

- [ ] **Global error boundary** — Catch unhandled errors, render fallback UI. Not a white screen. Include retry/reset. Log to monitoring service.
- [ ] **Error monitoring** — Sentry, Datadog RUM, or similar. Source maps uploaded (not public). Errors grouped by source map. Correlate frontend errors with backend traces via trace ID.
- [ ] **RUM (Real User Monitoring)** — Core Web Vitals from real users, not just synthetic Lighthouse. LCP, INP, CLS segmented by device, country, page. Know what users actually experience.
- [ ] **Structured logging** — On the server side (SSR/SSG). Client-side: meaningful error context in Sentry (user ID, route, browser, actions leading up).
- [ ] **Graceful degradation** — If JavaScript fails: is the page still usable? If API fails: cached data, stale-while-revalidate, or clear error message. Nothing is less professional than a stuck spinner.

## 14. Internationalization (i18n) — If Multi-Language

- [ ] **Decide early** — Adding i18n to an existing app is painful. If you might need it, at least externalize all user-facing strings from day one.
- [ ] **Library choice** — `i18next` (framework-agnostic, most popular), framework-specific wrapper, or built-in (`next-intl`, `vue-i18n`, `svelte-i18n`). ICU message format for complex pluralization/interpolation.
- [ ] **RTL support** — Logical CSS properties (`margin-inline-start`, not `margin-left`). Direction-aware utilities. Test with Arabic/Hebrew.
- [ ] **Locale detection** — `Accept-Language` header (server), `navigator.language` (client), URL segment (`/en/`, `/th/`), or user preference. URL segment is best for SEO and sharing.
- [ ] **Translation management** — Translation keys in code, translations in JSON/YAML. CI validates all keys exist in all locales. Consider a TMS (Lokalise, Phrase, Crowdin) for non-dev translators.

## 15. Offline & Resilience

- [ ] **Offline strategy** — PWA service worker (if needed). At minimum: no broken UI when API is down. Cached shell, error messages, retry buttons.
- [ ] **Network resilience** — `navigator.onLine` for awareness. Retry with exponential backoff for transient failures. Queue mutations while offline, replay when online (if PWA).
- [ ] **No uncached API calls on every render** — Stale cache serves instantly, background refetch updates. Better to show slightly stale data fast than a spinner.

---

## Quick Sanity Check Before Launch

- [ ] Every page has a unique `<title>` and `<meta name="description">`
- [ ] LCP image uses `fetchpriority="high"` and is not lazy-loaded
- [ ] No console errors in production build
- [ ] Lighthouse score ≥ 90 on mobile (Performance, Accessibility, Best Practices, SEO)
- [ ] All forms submit with Enter key
- [ ] Back button works correctly — no redirect loops, no stuck pages
- [ ] Tested on actual mobile devices, not just Chrome DevTools responsive mode
- [ ] 404 page exists, is helpful, and has navigation options
- [ ] `robots.txt` and `sitemap.xml` exist and are correct
- [ ] OG meta tags render correctly (test with Slack/Discord/Twitter unfurl)
- [ ] `favicon.ico` and PWA manifest icons exist at expected sizes
- [ ] Keyboard navigation works end-to-end (tab through, close modals with Esc)
- [ ] No secrets in client bundle (check with source map explorer)
- [ ] Error boundary renders, not a white screen

---

## Framework Quick Reference

### React
- **Meta-frameworks:** Next.js (App Router), Remix, React Router 7 (framework mode)
- **State:** TanStack Query + Zustand
- **Forms:** React Hook Form + Zod
- **Styling:** Tailwind + shadcn/ui + Radix
- **Testing:** Vitest + React Testing Library + Playwright

### Vue
- **Meta-frameworks:** Nuxt (file-based router, SSR/SSG), Vite + Vue Router (SPA)
- **State:** TanStack Query (Vue adapter) + Pinia
- **Forms:** FormKit, VeeValidate + Zod
- **Styling:** Tailwind + Headless UI (Vue) or Radix Vue
- **Testing:** Vitest + Vue Testing Library + Playwright

### Svelte
- **Meta-frameworks:** SvelteKit (filesystem router, SSR/SSG/SPA)
- **State:** TanStack Query (Svelte adapter) + Svelte stores (built-in)
- **Forms:** Felte + Zod, Superforms (SvelteKit server actions)
- **Styling:** Tailwind + Melt UI + shadcn-svelte
- **Testing:** Vitest + Svelte Testing Library + Playwright

### Angular
- **Meta-frameworks:** Angular CLI, Analog (file-based, Vite-powered)
- **State:** TanStack Query (Angular adapter) + Signals (built-in) + NgRx (if complex)
- **Forms:** Angular Reactive Forms + Zod
- **Styling:** Tailwind + Angular CDK (headless primitives)
- **Testing:** Jasmine/Karma (default) or Jest/Vitest + Testing Library + Playwright

### Solid / Qwik / Astro
- **Solid:** TanStack Query (Solid adapter) + signals (built-in). Vite-based.
- **Qwik:** Resumability — no hydration. Built-in routing, state, forms. Unique model.
- **Astro:** Islands architecture. Bring your own framework for interactive islands (React, Vue, Svelte, Solid). Best for content-heavy sites.

### Universal Tools (any framework)
- **Lint/Format:** Biome (recommended) or ESLint + Prettier
- **Testing:** Playwright (E2E), Vitest (unit), MSW (API mocking), axe-core (a11y)
- **Monitoring:** Sentry, Datadog RUM, OpenTelemetry (trace propagation)
- **Feature flags:** LaunchDarkly, Vercel Flags, Unleash
- **Analytics:** Plausible (privacy-first), PostHog (product analytics), or whatever the team uses
