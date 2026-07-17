# Bun + React 19 + DaisyUI Frontend Setup

When the Go API is ready and the user wants a frontend, scaffold with this stack.

## Init (manual — `bun create vite` is interactive, fails in non-PTY)

```bash
mkdir frontend && cd frontend
```

Write `package.json` manually:
```json
{
  "name": "project-web",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "autoprefixer": "^10.4.0",
    "daisyui": "^5.0.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^4.0.0",
    "typescript": "^5.6.0",
    "vite": "^6.0.0"
  }
}
```

Then: `bun install`

## Tailwind v4 + DaisyUI 5

`src/index.css`:
```css
@import "tailwindcss";
@plugin "daisyui" {}
```

No `tailwind.config.js` or `postcss.config.js` needed with Tailwind v4.

## Vite Config (API proxy)

```ts
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:3000',
    },
  },
})
```

## CSS Module Types

Create `src/vite-env.d.ts`:
```ts
/// <reference types="vite/client" />
```

Without this, `import './index.css'` fails with `TS2307`.

## Project Structure

```
src/
├── api/client.ts          ← Typed fetch wrapper
├── types/api.ts           ← TypeScript types (mirror backend model/)
├── components/            ← Reusable UI components
├── pages/                 ← Route pages
├── App.tsx                ← Router (react-router-dom)
├── main.tsx               ← Entry point
└── index.css              ← Tailwind + DaisyUI
```

## DaisyUI Component Patterns

- Cards: `<div className="card bg-base-100 shadow-md border border-base-300">`
- Badges: `<span className="badge badge-success">done</span>`
- Modals: `<dialog className="modal modal-open">`
- Loading: `<span className="loading loading-spinner loading-lg"></span>`
- Pagination: `<div className="join">` with `join-item btn btn-sm`
- Forms: `input input-bordered`, `textarea textarea-bordered`, `select select-bordered`
