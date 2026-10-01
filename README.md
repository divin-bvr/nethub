# Nethub

Hands-on cybersecurity and networking training. Uganda, DRC, and Sunday labs.

## GitHub Pages (public website)

The pages themselves are static HTML. Public site: https://divin-bvr.github.io/nethub/

A GitHub Action deploys Pages on every push to `main`. If the first deploy asks for permission, open the failed Actions run and enable GitHub Pages.

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
