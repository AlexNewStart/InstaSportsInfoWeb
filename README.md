# InstaSportsInfoWeb

Marketing website for **InstaPickleball**, hosted on Vercel and served at
`instapickleball.info`.

Pure static HTML — no build step, no dependencies. Styling is Tailwind via CDN.

## Structure

| Path                 | Purpose                                                          |
| -------------------- | ---------------------------------------------------------------- |
| `index.html`         | Landing page                                                     |
| `contact_us.html`    | Contact page                                                     |
| `legal/privacy.html` | Privacy Policy                                                   |
| `legal/terms.html`   | Terms of Service                                                 |
| `vercel.json`        | Vercel config — `cleanUrls` serves pages without the `.html` suffix |

## Local preview

Run from the repo root:

```bash
npx serve
```

Then open the printed URL (usually `http://localhost:3000`).

> **Do not preview with `python3 -m http.server`.** That server does not read
> `vercel.json`, so clean URLs like `/legal/terms` return a 404 — the file on
> disk is `legal/terms.html`, and only Vercel (or `serve`) auto-appends the
> `.html`. `npx serve` is Vercel's own static server and enables clean URLs by
> default, so it matches production behavior. If you must use `http.server`,
> request the file with its `.html` suffix: `/legal/terms.html`.

## Deploy

Push to the connected branch — Vercel auto-deploys. Live URLs:

- `https://instapickleball.info/`
- `https://instapickleball.info/legal/privacy`
- `https://instapickleball.info/legal/terms`

## Legal pages

`legal/privacy.html` and `legal/terms.html` are **generated** — do not edit
them by hand. Their source of truth is Markdown in the InstaPickleball app
repository:

- `../Claude_Code_APP_Prj/docs/legal/privacy.md`
- `../Claude_Code_APP_Prj/docs/legal/terms.md`

When that Markdown changes, regenerate and commit the HTML:

```bash
python3 scripts/build-legal.py
```

The script self-bootstraps its dependency (`scripts/.venv` is created on first
run). It is a manual, dev-time tool — Vercel never runs it, so the deployed
site stays build-free. See `CLAUDE.md` for the full regeneration checklist.
