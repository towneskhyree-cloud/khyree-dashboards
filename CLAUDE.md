# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of self-contained static HTML dashboards, decks, and tools for Khyree (barber / Khyree City brand, Cut Creaters salon suites, Townes family projects). There is no build system, no package.json, no tests, no framework — every page is a single `index.html` with all CSS and JavaScript inlined.

## Structure

- `index.html` — the **Khyree Vault**: a launcher/index page listing every dashboard. Its `ITEMS` array (inside the `<script>` tag) is the registry of all projects — slug, title, category, `kind` (`"live"` = deployed URL, `"local"` = folder in this repo), URL, pin/status flags. `CAT_ORDER` controls category display order. **When adding or removing a dashboard, update `ITEMS` here.**
- `local/<slug>/index.html` — archived/local dashboards served relative to the vault (linked as `./local/<slug>/`).
- `blast/`, `book-reader/`, `cut-creaters-licensing/` — newer standalone tools at the repo root, each a single `index.html`.
- Live dashboards are deployed externally (mostly `*.surge.sh`, plus `khyreecity.com` / `book.khyreecity.com`) and are only referenced by URL from the vault — their source is not in this repo.

## Development

No build, lint, or test commands. To view a page locally, serve the repo root (needed so the vault's relative `./local/...` links work):

```
python3 -m http.server 8000
```

then open `http://localhost:8000/` (or a subfolder path directly).

## Conventions

- Keep each dashboard fully self-contained in one `index.html`: inline `<style>` and `<script>`, no local asset files. Google Fonts is the only external dependency pattern in use (Inter, Anton, JetBrains Mono are common).
- Styling is hand-rolled modern CSS: `oklch()` colors via CSS custom properties on `:root`, `color-mix()`, `clamp()` for fluid type, backdrop-filter glass surfaces. Match the existing palette/variable style of the file you're editing — pages differ (the vault is dark; `cut-creaters-licensing` defaults to a warm light theme with a light/dark toggle).
- Plain vanilla JavaScript (DOM APIs, `localStorage` for persistence such as the vault's edit/delete state). No frameworks or npm dependencies.
- Commit messages are short, imperative, and describe the user-facing change (e.g. "Add share overlay: QR code, copy link, email, text").
