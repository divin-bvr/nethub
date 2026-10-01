# Nethub

Hands-on cybersecurity and networking training. Uganda, DRC, and Sunday labs.

## GitHub Pages (public website)

The pages themselves are static HTML. After you push this repo to GitHub:

1. Repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: **main**, folder: **/ (root)**
4. Site URL: `https://YOUR-USERNAME.github.io/nethub/`

Browsing, catalog, About, legal, and pricing will load on that address.

## What will not work on GitHub Pages

GitHub Pages does not run Python. Sign in, register, admin desk, CMS, module enrolment, clubs, exams, and news feeds need the Flask server in `server/`.

To run the full platform locally:

```
cd server
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:8765`.

For login and the desk on the public internet, host Flask on a Python host (Render, Railway, Fly.io, or a VPS), not GitHub Pages.
