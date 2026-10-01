from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
pool = [
    "assets/nethub/photos/soldiers-fade.jpg",
    "assets/nethub/cards/collage-labs.jpg",
    "assets/nethub/cards/collage-paths.jpg",
    "assets/nethub/photos/lab-students.jpg",
    "assets/nethub/photos/lab-cohort.jpg",
]
pat = re.compile(
    r'src="(_external/cdn\.prod\.website-files\.com/[^"]+\.(?:webp|jpg|jpeg|png)[^"]*)"',
    re.I,
)
files = ["catalog.html", "career-path.html", "skill-paths.html", "for-your-team.html"]
for name in files:
    p = root / name
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="surrogateescape")
    i = [0]

    def repl(_m):
        src = pool[i[0] % len(pool)]
        i[0] += 1
        return f'src="{src}"'

    newt = pat.sub(repl, text)
    newt = re.sub(r'\ssrcset="[^"]*"', "", newt)
    if newt != text:
        p.write_text(newt, encoding="utf-8", errors="surrogateescape")
    print(name, "replacements", i[0])
