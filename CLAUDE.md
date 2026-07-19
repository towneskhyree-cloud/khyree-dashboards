# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this repo is

**Khyree Vault** — a personal portfolio/launcher of every dashboard, site, codex, and brief Khyree has built, plus a couple of standalone tools. It is deployed as a free static site at **https://khyree-vault.surge.sh** (Surge). There is no backend, no API, and no build step.

Everything here is plain, self-contained HTML: each page is a single `index.html` with all CSS and JS inline. There is no `package.json`, no framework, no bundler, no test suite, and no CI.

## Repository structure

```
index.html          The Vault hub — the main page. Lists every build as a card,
                    with search, category filter chips, stats, iframe previews,
                    and a localStorage-backed hide/restore ("Edit") mode.
blast/index.html    Client Blast Console — mobile-first tool for composing and
                    sending client text blasts (booking announcements etc.).
book-reader/index.html  Book reader / teleprompter — paste text, auto-scroll
                    reading screen (built for Khyree's aunt).
local/<slug>/index.html  Archive of ~22 dashboards originally built on the Mac
                    (Downloads/, iCloud) and bundled into the repo so they work
                    from static hosting. One directory per dashboard, each
                    containing exactly one index.html. Directory-per-file lets
                    the hub link to ./local/<slug>/ with clean URLs.
.gitignore          node_modules/ and .DS_Store only.
```

## How the Vault hub works (index.html)

All content is driven by two constants in the inline `<script>`:

- **`ITEMS`** (~line 181) — the registry of every build. Each entry:
  - `slug` — unique id; for local items it must match the directory name under `local/`
  - `title` — display name, often with an emoji prefix
  - `cat` — category string (must be one of `CAT_ORDER` to sort correctly)
  - `kind` — `"live"` (deployed to the web) or `"local"` (bundled in `local/`)
  - `url` — full https URL for live items; `./local/<slug>/` for local items
  - `path` (local only) — original file location on the Mac, shown as the subtitle
  - `size` (local only, bytes), `date` — display metadata
  - `pin` — optional; marks the card as a ★ HEADLINER
  - `status` — optional; `"active"` shows the ACTIVE NOW badge and includes the
    item in the "Active Now" filter; `"reference"` shows a REFERENCE badge
  - `note` — optional accent-colored one-liner under the URL
- **`CAT_ORDER`** (~line 235) — display order of categories (Family / Move, Cut Creaters, Khyree City, Content / Brand, Strategy / Codex, Money / Finance, UCO, Product, Clients / Demos).

Stats in the hero (total / active / live / local / categories) are computed from `ITEMS` at runtime — never hardcode them. The **footer** (~line 177) is the one thing maintained by hand: it carries the version number, manual counts, and a running changelog sentence. Update it when you add/remove items, and keep the version in the footer in sync with the `kicker` text in the header (~line 153).

Hidden cards are stored in `localStorage` under the key `kc_hidden_slugs` — user-side state, nothing to maintain in code.

## Common tasks

**Add a new live dashboard:** add an entry to `ITEMS` with `kind: "live"` and the full URL, put it under the right category, then update the footer text.

**Add a new local dashboard:** create `local/<slug>/index.html` (the whole page in one file), then add an `ITEMS` entry with `kind: "local"`, `url: "./local/<slug>/"`, and the original Mac `path`/`size`/`date` if known.

**Add a new standalone tool** (like `blast/` or `book-reader/`): create a top-level directory with a single `index.html`. Add it to `ITEMS` only if it should appear in the Vault.

**Retire/rename items:** users can hide cards themselves via Edit mode, so prefer editing `ITEMS` only when the change should be permanent for everyone (see commits `cd39f5f`, `e4c4ebc` for precedent).

## Conventions

- **Single-file pages, always.** No external JS/CSS files, no npm dependencies, no build tooling. Fonts may come from Google Fonts; everything else is inline (SVGs as data URIs).
- **Dark themes throughout.** The Vault and Blast Console share a visual identity: near-black backgrounds, lime green accent `#b8ff00`, blue `#3b82f6`, warm orange/cream accents. The Vault uses `oklch`/`color-mix` CSS with Inter, Anton (display), and JetBrains Mono. The book reader is intentionally different (warm serif, cream-on-dark) — match the style of the file you're editing, not a global standard.
- **Mobile-first for tools.** `blast/` and `book-reader/` are designed for phone use (`maximum-scale=1.0`, tap-highlight disabled, thumb-sized buttons). Keep them that way.
- **Escape user-visible strings** rendered into innerHTML — the hub has an `escapeHtml` helper; use it for anything from `ITEMS`.
- **Respect reduced motion** — the hub disables all animation under `prefers-reduced-motion`; preserve that in new styles.
- **Plain-spoken commit messages** describing the user-facing change (e.g. "Edit/delete control (you can remove cards, persists)"). No conventional-commits formatting.

## Testing and deployment

- **Verify locally** by serving statically (e.g. `python3 -m http.server`) and opening the page — iframe previews on the hub need a server, but individual pages also work opened directly as files.
- **Deployment** is via Surge (`surge` CLI) to `khyree-vault.surge.sh` from the repo root. Deployment is done manually from the owner's machine; pushing to GitHub does not deploy.
- There are no tests or linters. The bar is: open it in a browser, it looks right, search/filters still work.

## Sensitivity note

This is a personal repo containing family planning, finances, and business material (the initial commit explicitly excluded "sensitive research"). Don't add personal data beyond what a task requires, and don't surface repo contents to external services beyond what the owner asks for.
