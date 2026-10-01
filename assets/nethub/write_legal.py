from pathlib import Path

ROOT = Path(r"C:\Users\Divin-Kapata\Downloads\0b1711f4-cf39-4231-a28a-b7f2c85744a0\Nethub")

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="icon" href="assets/nethub/logo-mark-inverse.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/nethub/nethub.css">
</head>
<body class="nethub-site">
  <header class="nh-nav" id="nav">
    <div class="nh-wrap nh-nav-inner">
      <a class="nh-brand" href="index.html"><img src="assets/nethub/logo-nav.png" alt="Nethub"></a>
      <button class="nh-menu-btn" type="button" onclick="document.getElementById('nav').classList.toggle('open')">Menu</button>
      <nav class="nh-nav-links">
        <a href="catalog.html">Labs</a>
        <a href="index.html#learn">Sundays</a>
        <a href="index.html#campuses">Campuses</a>
        <a class="nh-split" href="business.html">Services</a>
        <a href="about.html">Our story</a>
      </nav>
      <div class="nh-actions"><a class="nh-btn nh-btn-primary" href="index.html#join">Join a lab</a></div>
    </div>
  </header>
"""

FOOT = """
  <footer class="nh-footer">
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
    <div class="nh-wrap nh-copy">© 2026 Nethub.</div>
  </footer>
