# CLAUDE.md

Guidance for Claude Code when working in the **InstaSportsInfoWeb** repository.

## What this repo is

The marketing website for **InstaPickleball**, deployed on Vercel at
`www.instapickleball.info`. Pure static HTML — Tailwind via CDN, no build step, no
npm dependencies. What is committed is exactly what Vercel serves.

## Pages

| File                 | URL (via Vercel `cleanUrls`) |
| -------------------- | ---------------------------- |
| `index.html`         | `/`                          |
| `contact_us.html`    | `/contact_us`                |
| `invite.html`        | `/invite/:code` via rewrite  |
| `legal/privacy.html` | `/legal/privacy`             |
| `legal/terms.html`   | `/legal/terms`               |

## Legal pages are GENERATED — do not hand-edit them

`legal/privacy.html` and `legal/terms.html` are **rendered output**. Do NOT
edit them by hand. Their source of truth is Markdown in the app repository:

- `../Claude_Code_APP_Prj/docs/legal/privacy.md`
- `../Claude_Code_APP_Prj/docs/legal/terms.md`

When that Markdown changes, regenerate the HTML:

```bash
python3 scripts/build-legal.py
```

The script self-bootstraps its one dependency (python-markdown) into
`scripts/.venv` on first run — no manual setup needed. If the app repo is not
the sibling directory `Claude_Code_APP_Prj`, pass `--src PATH_TO_docs/legal`.

After running: review the diff, then commit the updated `legal/*.html`.

### Why a script instead of editing the HTML directly

The rendering encodes non-obvious decisions — YAML frontmatter stripping, the
`nl2br` / `toc` / `extra` Markdown extensions, the `.legal-content` CSS that
re-adds the styling Tailwind's Preflight strips, and the shared nav/footer
template. `scripts/build-legal.py` is the single written specification of all
of that. Hand-editing the HTML would silently diverge from the Markdown
source-of-truth and drift on the next regeneration.

The script is a **manual, dev-time tool**. Vercel never runs it; the deployed
site stays zero-build. `scripts/` is kept out of deployment via `.vercelignore`.

## Naming: product vs legal entity

- **InstaPickleball** — the product / brand. Use in page titles, logos, copy.
- **InstaSportsInfo, Inc.** — the legal entity (a Delaware corporation). Use
  ONLY in copyright lines and legal text. Do not "tidy" it into InstaPickleball.

## Local preview

Use `npx serve` — it honors `cleanUrls` and matches Vercel's behavior. Plain
`python3 -m http.server` does NOT: clean URLs like `/legal/terms` return 404
there because the file on disk is `legal/terms.html`. See `README.md`.

For referral invite pages, `npx serve` can preview the static page at
`/invite?code=1A`. The exact shared URL shape `/invite/1A` is handled by
Vercel's rewrite rules.

The invite page intentionally does not auto-open the app. Users copy the code
and manually tap **Open App**, which currently launches the app root
`instapickleball://` until the app has a real invite-code route.
