from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
skip = {root / "index.html", root / "about.html", root / "business.html"}
n = 0
js_added = 0

for html in root.rglob("*.html"):
    if html in skip:
        continue
    rel = html.relative_to(root)
    depth = len(rel.parts) - 1
    asset = ("../" * depth) + "assets/nethub/"
    text = html.read_text(encoding="utf-8", errors="surrogateescape")
    orig = text
    text = text.replace(asset + "logo-mark.png", asset + "logo-nav.png")
    # keep favicon as the small mark
    text = text.replace(
        'href="' + asset + 'logo-nav.png" rel="shortcut icon"',
        'href="' + asset + 'logo-mark.png" rel="shortcut icon"',
    )
    text = text.replace(
        'href="' + asset + 'logo-nav.png" rel="icon"',
        'href="' + asset + 'logo-mark.png" rel="icon"',
    )
    js_tag = f'<script src="{asset}nethub.js" data-depth="{depth}"></script>'
    if "assets/nethub/nethub.js" not in text:
        if "</body>" in text:
            text = text.replace("</body>", js_tag + "</body>", 1)
            js_added += 1
        else:
            text += js_tag
            js_added += 1
    if text != orig:
        html.write_text(text, encoding="utf-8", errors="surrogateescape")
        n += 1

print("updated", n, "html; js added", js_added)
c = (root / "catalog.html").read_text(encoding="utf-8", errors="ignore")
print("catalog logo-nav", "logo-nav.png" in c)
print("catalog nethub.js", "nethub.js" in c)