</body></html>
"""

pages = {
"privacy-policy.html": dict(
title="Privacy | Nethub",
desc="How Nethub handles personal information for learners, facilitators, sponsors, and small-business clients in Uganda, DRC, and online Sunday labs.",
kicker="Policies · last updated September 2026",
h1="Privacy",
lead="Nethub is a training community and a small security practice. We collect only what we need to run labs, support sponsored seats, and deliver work we are hired to do.",
body="""
<article class="nh-card"><h3>Who we are</h3><p>Nethub operates hands-on cybersecurity and networking labs with partner universities in Uganda (two campuses) and the DRC (one university), plus Sunday sessions online. We also support refugee and underserved learners whose seats are funded by sponsors, NGOs, and institutions.</p></article>
<article class="nh-card"><h3>What we collect</h3><p>Name, campus or settlement, email or messaging handle, attendance, lab progress, and — if you pay — contribution records. For sponsored learners we may receive a roster from the partner that funds the seat. For small-business work we keep the scope, contacts, and reports needed to do the job.</p></article>
<article class="nh-card"><h3>How we use it</h3><p>To run weekend and Sunday labs, match you with a facilitator, offer career guidance, invoice contributions, and protect the lab environment. We do not sell learner lists. Service reports stay with the client unless they ask us to share a summary with a regulator or insurer.</p></article>
<article class="nh-card"><h3>Who we share with</h3><p>Facilitators and university hosts who need a roster. Sponsors who fund a specific cohort, on request. Processors that host email or lab infrastructure. We will not hand data to a marketplace or an unrelated training platform.</p></article>
<article class="nh-card"><h3>Your choices</h3><p>Ask us to correct a record, drop you from a mailing list, or delete an account that is not required for an active contract or safety incident. Write through the contact page. This notice is written for Nethub — it is not Cybrary’s policy and does not cover cybrary.it.</p></article>
"""
),
"terms-service.html": dict(
title="Terms | Nethub",
desc="Terms for joining Nethub labs, sponsored seats, and scoped security work for small companies.",
kicker="Policies · last updated September 2026",
h1="Terms of use",
lead="These terms cover campus labs, Sunday global sessions, sponsored seats, and security services. They replace any Cybrary terms that used to sit on this URL.",
body="""
<article class="nh-card"><h3>Labs are practical, not a degree</h3><p>Nethub builds an environment where you attack, defend, configure, and break things safely. We invite experts, sit one-on-one, and talk careers. Completing a weekend or Sunday session is not a university diploma and not a professional license.</p></article>
<article class="nh-card"><h3>Contribution</h3><p>Paying learners contribute about $25 a month, sometimes less. Sponsored and underserved seats are funded by NGOs, sponsors, and institutions. Missing payment may pause lab access; it does not erase the community’s duty of care in an active session.</p></article>
<article class="nh-card"><h3>Lab rules</h3><p>Practice only inside the environments we give you. Do not use Nethub techniques against systems you do not have permission to test. That includes “practice” on a friend’s business. Services for companies are scoped in writing.</p></article>
<article class="nh-card"><h3>Services</h3><p>Pentesting, awareness, hardening, forensics, network security, web-app security, and WAF work are delivered under a separate statement of work. Findings are confidential to the client.</p></article>
<article class="nh-card"><h3>Liability</h3><p>Labs are educational. We are not liable for career outcomes, exam results, or damages from misuse of skills. For paid services, liability is limited to fees paid for that engagement unless the law says otherwise.</p></article>
"""
),
"cookie-policy.html": dict(
title="Cookies | Nethub",
desc="How the Nethub website uses cookies and similar storage.",
kicker="Policies · last updated September 2026",
h1="Cookies",
lead="This static site is meant to explain Nethub and point you to labs. We keep tracking light.",
body="""
<article class="nh-card"><h3>What we use</h3><p>Essential cookies or local storage may remember a menu state or a form draft. If a future lab portal is added, it may keep a signed-in session.</p></article>
<article class="nh-card"><h3>What we do not do</h3><p>We do not run Cybrary analytics, Cybrary ads, or Cybrary login cookies on these pages. Third-party fonts (Google Fonts) may set their own technical cookies when your browser loads them.</p></article>
<article class="nh-card"><h3>Your controls</h3><p>You can block cookies in the browser. The site will still describe the program; some interactive bits on leftover catalog pages may look broken if scripts are blocked.</p></article>
"""
),
"faq.html": dict(
title="FAQ | Nethub",
desc="Common questions about Nethub labs, cost, refugee seats, Sundays, and services.",
kicker="Help",
h1="Questions we actually get",
lead="Short answers. If yours is missing, use the contact page.",
body="""
<article class="nh-card"><h3>Where do you operate?</h3><p>Two universities in Uganda, one in the DRC, Kyangwali and other refugee learners, and a Sunday room online with students elsewhere.</p></article>
<article class="nh-card"><h3>Is this slides?</h3><p>No. We create labs so you work in a live environment. Weekends on campus. Sundays together online. Experts visit. Facilitators sit with you.</p></article>
<article class="nh-card"><h3>What does it cost?</h3><p>About $25 a month, sometimes less. Refugee and underserved learners are supported by sponsors, NGOs, and institutions.</p></article>
<article class="nh-card"><h3>Do you work with small companies?</h3><p>Yes. Pentesting, awareness, hardening, forensics, network security, web-app security, WAF deployment. That work also funds free seats.</p></article>
<article class="nh-card"><h3>Is this Cybrary?</h3><p>No. This site used a visual template. The organization is Nethub, founded 2022.</p></article>
"""
),
"contact.html": dict(
title="Contact | Nethub",
desc="Reach Nethub for a campus seat, a sponsored cohort, or a scoped security engagement.",
kicker="Uganda · DRC · online Sundays",
h1="Talk to Nethub",
lead="Tell us whether you want a lab seat, a sponsored cohort, or a small-business engagement. We will point you to a facilitator, not a ticket bot.",
body="""
<img class="nh-photo" src="assets/nethub/photo-analyst.jpg" alt="Nethub practitioner at a terminal" style="margin-bottom:28px">
<div class="nh-grid-2">
<article class="nh-card"><h3>Learners</h3><p>Join a weekend campus session or the Sunday global lab. If $25 is too much, say so — we look for a sponsored seat.</p><p style="margin-top:16px"><a class="nh-btn nh-btn-primary" href="index.html#join">See how joining works</a></p></article>
<article class="nh-card"><h3>Sponsors, NGOs, companies</h3><p>Fund a cohort, host a lab, or hire us for pentesting, awareness, hardening, forensics, or a WAF. One contract can open several free seats.</p><p style="margin-top:16px"><a class="nh-btn nh-btn-ghost" href="business.html">Open services</a></p></article>
</div>
<article class="nh-card" style="margin-top:16px"><h3>People</h3><p>Kapata Divin (venture lead), Joseph Mugerwa (patron and advisor), Leonard Musonda (technical lead), and eleven facilitators across Uganda and DRC.</p></article>
"""
),
"join-our-team.html": dict(
title="Facilitate with Nethub",
desc="Advanced trainees become Nethub facilitators. Come teach the next cohort.",
kicker="Peer cycle",
h1="Facilitate with us",
lead="Graduates train the next room. That is how eleven facilitators already work across Uganda and DRC.",
body="""
<img class="nh-photo" src="assets/nethub/photo-command.jpg" alt="Facilitators in a cyber command environment" style="margin-bottom:28px">
<article class="nh-card"><h3>Who this is for</h3><p>Advanced trainees who can sit with a zero-baseline student, keep a lab honest, and show up on a weekend or a Sunday. Professors at partner campuses who want the club to be a real environment, not a slide club.</p></article>
<article class="nh-card"><h3>What you do</h3><p>Run the room. Invite an expert when you can. Keep one-on-one time. Point people toward cybersecurity work, not just another certificate tab.</p></article>
<article class="nh-card"><h3>How to raise your hand</h3><p>Use the contact page and say you want to facilitate. Tell us your campus or whether you can only join Sundays.</p></article>
"""
),
"responsible-disclosure-program.html": dict(
title="Responsible disclosure | Nethub",
desc="Tell Nethub if you find a security issue in our labs or public site.",
kicker="Security",
h1="If you find a hole, tell us",
lead="We teach people to find weaknesses. We expect the same honesty toward our own systems.",
body="""
<article class="nh-card"><h3>In scope</h3><p>The public Nethub site, lab infrastructure we operate, and systems we explicitly list in a statement of work. Not a university’s entire network unless they hired us for that.</p></article>
<article class="nh-card"><h3>How to report</h3><p>Use the contact page. Include steps, impact, and whether you already tested beyond a proof. Do not dump learner data in the ticket.</p></article>
<article class="nh-card"><h3>What we ask</h3><p>Give us a chance to fix before public write-ups. Do not ransom, do not pivot into student machines, do not DDoS the Sunday room.</p></article>
"""
),
}

for name, p in pages.items():
    html = HEAD.format(title=p["title"], desc=p["desc"])
    html += f"""
  <section class="nh-hero"><div class="nh-wrap">
    <div class="nh-kicker">{p['kicker']}</div>
    <h1>{p['h1']}</h1>
    <p class="nh-lead">{p['lead']}</p>
  </div></section>
  <section class="nh-section alt nh-legal"><div class="nh-wrap">{p['body']}</div></section>
"""
    html += FOOT
    (ROOT / name).write_text(html, encoding="utf-8")
    print("wrote", name)
