(function () {
  var depth = document.currentScript && document.currentScript.getAttribute("data-depth");
  var prefix = depth === "1" ? "../" : depth === "2" ? "../../" : "";
  var mark = prefix + "assets/nethub/logo-mark-inverse.jpg";
  var navLogo = prefix + "assets/nethub/logo-nav.png";
  var home = prefix + "index.html";
  var armyOps = prefix + "assets/nethub/cards/army-soc-wall.png";
  var socStaff = prefix + "assets/nethub/cards/nethub-soc-staff-dark.jpg";
  var campusLab = prefix + "assets/nethub/photos/lab-students.jpg";
  var photos = [
    socStaff,
    campusLab,
    prefix + "assets/nethub/photo-command.jpg",
    prefix + "assets/nethub/nethub-lab-room.jpg",
    prefix + "assets/nethub/photo-analyst.jpg"
  ];

  var I18N = {
    en: {
      "nav.places": "Places",
      "nav.allPlaces": "All places",
      "nav.uganda": "Uganda",
      "nav.drc": "DRC",
      "nav.community": "Community",
      "nav.learn": "For learners",
      "nav.companies": "For companies",
      "nav.labs": "Labs",
      "nav.catalog": "Catalog",
      "nav.sunday": "Sunday lab",
      "nav.exams": "Practice exams",
      "nav.join": "Join a lab",
      "nav.gallery": "Gallery",
      "nav.clubs": "Clubs",
      "nav.instructors": "Instructors",
      "nav.createClub": "Create a Nethub club in your institution",
      "nav.leaders": "Term leaders",
      "nav.pricing": "Pricing",
      "nav.services": "Services",
      "nav.about": "About",
      "nav.signin": "Sign in",
      "nav.logout": "Log out",
      "nav.desk": "Desk",
      "role.admin": "Admin",
      "role.student": "Student",
      "role.mentor": "Mentor",
      "mission.kicker": "Two offerings",
      "mission.title": "Learning is not the same as company services",
      "mission.body": "Students and individuals train in eight tracks. Companies hire scoped security work.",
      "org.kicker": "For companies",
      "org.title": "Security work on your network",
      "org.body": "Pentest, assessments, hardening, awareness, and forensics as engagements — not as a course.",
      "foot.blurb": "Hands-on cybersecurity and networking. Uganda, DRC, and Sunday labs worldwide.",
      "foot.practice": "Practice",
      "foot.nethub": "Nethub",
      "foot.policies": "Policies"
    },
    fr: {
      "nav.places": "Lieux",
      "nav.allPlaces": "Tous les lieux",
      "nav.uganda": "Ouganda",
      "nav.drc": "RDC",
      "nav.community": "Communauté",
      "nav.learn": "Pour les apprenants",
      "nav.companies": "Pour les entreprises",
      "nav.labs": "Labos",
      "nav.catalog": "Catalogue",
      "nav.sunday": "Labo du dimanche",
      "nav.exams": "Examens blancs",
      "nav.join": "Rejoindre un labo",
      "nav.gallery": "Galerie",
      "nav.clubs": "Clubs",
      "nav.instructors": "Instructeurs",
      "nav.createClub": "Créer un club Nethub dans votre institution",
      "nav.leaders": "Responsables de trimestre",
      "nav.pricing": "Tarifs",
      "nav.services": "Services",
      "nav.about": "À propos",
      "nav.signin": "Connexion",
      "nav.logout": "Déconnexion",
      "nav.desk": "Bureau",
      "role.admin": "Admin",
      "role.student": "Étudiant",
      "role.mentor": "Mentor",
      "mission.kicker": "Deux offres",
      "mission.title": "L’apprentissage n’est pas le service aux entreprises",
      "mission.body": "Les étudiants et les particuliers se forment sur huit parcours. Les entreprises commandent un travail de sécurité cadré.",
      "org.kicker": "Pour les entreprises",
      "org.title": "Travail de sécurité sur votre réseau",
      "org.body": "Tests d’intrusion, évaluations, durcissement, sensibilisation et forensics en mission — pas en cours.",
      "foot.blurb": "Cybersécurité et réseaux, en pratique. Ouganda, RDC, et labos du dimanche partout.",
      "foot.practice": "Pratique",
      "foot.nethub": "Nethub",
      "foot.policies": "Règles"
    }
  };

  function lang() {
    return localStorage.getItem("nethub_lang") === "fr" ? "fr" : "en";
  }

  function t(key) {
    var pack = I18N[lang()] || I18N.en;
    return pack[key] || I18N.en[key] || key;
  }

  function navHTML() {
    return (
      '<div class="nh-drop">' +
        '<button type="button" aria-haspopup="true">' + t("nav.places") + "</button>" +
        '<div class="nh-drop-menu">' +
          '<a href="' + prefix + 'places.html">' + t("nav.allPlaces") + "</a>" +
          '<a href="' + prefix + 'uganda.html">' + t("nav.uganda") + "</a>" +
          '<a href="' + prefix + 'drc.html">' + t("nav.drc") + "</a>" +
          '<a href="' + prefix + 'community.html">' + t("nav.community") + "</a>" +
        "</div>" +
      "</div>" +
      '<div class="nh-drop">' +
        '<button type="button" aria-haspopup="true">' + t("nav.labs") + "</button>" +
        '<div class="nh-drop-menu">' +
          '<a href="' + prefix + 'catalog.html">' + t("nav.catalog") + "</a>" +
          '<a href="' + prefix + 'sunday-lab.html">' + t("nav.sunday") + "</a>" +
          '<a href="' + prefix + 'practice-exams.html">' + t("nav.exams") + "</a>" +
          '<a href="' + prefix + 'register.html">' + t("nav.join") + "</a>" +
        "</div>" +
      "</div>" +
      '<a href="' + prefix + 'gallery.html">' + t("nav.gallery") + "</a>" +
      '<div class="nh-drop">' +
        '<button type="button" aria-haspopup="true">' + t("nav.clubs") + "</button>" +
        '<div class="nh-drop-menu">' +
          '<a href="' + prefix + 'instructor.html">' + t("nav.instructors") + "</a>" +
          '<a href="' + prefix + 'club-create.html">' + t("nav.createClub") + "</a>" +
          '<a href="' + prefix + 'leaders.html">' + t("nav.leaders") + "</a>" +
        "</div>" +
      "</div>" +
      '<a href="' + prefix + 'pricing.html">' + t("nav.pricing") + "</a>" +
      '<div class="nh-drop">' +
        '<button type="button" aria-haspopup="true">' + t("nav.services") + "</button>" +
        '<div class="nh-drop-menu">' +
          '<a href="' + prefix + 'about.html#learn">' + t("nav.learn") + "</a>" +
          '<a href="' + prefix + 'business.html">' + t("nav.companies") + "</a>" +
        "</div>" +
      "</div>" +
      '<a href="' + prefix + 'about.html">' + t("nav.about") + "</a>"
    );
  }

  function chrome() {
    return (
      '<header class="nh-nav" id="nav">' +
        '<div class="nh-wrap">' +
          '<div class="nh-nav-top">' +
            '<a class="nh-brand" href="' + home + '"><img src="' + navLogo + '" alt="Nethub"></a>' +
            '<nav class="nh-nav-links">' + navHTML() + "</nav>" +
            '<div class="nh-nav-tools"></div>' +
            '<button class="nh-menu-btn" type="button" aria-label="Menu" onclick="document.getElementById(\'nav\').classList.toggle(\'open\')">Menu</button>' +
          "</div>" +
        "</div>" +
      "</header>"
    );
  }

  function foot() {
    return (
      '<footer class="nh-footer">' +
        '<div class="nh-wrap nh-footer-grid">' +
          "<div>" +
            '<a class="nh-brand" href="' + home + '"><img src="' + navLogo + '" alt="Nethub"></a>' +
            "<p data-i18n=\"foot.blurb\">Hands-on cybersecurity and networking. Uganda, DRC, and Sunday labs worldwide.</p>" +
          "</div>" +
          "<div><h4 data-i18n=\"foot.practice\">Practice</h4><ul>" +
            '<li><a href="' + prefix + 'catalog.html">' + t("nav.labs") + "</a></li>" +
            '<li><a href="' + prefix + 'practice-exams.html">' + t("nav.exams") + "</a></li>" +
            '<li><a href="' + prefix + 'news.html">News</a></li>' +
            '<li><a href="' + prefix + 'pricing.html">' + t("nav.pricing") + "</a></li>" +
            '<li><a href="' + prefix + 'business.html">' + t("nav.services") + "</a></li>" +
          "</ul></div>" +
          "<div><h4 data-i18n=\"foot.nethub\">Nethub</h4><ul>" +
            '<li><a href="' + prefix + 'about.html">' + t("nav.about") + "</a></li>" +
            '<li><a href="' + prefix + 'instructor.html">' + t("nav.instructors") + "</a></li>" +
            '<li><a href="' + prefix + 'gallery.html">' + t("nav.gallery") + "</a></li>" +
            '<li><a href="' + prefix + 'join-our-team.html">Facilitate</a></li>' +
            '<li><a href="' + prefix + 'contact.html">Contact</a></li>' +
            '<li><a href="' + prefix + 'platform.html">Platform</a></li>' +
          "</ul></div>" +
          "<div><h4>Policies</h4><ul>" +
            '<li><a href="' + prefix + 'privacy-policy.html">Privacy</a></li>' +
            '<li><a href="' + prefix + 'terms-service.html">Terms</a></li>' +
            '<li><a href="' + prefix + 'cookie-policy.html">Cookies</a></li>' +
            '<li><a href="' + prefix + 'faq.html">FAQ</a></li>' +
          "</ul></div>" +
        "</div>" +
        '<div class="nh-wrap nh-copy">© 2026 Nethub. Building Africa’s cybersecurity future from the inside out.</div>' +
      "</footer>"
    );
  }

  function looksCybrary(el) {
    var src = (el.getAttribute("src") || "") + " " + (el.getAttribute("srcset") || "");
    var blob = (src + " " + (el.alt || "")).toLowerCase();
    if (/assets\/nethub\//i.test(src)) return false;
    if (/cybrary|logo-full-white|cybrary-logo/.test(blob)) return true;
    if (/website-files/i.test(src) && /\.(webp|jpg|jpeg|png)/i.test(src) && !/\.svg/i.test(src)) return true;
    return false;
  }

  var titles = ["Pentest lab", "SOC floor", "Network lab", "Awareness", "Cert prep", "Career lab"];

  function fanMarkup() {
    var cards = [
      { tag: "SUNDAY LAB", pill: "LIVE", title: "Night watch: packet paths", meta: "SOC · 4 rooms", img: armyOps },
      { tag: "CAMPUS", pill: "ON SITE", title: "Lab floor, live terminals", meta: "Network · campus", img: campusLab },
      { tag: "SOC", pill: "STAFF", title: "Professional night desk", meta: "Analysts · live monitors", img: socStaff }
    ];
    return (
      '<div class="nh-fan">' +
      cards
        .map(function (c) {
          return (
            '<article class="nh-fan-card"><div class="nh-fan-copy"><div class="nh-fan-tags"><span>' +
            c.tag +
            '</span><span class="hot">' +
            c.pill +
            "</span></div><h3>" +
            c.title +
            "</h3><p>" +
            c.meta +
            '</p></div><div class="nh-fan-photo"><img src="' +
            c.img +
            '" alt=""></div></article>'
          );
        })
        .join("") +
      "</div>"
    );
  }

  function replaceStackedCards() {
    document.querySelectorAll(".card-component, .testimonial-slider_background-cards").forEach(function (el) {
      var wrap = document.createElement("div");
      wrap.innerHTML = fanMarkup();
      el.replaceWith(wrap.firstChild);
    });
    document.querySelectorAll("img.announcement-hero_image, img.career-path_hero-image").forEach(function (img) {
      var wrap = document.createElement("div");
      wrap.innerHTML = fanMarkup();
      img.replaceWith(wrap.firstChild);
    });
  }

  function animateAndBrandCards() {
    var i = 0;
    document.querySelectorAll(".card-component img, .card-component_item img, .career-path_hero-image img, .left-align-tabs_image").forEach(function (img) {
      if (looksCybrary(img)) {
        img.src = photos[i % photos.length];
        img.removeAttribute("srcset");
        img.alt = "Nethub " + titles[i % titles.length];
      }
      img.classList.add("nh-float-img");
      img.style.animationDuration = 52 + (i % 5) * 10 + "s";
      img.style.animationDelay = -(i * 9) + "s";
      i += 1;
    });
  }

  function dropBadgeBlocks() {
    document.querySelectorAll("h2, h3, h5, .heading-style-h5, .heading-style-h3").forEach(function (h) {
      var t = (h.textContent || "").replace(/\s+/g, " ").trim();
      if (!/badge/i.test(t)) return;
      if (!/earn|credly|industry/i.test(t)) return;
      var box = h.closest("._3-features_item") || h.closest("article");
      if (box) box.remove();
    });
  }

  function replaceCybraryCopy() {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    var node;
    while ((node = walker.nextNode())) {
      if (!node.nodeValue) continue;
      if (/Cybrary|CYBRARY/.test(node.nodeValue)) {
        node.nodeValue = node.nodeValue.replace(/CYBRARY/g, "NETHUB").replace(/Cybrary/g, "Nethub");
      }
    }
  }

  function swapImages() {
    var i = 0;
    document.querySelectorAll("img").forEach(function (img) {
      if (!looksCybrary(img)) return;
      img.src = photos[i % photos.length];
      img.removeAttribute("srcset");
      img.alt = "Nethub";
      img.style.objectFit = "cover";
      i += 1;
    });
  }

  function injectChrome() {
    if (document.body.classList.contains("nethub-site")) return;
    if (document.getElementById("nav")) return;
    document.body.insertAdjacentHTML("afterbegin", chrome());
    document.body.insertAdjacentHTML("beforeend", foot());
  }

  var snakePaths = [
    { d: "M 20 240 C 180 40, 340 420, 560 160 S 880 40, 1180 300", a: [20, 240], b: [1180, 300] },
    { d: "M 1180 90 C 920 280, 700 20, 460 250 S 180 430, 30 170", a: [1180, 90], b: [30, 170] },
    { d: "M 40 480 C 280 560, 500 120, 760 500 S 1040 160, 1180 380", a: [40, 480], b: [1180, 380] },
    { d: "M 80 40 C 260 220, 520 80, 740 360 S 1020 120, 1160 520", a: [80, 40], b: [1160, 520] },
    { d: "M 1160 430 C 880 520, 640 180, 400 420 S 160 80, 40 260", a: [1160, 430], b: [40, 260] }
  ];

  var snakeColors = {
    index: ["#4a8ad4", "#c026d3", "#22d3ee", "#f59e0b", "#34d399"],
    about: ["#c026d3", "#818cf8", "#fb7185"],
    business: ["#38bdf8", "#fbbf24", "#2dd4bf"],
    catalog: ["#a78bfa", "#34d399", "#60a5fa"],
    contact: ["#f472b6", "#38bdf8"],
    faq: ["#4ade80", "#818cf8"],
    "join-our-team": ["#fb923c", "#67e8f9"],
    "privacy-policy": ["#67e8f9", "#a78bfa"],
    "terms-service": ["#94a3b8", "#60a5fa"],
    "cookie-policy": ["#c4b5fd", "#22d3ee"]
  };

  function pageKey() {
    var file = (location.pathname.split("/").pop() || "index.html").replace(/\.html$/i, "");
    if (!file || file === "") return "index";
    return file;
  }

  function snakeMarkup(color, spec, duration, delay) {
    return (
      '<svg class="nh-snake" viewBox="0 0 1200 700" preserveAspectRatio="none" aria-hidden="true">' +
        '<path class="nh-snake-glow" d="' + spec.d + '" style="stroke:' + color + ";animation-duration:" + duration + "s;animation-delay:-" + delay + 's"></path>' +
        '<path class="nh-snake-core" d="' + spec.d + '" style="stroke:' + color + ";color:" + color + ";animation-duration:" + duration + "s;animation-delay:-" + delay + 's"></path>' +
        '<circle class="nh-snake-node" cx="' + spec.a[0] + '" cy="' + spec.a[1] + '" r="4" fill="' + color + '" style="color:' + color + '"></circle>' +
        '<circle class="nh-snake-node" cx="' + spec.b[0] + '" cy="' + spec.b[1] + '" r="4" fill="' + color + '" style="color:' + color + ';animation-delay:-3s"></circle>' +
      "</svg>"
    );
  }

  function injectSnakes() {
    var key = pageKey();
    var colors = snakeColors[key] || ["#4a8ad4", "#c026d3", "#22d3ee"];
    var hosts = Array.prototype.slice.call(document.querySelectorAll(".nh-hero, .nh-section"));
    if (!hosts.length) {
      var page = document.createElement("div");
      page.className = "nh-snake-page";
      document.body.insertBefore(page, document.body.firstChild);
      hosts = [page];
    }
    hosts.forEach(function (host, i) {
      if (host.querySelector(".nh-snake")) return;
      var color = colors[i % colors.length];
      var spec = snakePaths[i % snakePaths.length];
      var duration = 28 + (i % 4) * 6;
      var delay = (i * 7) % 24;
      if (getComputedStyle(host).position === "static") host.style.position = "relative";
      host.insertAdjacentHTML("afterbegin", snakeMarkup(color, spec, duration, delay));
    });
  }

  function wireJoinLinks() {
    var seat = prefix + "register.html";
    var dash = prefix + "dashboard.html";
    var signed = !!localStorage.getItem("nethub_token");
    document.querySelectorAll("a").forEach(function (a) {
      if (a.closest(".nh-nav-tools")) return;
      if (a.getAttribute("data-nh-logout")) return;
      var label = (a.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
      if (/team|facilitate|partner|hire the work|commander une mission/.test(label)) return;
      if (!/(join a lab|rejoindre un labo|enrol|enroll|sign up|create a seat|créer une place|create account|créer le compte|join today|start learning)/.test(label)) return;
      a.href = signed ? dash : seat;
      if (signed && /(join a lab|rejoindre un labo)/.test(label)) a.textContent = t("nav.desk");
    });
  }

  function applyFooter() {
    document.querySelectorAll(".nh-footer-grid").forEach(function (grid) {
      var col = grid.children[2];
      if (!col) return;
      var ul = col.querySelector("ul");
      if (!ul) return;
      if (!ul.querySelector('a[href*="about.html"]')) {
        var about = document.createElement("li");
        about.innerHTML = '<a href="' + prefix + 'about.html">' + t("nav.about") + "</a>";
        ul.insertBefore(about, ul.firstChild);
      }
      if (!ul.querySelector('a[href*="platform.html"]')) {
        var li = document.createElement("li");
        li.innerHTML = '<a href="' + prefix + 'platform.html">Platform</a>';
        ul.appendChild(li);
      }
    });
  }

  function sessionUser() {
    try {
      return JSON.parse(localStorage.getItem("nethub_user") || "null");
    } catch (e) {
      return null;
    }
  }

  function roleKey(user) {
    var r = (user && user.role) || "student";
    if (r === "admin") return "role.admin";
    if (r === "mentor") return "role.mentor";
    return "role.student";
  }

  function applySessionTools() {
    var top = document.querySelector(".nh-nav-top");
    if (!top) return;
    var tools = top.querySelector(".nh-nav-tools");
    if (!tools) {
      tools = document.createElement("div");
      tools.className = "nh-nav-tools";
      var menu = top.querySelector(".nh-menu-btn");
      if (menu) top.insertBefore(tools, menu);
      else top.appendChild(tools);
    }
    var cta = top.querySelector(".nh-nav-cta");
    if (cta) cta.remove();
    var user = sessionUser();
    var token = localStorage.getItem("nethub_token");
    var cur = lang();
    var sessionHtml = "";
    if (token && user && user.name) {
      var desk = user.role === "admin" ? prefix + "admin.html" : prefix + "dashboard.html";
      sessionHtml =
        '<span class="nh-role-pill">' +
        t(roleKey(user)) +
        "</span>" +
        '<a class="nh-session-name" href="' +
        desk +
        '">' +
        String(user.name).split(" ")[0] +
        "</a>" +
        '<a class="nh-btn nh-btn-ghost" href="#" data-nh-logout="1">' +
        t("nav.logout") +
        "</a>";
    } else {
      sessionHtml =
        '<a class="nh-btn nh-btn-ghost" href="' +
        prefix +
        'login.html">' +
        t("nav.signin") +
        "</a>" +
        '<a class="nh-btn nh-btn-primary nh-nav-cta" href="' +
        prefix +
        'register.html">' +
        t("nav.join") +
        "</a>";
    }
    tools.innerHTML =
      '<div class="nh-lang" role="group" aria-label="Language">' +
      '<button type="button" class="nh-lang-btn' +
      (cur === "en" ? " is-on" : "") +
      '" data-lang-set="en">EN</button>' +
      '<button type="button" class="nh-lang-btn' +
      (cur === "fr" ? " is-on" : "") +
      '" data-lang-set="fr">FR</button>' +
      "</div>" +
      sessionHtml;
  }

  function applyI18n() {
    document.documentElement.lang = lang() === "fr" ? "fr" : "en";
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (key && I18N.en[key]) el.textContent = t(key);
    });
    var en2fr = {};
    var fr2en = {};
    function addPair(en, fr) {
      if (!en || !fr) return;
      var a = String(en).replace(/\s+/g, " ").trim();
      var b = String(fr).replace(/\s+/g, " ").trim();
      en2fr[a] = b;
      fr2en[b] = a;
    }
    Object.keys(I18N.en).forEach(function (k) {
      addPair(I18N.en[k], I18N.fr[k]);
    });
    (window.NETHUB_I18N_PAIRS || []).forEach(function (p) {
      addPair(p[0], p[1]);
    });
    function flip(raw) {
      if (raw == null) return raw;
      var lead = String(raw).match(/^\s*/)[0];
      var trail = String(raw).match(/\s*$/)[0];
      var mid = String(raw).slice(lead.length, String(raw).length - trail.length).replace(/\s+/g, " ").trim();
      if (!mid) return raw;
      var next = lang() === "fr" ? en2fr[mid] : fr2en[mid];
      return next ? lead + next + trail : raw;
    }
    var skip = /^(SCRIPT|STYLE|NOSCRIPT|TEXTAREA|CODE|PRE|SVG)$/;
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var p = node.parentElement;
        if (!p || skip.test(p.tagName)) return NodeFilter.FILTER_REJECT;
        if (p.closest(".nh-lang, [data-no-i18n], input, textarea")) return NodeFilter.FILTER_REJECT;
        if (!node.nodeValue || !node.nodeValue.replace(/\s/g, "")) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) {
      var out = flip(n.nodeValue);
      if (out !== n.nodeValue) n.nodeValue = out;
    }
    document.querySelectorAll("[alt], [title], [placeholder], [aria-label]").forEach(function (el) {
      if (el.closest(".nh-lang")) return;
      ["alt", "title", "placeholder", "aria-label"].forEach(function (attr) {
        if (!el.hasAttribute(attr)) return;
        var v = flip(el.getAttribute(attr));
        if (v) el.setAttribute(attr, v);
      });
    });
    document.querySelectorAll("button, a.nh-btn").forEach(function (el) {
      if (el.closest(".nh-lang")) return;
    });
    document.title = flip(document.title) || document.title;
    var meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute("content", flip(meta.getAttribute("content")));
    document.querySelectorAll("img").forEach(function (img) {
      var want = img.getAttribute("data-src-" + lang());
      if (want) {
        if (!img.getAttribute("data-src-en")) img.setAttribute("data-src-en", img.getAttribute("src") || "");
        img.src = want;
        return;
      }
      var src = img.getAttribute("src") || "";
      if (lang() === "fr" && /-en(\.[a-z0-9]+)$/i.test(src)) {
        img.setAttribute("data-src-en", src);
        img.src = src.replace(/-en(\.[a-z0-9]+)$/i, "-fr$1");
      } else if (lang() === "en" && img.getAttribute("data-src-en")) {
        img.src = img.getAttribute("data-src-en");
      } else if (lang() === "en" && /-fr(\.[a-z0-9]+)$/i.test(src)) {
        img.src = src.replace(/-fr(\.[a-z0-9]+)$/i, "-en$1");
      }
    });
    window.nethubPhrase = flip;
    document.dispatchEvent(new CustomEvent("nethub:lang", { detail: { lang: lang() } }));
  }

  function loadI18nDict(done) {
    if (window.NETHUB_I18N_PAIRS) {
      done();
      return;
    }
    var s = document.createElement("script");
    s.src = prefix + "assets/nethub/i18n-dict.js";
    s.onload = done;
    s.onerror = done;
    document.head.appendChild(s);
  }

  function neutralizeHostileLinks() {
    document.querySelectorAll("a[href]").forEach(function (a) {
      var href = (a.getAttribute("href") || "").toLowerCase();
      if (/cybrary/.test(href) || /app\.cybrary/.test(href)) {
        a.setAttribute("href", prefix + "about.html");
        a.removeAttribute("target");
      }
    });
  }

  function glassNav() {
    var nav = document.getElementById("nav") || document.querySelector(".nh-nav");
    if (!nav) return;
    function tick() {
      nav.classList.toggle("is-scrolled", window.scrollY > 10);
    }
    tick();
    window.addEventListener("scroll", tick, { passive: true });
  }

  function brandOffensiveArmy() {
    if (!/offensive/i.test(location.pathname + " " + document.title)) return;
    var swapped = 0;
    document.querySelectorAll("img").forEach(function (img) {
      var src = (img.getAttribute("src") || "") + " " + (img.className || "");
      if (/logo|svg|marquee|social|google|favicon|wordmark|avatar|instructor/i.test(src)) return;
      if (!looksCybrary(img) && !/hero|career|header|catalog-hero|Get-Hands-On|HP-Learn|HP-Practice|HP-Prove/i.test(src)) return;
      img.src = armyOps;
      img.removeAttribute("srcset");
      img.alt = "Nethub offensive security — army cyber operations";
      img.style.objectFit = "cover";
      swapped += 1;
    });
    var title = document.querySelector(".career_details_content .career-path-title")
      || document.querySelector(".career_section_header_main h1")
      || document.querySelector("h1.heading-style-h1");
    if (title && !document.querySelector(".nh-army-hero")) {
      var img = document.createElement("img");
      img.className = "nh-army-hero";
      img.src = armyOps;
      img.alt = "Army cyber operations";
      title.insertAdjacentElement("afterend", img);
    }
  }
  function cmsEsc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function cardsOf(data, section) {
    return (data.cards || []).filter(function (c) {
      return c.section === section;
    });
  }

  function applyGrade(wrap, rec) {
    if (!wrap || !rec) return;
    wrap.style.setProperty("--nh-ov-color", rec.overlay_color || "#050a12");
    wrap.style.setProperty("--nh-ov-op", String((rec.overlay_opacity != null ? rec.overlay_opacity : 50) / 100));
    wrap.style.setProperty("--nh-img-op", String((rec.img_opacity != null ? rec.img_opacity : 100) / 100));
    wrap.style.setProperty("--nh-img-bw", rec.bw ? "1" : "0");
    wrap.style.setProperty("--nh-img-br", String((rec.brightness != null ? rec.brightness : 100) / 100));
    if (rec.photo_h && !wrap.classList.contains("nh-fan-photo")) {
      wrap.style.setProperty("--nh-img-h", rec.photo_h + "px");
      if (wrap.classList.contains("nh-course-photos")) wrap.style.height = rec.photo_h + "px";
    }
  }

  function gradeCss(rec) {
    if (!rec) return "";
    var parts = [
      "--nh-ov-color:" + (rec.overlay_color || "#050a12"),
      "--nh-ov-op:" + (rec.overlay_opacity != null ? rec.overlay_opacity : 50) / 100,
      "--nh-img-op:" + (rec.img_opacity != null ? rec.img_opacity : 100) / 100,
      "--nh-img-bw:" + (rec.bw ? 1 : 0),
      "--nh-img-br:" + (rec.brightness != null ? rec.brightness : 100) / 100
    ];
    if (rec.photo_h) parts.push("--nh-img-h:" + rec.photo_h + "px");
    return parts.join(";");
  }

  function applyCms(data) {
    if (!data) return;
    var photos = data.photos || {};
    Object.keys(photos).forEach(function (slot) {
      var rec = photos[slot];
      document.querySelectorAll('[data-cms-photo="' + slot + '"]').forEach(function (el) {
        var img = el.tagName === "IMG" ? el : el.querySelector("img");
        if (!img) return;
        img.src = rec.url;
        if (rec.alt) img.alt = rec.alt;
        var wrap = img.closest(".nh-photo-dark, .nh-fan-photo, .nh-course-photos");
        if (wrap) applyGrade(wrap, rec);
      });
      if (slot === "logo-nav") {
        document.querySelectorAll(".nh-nav .nh-brand img").forEach(function (img) {
          img.src = rec.url;
        });
      }
      if (slot === "logo-footer") {
        document.querySelectorAll(".nh-footer .nh-brand img").forEach(function (img) {
          img.src = rec.url;
        });
      }
    });
    var pages = data.pages || {};
    document.querySelectorAll("[data-cms-page]").forEach(function (el) {
      var rec = pages[el.getAttribute("data-cms-page")];
      if (!rec) return;
      var field = el.getAttribute("data-cms-field") || "title";
      if (rec[field]) el.textContent = rec[field];
    });
    var settings = data.settings || {};
    var root = document.documentElement;
    if (settings.card_color_1) root.style.setProperty("--nh-course-1", settings.card_color_1);
    if (settings.card_color_2) root.style.setProperty("--nh-course-2", settings.card_color_2);
    if (settings.card_color_3) root.style.setProperty("--nh-course-3", settings.card_color_3);
    if (settings.accent) root.style.setProperty("--nh-blue-bright", settings.accent);
    if (settings.site_tagline) {
      var hero = document.querySelector(".nh-hero h1");
      if (hero && /talent exists/i.test(hero.textContent || "")) hero.textContent = settings.site_tagline;
    }
    (data.cards || []).forEach(function (card) {
      document.querySelectorAll('[data-cms-card="' + card.id + '"], [data-cms-card-section="' + card.section + '"][data-cms-card-order="' + card.sort_order + '"]').forEach(function (el) {
        var h = el.querySelector("h3");
        var p = el.querySelector("p");
        var cta = el.querySelector(".nh-tile-cta");
        var img = el.querySelector("img");
        if (h) h.textContent = card.title;
        if (p) p.textContent = card.body || "";
        if (cta && card.cta) cta.textContent = card.cta;
        if (card.href) el.setAttribute("href", card.href);
        if (card.color) el.style.background = "linear-gradient(180deg, rgba(8,12,20,0.08), rgba(8,12,20,0.55)), " + card.color;
        if (img && card.image_url) img.src = card.image_url;
        var wrap = el.querySelector(".nh-course-photos, .nh-photo-dark");
        if (wrap) applyGrade(wrap, card);
      });
    });
    var train = document.getElementById("nh-train");
    if (train) {
      var trainCards = cardsOf(data, "train");
      if (trainCards.length) {
        train.innerHTML = trainCards
          .map(function (c) {
            return (
              '<a class="nh-course" href="' +
              cmsEsc(c.href || "catalog.html") +
              '">' +
              (c.image_url ? '<div class="nh-course-photos" style="' + gradeCss(c) + '"><img src="' + cmsEsc(c.image_url) + '" alt=""></div>' : "") +
              "<h3>" +
              cmsEsc(c.title) +
              "</h3><p>" +
              cmsEsc(c.body || "") +
              '</p><span class="nh-tile-cta">' +
              cmsEsc(c.cta || "Open") +
              "</span></a>"
            );
          })
          .join("");
      }
    }
    var community = document.getElementById("nh-community-cards");
    if (community) {
      var communityCards = cardsOf(data, "community");
      if (communityCards.length) {
        community.innerHTML = communityCards
          .map(function (c) {
            return (
              '<a class="nh-course nh-course-text" href="' +
              cmsEsc(c.href || "community.html") +
              '"><h3>' +
              cmsEsc(c.title) +
              "</h3><p>" +
              cmsEsc(c.body || "") +
              '</p><span class="nh-tile-cta">' +
              cmsEsc(c.cta || "Open") +
              "</span></a>"
            );
          })
          .join("");
      }
    }
    var places = document.getElementById("nh-places");
    if (places) {
      var placeCards = cardsOf(data, "places");
      if (placeCards.length) {
        places.innerHTML = placeCards
          .map(function (c) {
            return (
              '<a class="nh-tile" href="' +
              cmsEsc(c.href || "#") +
              '">' +
              (c.image_url
                ? '<span class="nh-photo-dark" style="' + gradeCss(c) + '"><img src="' + cmsEsc(c.image_url) + '" alt="' + cmsEsc(c.title) + '"></span>'
                : "") +
              "<h3>" +
              cmsEsc(c.title) +
              "</h3>" +
              (c.body ? "<p>" + cmsEsc(c.body) + "</p>" : "") +
              "</a>"
            );
          })
          .join("");
      }
    }
    var gallery = document.getElementById("nh-gallery");
    if (gallery) {
      gallery.innerHTML = (data.gallery || [])
        .map(function (g) {
          return (
            "<figure><span class=\"nh-photo-dark\" style=\"" +
            gradeCss(g) +
            '"><img src="' +
            cmsEsc(g.photo_url) +
            '" alt="' +
            cmsEsc(g.title || "") +
            '"></span><figcaption><strong>' +
            cmsEsc(g.title || "") +
            "</strong><p>" +
            cmsEsc(g.caption || "") +
            "</p></figcaption></figure>"
          );
        })
        .join("") || "<p>The desk has not published photos yet.</p>";
    }
    var sessions = document.getElementById("nh-sessions");
    if (sessions) {
      sessions.innerHTML = (data.sessions || [])
        .map(function (s) {
          return (
            '<article class="nh-card"><div class="nh-tag">Online session</div><h3>' +
            cmsEsc(s.title) +
            "</h3><p>" +
            cmsEsc(s.starts_at || "") +
            "<br>" +
            cmsEsc(s.notes || "") +
            "</p>" +
            (s.join_url
              ? '<a class="nh-btn nh-btn-primary" href="' + cmsEsc(s.join_url) + '">Join</a>'
              : "") +
            "</article>"
          );
        })
        .join("") || (sessions.closest(".nh-hero") ? "" : "<p>No live session posted yet.</p>");
    }
    var notes = document.getElementById("desk-notes");
    if (notes) {
      notes.innerHTML = (data.messages || [])
        .map(function (m) {
          return (
            '<article class="nh-card"><div class="nh-tag">Desk</div><p>' +
            cmsEsc(m.body) +
            "</p><p class=\"intro\">" +
            cmsEsc(m.from_name || "Desk") +
            " · " +
            cmsEsc(m.created_at || "") +
            "</p></article>"
          );
        })
        .join("");
    }
    var grid = document.getElementById("nh-instructors");
    if (grid) {
      grid.innerHTML = (data.instructors || [])
        .map(function (p) {
          return (
            '<article class="nh-card nh-instructor">' +
            (p.photo_url ? '<div class="nh-photo-dark" style="' + gradeCss(p) + '"><img src="' + p.photo_url + '" alt="' + (p.name || "") + '"></div>' : "") +
            "<h3>" +
            (p.name || "") +
            "</h3><p class=\"nh-tag\">" +
            (p.title || "Instructor") +
            "</p><p>" +
            (p.bio || "") +
            "</p></article>"
          );
        })
        .join("") || "<p>The desk has not published instructors yet.</p>";
    }
  }

  function loadCms() {
    fetch("/api/cms")
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        applyCms(data);
        applyI18n();
      })
      .catch(function () {});
  }

  function applyNav() {
    var nav = document.querySelector(".nh-nav-links");
    if (nav) nav.innerHTML = navHTML();
    document.querySelectorAll(".nh-drop > button").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var box = btn.parentElement;
        document.querySelectorAll(".nh-drop.open").forEach(function (d) {
          if (d !== box) d.classList.remove("open");
        });
        box.classList.toggle("open");
      });
    });
    applySessionTools();
  }

  document.addEventListener("click", function (e) {
    var langBtn = e.target.closest("[data-lang-set]");
    if (langBtn) {
      localStorage.setItem("nethub_lang", langBtn.getAttribute("data-lang-set"));
      applyNav();
      applyI18n();
      wireJoinLinks();
      return;
    }
    var out = e.target.closest("[data-nh-logout]");
    if (out) {
      e.preventDefault();
      localStorage.removeItem("nethub_token");
      localStorage.removeItem("nethub_user");
      location.href = prefix + "index.html";
    }
  });

  document.addEventListener("DOMContentLoaded", function () {
    loadI18nDict(function () {
      injectChrome();
      applyNav();
      glassNav();
      applyFooter();
      swapImages();
      replaceStackedCards();
      animateAndBrandCards();
      brandOffensiveArmy();
      replaceCybraryCopy();
      neutralizeHostileLinks();
      dropBadgeBlocks();
      injectSnakes();
      wireJoinLinks();
      applyI18n();
      loadCms();
      document.title = document.title.replace(/Cybrary/g, "Nethub");
      var icon = document.querySelector('link[rel="shortcut icon"], link[rel="icon"]');
      if (icon) icon.href = mark;
    });
  });
})();
