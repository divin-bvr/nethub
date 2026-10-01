from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
NAV = '''  <header class="nh-nav" id="nav">
    <div class="nh-wrap">
      <div class="nh-nav-top">
        <a class="nh-brand" href="index.html"><img src="assets/nethub/logo-nav.png" alt="Nethub"></a>
        <p class="nh-nav-locale">Uganda · DRC · Sunday lab</p>
        <a class="nh-btn nh-btn-primary nh-nav-cta" href="index.html#join">Join a lab</a>
        <button class="nh-menu-btn" type="button" aria-label="Menu" onclick="document.getElementById('nav').classList.toggle('open')">Menu</button>
      </div>
      <nav class="nh-nav-links">
        <a href="index.html#campuses">Campuses</a>
        <a href="index.html#learn">Sunday lab</a>
        <a href="catalog.html">Labs</a>
        <a class="nh-split" href="business.html">Apply it</a>
        <a href="about.html">Our story</a>
      </nav>
    </div>
  </header>'''

FOOT = '''  <footer class="nh-footer">
    <div class="nh-wrap nh-footer-grid">
      <div>
        <a class="nh-brand" href="index.html"><img src="assets/nethub/logo-nav.png" alt="Nethub"></a>
        <p>Hands-on cybersecurity and networking. Uganda, DRC, and Sunday labs worldwide.</p>
      </div>
      <div><h4>Practice</h4><ul>
        <li><a href="catalog.html">Labs</a></li>
        <li><a href="index.html#join">Join a lab</a></li>
        <li><a href="business.html">Services</a></li>
      </ul></div>
      <div><h4>Nethub</h4><ul>
        <li><a href="about.html">Our story</a></li>
        <li><a href="join-our-team.html">Facilitate</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul></div>
      <div><h4>Policies</h4><ul>
        <li><a href="privacy-policy.html">Privacy</a></li>
        <li><a href="terms-service.html">Terms</a></li>
        <li><a href="cookie-policy.html">Cookies</a></li>
        <li><a href="faq.html">FAQ</a></li>
      </ul></div>
    </div>
    <div class="nh-wrap nh-copy">© 2026 Nethub. Building Africa’s cybersecurity future from the inside out.</div>
  </footer>'''

for name in ["about.html", "business.html", "privacy-policy.html", "terms-service.html", "cookie-policy.html"]:
    p = root / name
    t = p.read_text(encoding="utf-8")
    t = re.sub(r"<header class=\"nh-nav\"[\s\S]*?</header>", NAV, t, count=1)
    t = re.sub(r"<footer class=\"nh-footer\"[\s\S]*?</footer>", FOOT, t, count=1)
    t = t.replace("assets/nethub/logo-mark.png", "assets/nethub/logo-mark-inverse.jpg")
    p.write_text(t, encoding="utf-8")
    print("patched", name)

# image replacements on template pages
photos = [
    "assets/nethub/nethub-soc-back.jpg",
    "assets/nethub/nethub-face-glow.jpg",
    "assets/nethub/nethub-lab-room.jpg",
    "assets/nethub/card-pentest.jpg",
    "assets/nethub/card-soc.jpg",
    "assets/nethub/card-network.jpg",
    "assets/nethub/nethub-laptop-home-mockup.jpg",
    "assets/nethub/photo-command.jpg",
]
pat = re.compile(
    r'src="([^"]*(?:[Cc]ybrary|Logo-Full-White|cybrary-logo)[^"]*)"',
)
targets = [
    "catalog.html",
    "career-path.html",
    "skill-paths.html",
    "for-your-team.html",
    "collections.html",
    "free-content.html",
    "certifications.html",
]
n = 0
for name in targets:
    p = root / name
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8", errors="surrogateescape")
    i = [0]

    def repl(m):
        src = photos[i[0] % len(photos)]
        i[0] += 1
        return f'src="{src}"'

    newt = pat.sub(repl, t)
    # also swap a few stacked hero webps that say CYBRARY in the bitmap but not filename
    newt = newt.replace(
        "Logo-Full-White.svg",
        "assets/nethub/logo-nav.png",
    )
    if newt != t:
        p.write_text(newt, encoding="utf-8", errors="surrogateescape")
        print(name, "image swaps", i[0])
        n += 1
print("done", n)
