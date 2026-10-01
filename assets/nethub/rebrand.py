from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = {ROOT / "index.html", ROOT / "about.html", ROOT / "business.html"}

css_path = (
    ROOT
    / "_external/cdn.prod.website-files.com/63eef15e3ff8fd318e9a6888/css/cybrary-staging.webflow.shared.e4d16302d.min.css"
)
css = css_path.read_text(encoding="utf-8", errors="ignore")
for old, new in {
    "#e2047a": "#1b4f8a",
    "#d80c71": "#163a6b",
    "#dc1971": "#1b4f8a",
    "#e84175": "#2e6bb5",
    "#E2047A": "#1b4f8a",
    "#D80C71": "#163a6b",
}.items():
    css = css.replace(old, new)
css_path.write_text(css, encoding="utf-8")
print("patched css")

n = 0
for html in ROOT.rglob("*.html"):
    if html in SKIP:
        continue
    rel = html.relative_to(ROOT)
    depth = len(rel.parts) - 1
    ext = ("../" * depth) + "_external/"
    asset = ("../" * depth) + "assets/nethub/"
    home = "index.html" if depth == 0 else "../" * depth + "index.html"
    text = html.read_text(encoding="utf-8", errors="surrogateescape")
    text = re.sub(r"(?:\.\./)*_external/", ext, text)
    text = re.sub(
        r'src="[^"]*Logo-Full-White\.svg"',
        f'src="{asset}logo-mark.png" alt="Nethub"',
        text,
    )
    text = re.sub(
        r'src="[^"]*cybrary-logo\.svg"',
        f'src="{asset}logo-mark.png" alt="Nethub"',
        text,
    )
    text = re.sub(
        r'src="[^"]*64603abf9e8b1cbd2a4cc808_Vectors-Wrapper\.svg"',
        f'src="{asset}logo-mark.png" alt="Nethub"',
        text,
    )
    text = re.sub(
        r'href="[^"]*cybrary_favicon[^"]*"',
        f'href="{asset}logo-mark.png"',
        text,
    )
    text = text.replace("https://app.cybrary.it/login/", home + "#join")
    text = text.replace("https://app.cybrary.it/login", home + "#join")
    text = text.replace("| Cybrary", "| Nethub")
    text = text.replace("Cybrary", "Nethub")
    css_tag = f'<link rel="stylesheet" href="{asset}nethub.css">'
    js_tag = f'<script src="{asset}nethub.js" data-depth="{depth}"></script>'
    if "assets/nethub/nethub.css" not in text:
        if "</head>" in text:
            text = text.replace("</head>", css_tag + "</head>", 1)
        else:
            text = css_tag + text
    if "assets/nethub/nethub.js" not in text:
        if "</body>" in text:
            text = text.replace("</body>", js_tag + "</body>", 1)
        else:
            text += js_tag
    html.write_text(text, encoding="utf-8", errors="surrogateescape")
    n += 1

print("updated html files", n)
sample = (ROOT / "catalog.html").read_text(encoding="utf-8", errors="ignore")
m = re.search(r'href="[^"]+cybrary-staging[^"]+"', sample)
print("catalog css", m.group(0)[:160] if m else "NO CSS")
print("catalog nethub.css", "nethub.css" in sample)
course = (ROOT / "course/advanced-penetration-testing.html").read_text(
    encoding="utf-8", errors="ignore"
)
m = re.search(r'href="[^"]+cybrary-staging[^"]+"', course)
print("course css", m.group(0)[:160] if m else "NO")
print("index custom", "nethub-site" in (ROOT / "index.html").read_text(encoding="utf-8"))
