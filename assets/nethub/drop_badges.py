from pathlib import Path

root = Path(__file__).resolve().parents[2]
needle_h = "Earn Industry Badges"
files = [
    "catalog.html",
    "career-path.html",
    "skill-paths.html",
    "collections.html",
    "cybrary-insider-pro.html",
]
files += [str(p.relative_to(root)) for p in (root / "lp").glob("*.html")]
n = 0
for rel in files:
    p = root / rel
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8", errors="surrogateescape")
    if needle_h not in t and "Earn Credly" not in t:
        continue
    t2 = t.replace(
        '<h2 class="heading-style-h5">Earn Industry Badges</h2>',
        '<h2 class="heading-style-h5" data-removed="badges" style="display:none"></h2>',
    )
    t2 = t2.replace(
        "Complete coursework to earn industry-recognized badges via Credly.",
        "",
    )
    t2 = t2.replace("Earn Credly-Certified Badges", "")
    if t2 != t:
        p.write_text(t2, encoding="utf-8", errors="surrogateescape")
        n += 1
        print("updated", rel)
print("files", n)
