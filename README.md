## Vehicle Updates Dashboard (Static GitHub Pages)

This project is now designed to be hosted as a **pure static site** (for example, on GitHub Pages).

- `backend/index.html` is the main dashboard page (HTML + CSS + JS only).
- `backend/logo.png` is the logo used in the header.
- Python / Flask / Render files are no longer required for hosting.

> Live updates from Google Sheets require a backend (Flask, Apps Script, etc.).
> The static GitHub Pages version does **not** call any backend by default, so there
> are no "Live (error)" messages.

### 1. Host on GitHub Pages

1. Create a new GitHub repository (or use your existing one).
2. Copy these files to the **root** of the repo:
   - `backend/index.html` → `index.html`
   - `backend/logo.png` → `logo.png` (optional, if you use a logo)
3. Commit and push to GitHub.
4. In the repo on GitHub:
   - Go to **Settings → Pages**.
   - Under **Source**, choose `Deploy from a branch`.
   - Select branch `main` (or `master`) and folder `/ (root)`.
   - Save.
5. After a few minutes, GitHub Pages will give you a URL like:
   - `https://YOUR_USERNAME.github.io/YOUR_REPO/`

Open that URL to see your dashboard.

### 2. Optional: Enable live data again

If in the future you want live data from Google Sheets again, you will need
**some backend** (for example, Apps Script or a simple Flask API hosted elsewhere).

- In `index.html`, the frontend can call an API when `ENABLE_LIVE` is set to `true`.
- For static GitHub Pages, `ENABLE_LIVE` is left `false` so the page never
  calls a backend and always stays error-free.

If you add a backend later, you can:
- Set `ENABLE_LIVE = true` in the `<script>` of `index.html`.
- Set `API_BASE` to your backend URL (for example, your Apps Script web app URL).

