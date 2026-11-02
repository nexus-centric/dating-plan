# Hen Ho Sai Gon

A progressive web app that suggests date plans for couples in central Ho Chi Minh City. Pick a budget range, a combo and a mood, and the app proposes a food stop plus a cafe or activity, with photos and Google Maps links. Built with React, Vite, TypeScript and Tailwind; there is no backend.

Live site: https://nexus-centric.github.io/dating-plan/

## Getting started

Requires Node.js 24.22.1 or newer.

```bash
npm ci
npm run dev        # http://localhost:5173
npm run build      # type-check and build into dist/
npm run preview    # http://localhost:4173
```

## Project layout

- `src/App.tsx`: UI (Plan, Explore, Trips and Diary tabs).
- `src/planner.ts`: plan generation (slot and combo rules, weighted random picks, per-session history to keep suggestions varied).
- `src/data.ts`: data loading, normalisation and district list.
- `src/data.json`: the place list used by the app.
- `public/images/`: bundled place photos (webp).
- `scripts/`: data collection, verification and audit scripts (Python and Node).
- `data/`: raw and intermediate data for each data batch.

## Data

Each place has a name, district (`area`), `kind`, price range with source and confidence, rating, Google Maps link, optional photo, opening hours and status. Places are verified against Google Maps before they are added; entries whose details cannot be confirmed are marked `uncertain` or hidden. Coverage is central Ho Chi Minh City, including Phu Nhuan, Tan Binh and Tan Phu; outer districts such as District 12, Cu Chi and Hoc Mon are excluded. Plans are capped at 1,000,000 VND per outing for two people.

## Deployment

Pushing to `main` runs `.github/workflows/pages.yml`, which builds the app and deploys `dist/` to GitHub Pages. The base path is taken from the repository name. CI also runs `npm audit --omit=dev --audit-level=low` and `npm audit --audit-level=high`.
