from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
print("ASSETS")
for p in sorted((root / "assets" / "nethub").iterdir()):
    print(f"  {p.name:50} {p.stat().st_size}")

pat = re.compile(r'(?:src|srcset|href)=["\']([^"\']*[Cc]ybrary[^"\']*)', re.I)
logo_pat = re.compile(r'(?:src|href)=["\']([^"\']*(?:Logo-Full-White|cybrary-logo|cybrary_favicon)[^"\']*)', re.I)

files = {}
for html in root.glob("*.html"):
    t = html.read_text(encoding="utf-8", errors="ignore")
    hits = pat.findall(t) + logo_pat.findall(t)
    if hits:
        files[html.name] = hits[:6]
        print(html.name, "hits", len(pat.findall(t)), "logo", len(logo_pat.findall(t)))

print("ROOT FILES WITH CYBRARY IN SRC", len(files))
