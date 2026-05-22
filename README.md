# InstaSportsInfoWeb

Marketing website for **InstaPickleball**, hosted on Vercel and served at
`www.instapickleball.info`.

Pure static HTML — no build step, no dependencies. Styling is Tailwind via CDN.

## Structure

| Path                 | Purpose                                                          |
| -------------------- | ---------------------------------------------------------------- |
| `index.html`         | Landing page                                                     |
| `contact_us.html`    | Contact page                                                     |
| `invite.html`        | Referral invite landing page for `/invite/:code`                 |
| `legal/privacy.html` | Privacy Policy                                                   |
| `legal/terms.html`   | Terms of Service                                                 |
| `vercel.json`        | Vercel config — `cleanUrls` and referral invite rewrites         |

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
>
> For referral invite pages, preview the static page locally with
> `/invite?code=1A`. The exact shared URL shape `/invite/1A` depends on the
> Vercel rewrite in `vercel.json`.

## Deploy

Push to the connected branch — Vercel auto-deploys. Live URLs:

- `https://www.instapickleball.info/`
- `https://www.instapickleball.info/invite/1A`
- `https://www.instapickleball.info/legal/privacy`
- `https://www.instapickleball.info/legal/terms`

## Referral invites

The app shares links like `https://www.instapickleball.info/invite/1A`.
Vercel rewrites `/invite/:code` to `/invite?code=:code`, so one static file
can handle every referral code.

The page does not auto-open the app. Some in-app browsers, including WeChat,
block automatic third-party app launches and can make the page appear to flash.
Instead, the user can copy the code, tap **Open App** to launch
`instapickleball://`, or continue to the website download section. Until the iOS
App Store page is live, the fallback is the website rather than an App Store URL.

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
