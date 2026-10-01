(function () {
  var raw = localStorage.getItem("nethub_user");
  var user = raw ? JSON.parse(raw) : null;
  if (!user || user.role !== "admin" || !localStorage.getItem("nethub_token")) {
    location.href = "platform.html";
    return;
  }

  var err = document.getElementById("admin-err");
  var state = { instructors: [], photos: {}, cards: [], settings: {}, users: [], pages: {}, gallery: [], sessions: [], messages: [], me: null };

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function showErr(ex) {
    err.textContent = ex && ex.message ? ex.message : String(ex || "");
  }

  function gradeBody(prefix) {
    return {
      overlay_color: document.getElementById(prefix + "-ov-color").value,
      overlay_opacity: Number(document.getElementById(prefix + "-ov-opacity").value),
      img_opacity: Number(document.getElementById(prefix + "-img-opacity").value),
      photo_h: Number(document.getElementById(prefix + "-h").value || 0),
      brightness: Number(document.getElementById(prefix + "-br").value),
      bw: document.getElementById(prefix + "-bw").checked ? 1 : 0
    };
  }

  function fillGrade(prefix, rec) {
    rec = rec || {};
    document.getElementById(prefix + "-ov-color").value = rec.overlay_color || "#050a12";
    document.getElementById(prefix + "-ov-opacity").value = rec.overlay_opacity != null ? rec.overlay_opacity : 50;
    document.getElementById(prefix + "-img-opacity").value = rec.img_opacity != null ? rec.img_opacity : 100;
    document.getElementById(prefix + "-h").value = rec.photo_h || 0;
    document.getElementById(prefix + "-br").value = rec.brightness != null ? rec.brightness : 100;
    document.getElementById(prefix + "-bw").checked = !!rec.bw;
  }

  function upload(file, slot, alt) {
    var fd = new FormData();
    fd.append("file", file);
    if (slot) fd.append("slot", slot);
    if (alt) fd.append("alt", alt);
    var headers = {};
    if (nethubAuth.token()) headers.Authorization = "Bearer " + nethubAuth.token();
    return fetch("/api/admin/upload", { method: "POST", headers: headers, body: fd }).then(function (res) {
      return res.json().then(function (data) {
        if (!res.ok) throw new Error(data.error || "Upload failed");
        return data;
      });
    });
  }

  function load() {
    return nethubAuth.api("/admin/cms").then(function (data) {
      state.instructors = data.instructors || [];
      state.photos = data.photos || {};
      state.cards = data.cards || [];
      state.settings = data.settings || {};
      state.users = data.users || [];
      state.pages = data.pages || {};
      state.gallery = data.gallery || [];
      state.sessions = data.sessions || [];
      state.messages = data.messages || [];
      state.me = data.me || user;
      renderInstructors();
      renderPhotos();
      renderCards();
      renderColors();
      renderUsers();
      renderPages();
      renderGallery();
      renderSessions();
      renderMessages();
      renderStaff();
    });
  }

  function renderInstructors() {
    var box = document.getElementById("admin-instructors");
    box.innerHTML = state.instructors
      .map(function (p) {
        return (
          '<article class="nh-card nh-admin-item" data-id="' +
          p.id +
          '">' +
          (p.photo_url ? '<img class="nh-admin-thumb" src="' + esc(p.photo_url) + '" alt="">' : "") +
          "<h3>" +
          esc(p.name) +
          "</h3><p>" +
          esc(p.title || "") +
          "<br>" +
          esc(p.bio || "") +
          '</p><div class="nh-admin-actions">' +
          '<button type="button" class="nh-btn nh-btn-ghost" data-edit-instructor="' +
          p.id +
          '">Edit</button>' +
          '<button type="button" class="nh-btn nh-btn-ghost" data-del-instructor="' +
          p.id +
          '">Delete</button></div></article>'
        );
      })
      .join("") || "<p>No instructors yet.</p>";
  }

  function fillInstructor(p) {
    document.getElementById("ins-id").value = p ? p.id : "";
    document.getElementById("ins-name").value = p ? p.name : "";
    document.getElementById("ins-title").value = p ? p.title || "" : "";
    document.getElementById("ins-bio").value = p ? p.bio || "" : "";
    document.getElementById("ins-photo").value = p ? p.photo_url || "" : "";
    document.getElementById("ins-order").value = p ? p.sort_order : 0;
    fillGrade("ins", p);
  }

  document.getElementById("ins-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var id = document.getElementById("ins-id").value;
    var body = {
      name: document.getElementById("ins-name").value,
      title: document.getElementById("ins-title").value,
      bio: document.getElementById("ins-bio").value,
      photo_url: document.getElementById("ins-photo").value,
      sort_order: Number(document.getElementById("ins-order").value || 0),
      published: 1
    };
    Object.assign(body, gradeBody("ins"));
    var file = document.getElementById("ins-file").files[0];
    var go = file
      ? upload(file).then(function (up) {
          body.photo_url = up.url;
        })
      : Promise.resolve();
    go.then(function () {
      if (id) return nethubAuth.api("/admin/instructors/" + id, { method: "PUT", body: body });
      return nethubAuth.api("/admin/instructors", { method: "POST", body: body });
    })
      .then(function () {
        document.getElementById("ins-file").value = "";
        fillInstructor(null);
        return load();
      })
      .catch(showErr);
  });

  document.getElementById("ins-clear").addEventListener("click", function () {
    fillInstructor(null);
  });

  document.getElementById("admin-instructors").addEventListener("click", function (e) {
    var edit = e.target.getAttribute("data-edit-instructor");
    var del = e.target.getAttribute("data-del-instructor");
    if (edit) {
      var p = state.instructors.find(function (x) {
        return String(x.id) === String(edit);
      });
      fillInstructor(p);
      document.getElementById("ins-name").focus();
    }
    if (del && confirm("Delete this instructor?")) {
      nethubAuth.api("/admin/instructors/" + del, { method: "DELETE" }).then(load).catch(showErr);
    }
  });

  function renderPhotos() {
    var box = document.getElementById("admin-photos");
    var rows = Object.keys(state.photos)
      .sort()
      .map(function (slot) {
        var p = state.photos[slot];
        return (
          '<article class="nh-card nh-admin-item">' +
          '<img class="nh-admin-thumb" src="' +
          esc(p.url) +
          '" alt="">' +
          "<h3>" +
          esc(p.slot) +
          "</h3><p>" +
          esc(p.alt || "") +
          '</p><label class="nh-admin-file">Replace photo<input type="file" accept="image/*" data-slot="' +
          esc(p.slot) +
          '" data-pid="' +
          p.id +
          '"></label>' +
          '<button type="button" class="nh-btn nh-btn-ghost" data-grade-photo="' +
          p.id +
          '">Grade</button>' +
          '<button type="button" class="nh-btn nh-btn-ghost" data-del-photo="' +
          p.id +
          '">Delete slot</button></article>'
        );
      });
    box.innerHTML = rows.join("") || "<p>No photo slots yet.</p>";
  }

  document.getElementById("admin-photos").addEventListener("change", function (e) {
    var input = e.target;
    if (!input.files || !input.files[0]) return;
    var slot = input.getAttribute("data-slot");
    upload(input.files[0], slot).then(load).catch(showErr);
  });

  document.getElementById("admin-photos").addEventListener("click", function (e) {
    var del = e.target.getAttribute("data-del-photo");
    var grade = e.target.getAttribute("data-grade-photo");
    if (grade) {
      var rec = Object.keys(state.photos)
        .map(function (k) {
          return state.photos[k];
        })
        .find(function (p) {
          return String(p.id) === String(grade);
        });
      if (rec) {
        document.getElementById("pg-id").value = rec.id;
        document.getElementById("pg-slot-label").textContent = "Grading slot: " + rec.slot;
        fillGrade("pg", rec);
      }
    }
    if (del && confirm("Delete this photo slot?")) {
      nethubAuth.api("/admin/photos/" + del, { method: "DELETE" }).then(load).catch(showErr);
    }
  });

  document.getElementById("photo-grade").addEventListener("submit", function (e) {
    e.preventDefault();
    var id = document.getElementById("pg-id").value;
    if (!id) {
      showErr(new Error("Pick a photo slot and click Grade first."));
      return;
    }
    nethubAuth.api("/admin/photos/" + id, { method: "PUT", body: gradeBody("pg") }).then(load).catch(showErr);
  });

  document.getElementById("photo-new").addEventListener("submit", function (e) {
    e.preventDefault();
    var slot = document.getElementById("photo-slot").value.trim();
    var alt = document.getElementById("photo-alt").value.trim();
    var file = document.getElementById("photo-file").files[0];
    if (!slot || !file) {
      showErr(new Error("Slot name and a file."));
      return;
    }
    upload(file, slot, alt)
      .then(function () {
        e.target.reset();
        return load();
      })
      .then(function () {
        var rec = Object.keys(state.photos)
          .map(function (k) {
            return state.photos[k];
          })
          .find(function (p) {
            return p.slot === slot;
          });
        if (!rec) return;
        document.getElementById("pg-id").value = rec.id;
        document.getElementById("pg-slot-label").textContent = "Grading slot: " + rec.slot;
        return nethubAuth.api("/admin/photos/" + rec.id, { method: "PUT", body: gradeBody("pg") }).then(load);
      })
      .catch(showErr);
  });

  function renderCards() {
    var box = document.getElementById("admin-cards");
    box.innerHTML = state.cards
      .map(function (c) {
        return (
          '<article class="nh-card nh-admin-item" style="border-color:' +
          esc(c.color || "transparent") +
          '"><div class="nh-admin-swatch" style="background:' +
          esc(c.color || "#1b4f8a") +
          '"></div><h3>' +
          esc(c.title) +
          "</h3><p>" +
          esc(c.section) +
          " · " +
          esc(c.body || "") +
          '</p><div class="nh-admin-actions">' +
          '<button type="button" class="nh-btn nh-btn-ghost" data-edit-card="' +
          c.id +
          '">Edit</button>' +
          '<button type="button" class="nh-btn nh-btn-ghost" data-del-card="' +
          c.id +
          '">Delete</button></div></article>'
        );
      })
      .join("") || "<p>No cards yet.</p>";
  }

  function fillCard(c) {
    document.getElementById("card-id").value = c ? c.id : "";
    document.getElementById("card-section").value = c ? c.section : "community";
    document.getElementById("card-title").value = c ? c.title : "";
    document.getElementById("card-body").value = c ? c.body || "" : "";
    document.getElementById("card-href").value = c ? c.href || "" : "";
    document.getElementById("card-cta").value = c ? c.cta || "" : "";
    document.getElementById("card-image").value = c ? c.image_url || "" : "";
    document.getElementById("card-color").value = c && c.color ? c.color : "#1b4f8a";
    document.getElementById("card-order").value = c ? c.sort_order : 0;
    fillGrade("card", c);
  }

  document.getElementById("card-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var id = document.getElementById("card-id").value;
    var body = {
      section: document.getElementById("card-section").value,
      title: document.getElementById("card-title").value,
      body: document.getElementById("card-body").value,
      href: document.getElementById("card-href").value,
      cta: document.getElementById("card-cta").value,
      image_url: document.getElementById("card-image").value,
      color: document.getElementById("card-color").value,
      sort_order: Number(document.getElementById("card-order").value || 0),
      published: 1
    };
    Object.assign(body, gradeBody("card"));
    var file = document.getElementById("card-file").files[0];
    var go = file
      ? upload(file).then(function (up) {
          body.image_url = up.url;
        })
      : Promise.resolve();
    go.then(function () {
      if (id) return nethubAuth.api("/admin/cards/" + id, { method: "PUT", body: body });
      return nethubAuth.api("/admin/cards", { method: "POST", body: body });
    })
      .then(function () {
        document.getElementById("card-file").value = "";
        fillCard(null);
        return load();
      })
      .catch(showErr);
  });

  document.getElementById("card-clear").addEventListener("click", function () {
    fillCard(null);
  });

  document.getElementById("admin-cards").addEventListener("click", function (e) {
    var edit = e.target.getAttribute("data-edit-card");
    var del = e.target.getAttribute("data-del-card");
    if (edit) {
      fillCard(
        state.cards.find(function (x) {
          return String(x.id) === String(edit);
        })
      );
    }
    if (del && confirm("Delete this card?")) {
      nethubAuth.api("/admin/cards/" + del, { method: "DELETE" }).then(load).catch(showErr);
    }
  });

  function renderColors() {
    document.getElementById("color-1").value = state.settings.card_color_1 || "#1b4f8a";
    document.getElementById("color-2").value = state.settings.card_color_2 || "#16324f";
    document.getElementById("color-3").value = state.settings.card_color_3 || "#1a3a38";
    document.getElementById("color-accent").value = state.settings.accent || "#4a8ad4";
    document.getElementById("site-tagline").value = state.settings.site_tagline || "";
  }

  document.getElementById("color-form").addEventListener("submit", function (e) {
    e.preventDefault();
    nethubAuth
      .api("/admin/settings", {
        method: "PUT",
        body: {
          card_color_1: document.getElementById("color-1").value,
          card_color_2: document.getElementById("color-2").value,
          card_color_3: document.getElementById("color-3").value,
          accent: document.getElementById("color-accent").value,
          site_tagline: document.getElementById("site-tagline").value
        }
      })
      .then(load)
      .catch(showErr);
  });

  function renderUsers() {
    var box = document.getElementById("admin-list");
    box.innerHTML = state.users
      .map(function (u) {
        return (
          '<article class="nh-card"><div class="nh-tag">' +
          esc(u.role) +
          (u.is_owner ? " · owner" : "") +
          " · " +
          esc(u.status) +
          "</div><h3>" +
          esc(u.name) +
          "</h3><p>" +
          esc(u.email) +
          "<br>" +
          esc(u.campus || "") +
          "</p>" +
          (u.status === "pending"
            ? '<button class="nh-btn nh-btn-primary" data-approve="' + u.id + '">Approve</button> '
            : "") +
          (u.role !== "admin" || (state.me && state.me.is_owner && !u.is_owner)
            ? '<button class="nh-btn nh-btn-ghost" data-del-user="' + u.id + '">Delete</button>'
            : "") +
          "</article>"
        );
      })
      .join("") || "<p>No users yet.</p>";
  }

  document.getElementById("admin-list").addEventListener("click", function (e) {
    var approve = e.target.getAttribute("data-approve");
    var del = e.target.getAttribute("data-del-user");
    if (approve) nethubAuth.api("/admin/users/" + approve + "/approve", { method: "POST" }).then(load).catch(showErr);
    if (del && confirm("Delete this user?")) {
      nethubAuth.api("/admin/users/" + del, { method: "DELETE" }).then(load).catch(showErr);
    }
  });

  function loadInbox() {
    nethubAuth.api("/admin/inbox").then(function (data) {
      function block(title, rows, line) {
        return "<h3>" + title + "</h3>" + (rows && rows.length ? rows.map(function (r) {
          return '<article class="nh-card"><p>' + line(r) + "</p></article>";
        }).join("") : "<p>None yet.</p>");
      }
      document.getElementById("admin-inbox").innerHTML =
        block("Contact", data.contact, function (r) { return esc(r.name) + " · " + esc(r.email) + "<br>" + esc(r.message); }) +
        block("Quotes", data.quotes, function (r) { return esc(r.name) + " · " + esc(r.company) + "<br>" + esc(r.message); }) +
        block("Facilitate", data.facilitate, function (r) { return esc(r.name) + " · " + esc(r.email); }) +
        block("Mentor requests", data.mentor, function (r) { return esc(r.topic) + " · " + esc(r.status); }) +
        block("Career", data.career, function (r) { return esc(r.goal) + " · " + esc(r.status); }) +
        block("Exam attempts", data.exams, function (r) { return (r.category || "exam") + " · " + r.score + "/" + r.total; }) +
        block("Clubs", data.clubs, function (r) { return esc(r.name) + " · " + esc(r.status); });
    }).catch(function () {});
  }

  function renderPages() {
    var keys = Object.keys(state.pages).sort();
    var sel = document.getElementById("page-key");
    if (!sel) return;
    sel.innerHTML = keys
      .map(function (k) {
        return '<option value="' + esc(k) + '">' + esc(k) + "</option>";
      })
      .join("");
    var box = document.getElementById("admin-pages");
    box.innerHTML = keys
      .map(function (k) {
        var p = state.pages[k];
        return (
          '<article class="nh-card nh-admin-item"><h3>' +
          esc(p.title || k) +
          "</h3><p>" +
          esc(k) +
          "<br>" +
          esc(p.lead || "") +
          '</p><button type="button" class="nh-btn nh-btn-ghost" data-edit-page="' +
          esc(k) +
          '">Edit</button></article>'
        );
      })
      .join("") || "<p>No pages yet.</p>";
  }

  function fillPage(key) {
    var p = state.pages[key] || {};
    document.getElementById("page-key").value = key;
    document.getElementById("page-kicker").value = p.kicker || "";
    document.getElementById("page-title").value = p.title || "";
    document.getElementById("page-lead").value = p.lead || "";
  }

  document.getElementById("page-key").addEventListener("change", function () {
    fillPage(this.value);
  });

  document.getElementById("page-form").addEventListener("submit", function (e) {
    e.preventDefault();
    nethubAuth
      .api("/admin/pages", {
        method: "PUT",
        body: {
          page_key: document.getElementById("page-key").value,
          kicker: document.getElementById("page-kicker").value,
          title: document.getElementById("page-title").value,
          lead: document.getElementById("page-lead").value
        }
      })
      .then(load)
      .catch(showErr);
  });

  document.getElementById("admin-pages").addEventListener("click", function (e) {
    var key = e.target.getAttribute("data-edit-page");
    if (key) fillPage(key);
  });

  function renderGallery() {
    var box = document.getElementById("admin-gallery");
    box.innerHTML = state.gallery
      .map(function (g) {
        return (
          '<article class="nh-card nh-admin-item"><img class="nh-admin-thumb" src="' +
          esc(g.photo_url) +
          '" alt=""><h3>' +
          esc(g.title) +
          "</h3><p>" +
          esc(g.caption || "") +
          '</p><div class="nh-admin-actions"><button type="button" class="nh-btn nh-btn-ghost" data-edit-gal="' +
          g.id +
          '">Edit</button><button type="button" class="nh-btn nh-btn-ghost" data-del-gal="' +
          g.id +
          '">Delete</button></div></article>'
        );
      })
      .join("") || "<p>No gallery photos yet.</p>";
  }

  function fillGal(g) {
    document.getElementById("gal-id").value = g ? g.id : "";
    document.getElementById("gal-title").value = g ? g.title : "";
    document.getElementById("gal-caption").value = g ? g.caption || "" : "";
    document.getElementById("gal-photo").value = g ? g.photo_url || "" : "";
    document.getElementById("gal-order").value = g ? g.sort_order : 0;
    fillGrade("gal", g);
  }

  document.getElementById("gal-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var id = document.getElementById("gal-id").value;
    var body = {
      title: document.getElementById("gal-title").value,
      caption: document.getElementById("gal-caption").value,
      photo_url: document.getElementById("gal-photo").value,
      sort_order: Number(document.getElementById("gal-order").value || 0),
      published: 1
    };
    Object.assign(body, gradeBody("gal"));
    var file = document.getElementById("gal-file").files[0];
    var go = file
      ? upload(file).then(function (up) {
          body.photo_url = up.url;
        })
      : Promise.resolve();
    go.then(function () {
      if (id) return nethubAuth.api("/admin/gallery/" + id, { method: "PUT", body: body });
      return nethubAuth.api("/admin/gallery", { method: "POST", body: body });
    })
      .then(function () {
        document.getElementById("gal-file").value = "";
        fillGal(null);
        return load();
      })
      .catch(showErr);
  });

  document.getElementById("gal-clear").addEventListener("click", function () {
    fillGal(null);
  });

  document.getElementById("admin-gallery").addEventListener("click", function (e) {
    var edit = e.target.getAttribute("data-edit-gal");
    var del = e.target.getAttribute("data-del-gal");
    if (edit) {
      fillGal(
        state.gallery.find(function (x) {
          return String(x.id) === String(edit);
        })
      );
    }
    if (del && confirm("Delete this gallery photo?")) {
      nethubAuth.api("/admin/gallery/" + del, { method: "DELETE" }).then(load).catch(showErr);
    }
  });

  function renderSessions() {
    var box = document.getElementById("admin-sessions");
    box.innerHTML = state.sessions
      .map(function (s) {
        return (
          '<article class="nh-card nh-admin-item"><h3>' +
          esc(s.title) +
          "</h3><p>" +
          esc(s.starts_at || "") +
          "<br>" +
          esc(s.join_url || "") +
          '</p><div class="nh-admin-actions"><button type="button" class="nh-btn nh-btn-ghost" data-edit-sess="' +
          s.id +
          '">Edit</button><button type="button" class="nh-btn nh-btn-ghost" data-del-sess="' +
          s.id +
          '">Delete</button></div></article>'
        );
      })
      .join("") || "<p>No sessions yet.</p>";
  }

  function fillSess(s) {
    document.getElementById("sess-id").value = s ? s.id : "";
    document.getElementById("sess-title").value = s ? s.title : "";
    document.getElementById("sess-when").value = s ? s.starts_at || "" : "";
    document.getElementById("sess-url").value = s ? s.join_url || "" : "";
    document.getElementById("sess-notes").value = s ? s.notes || "" : "";
  }

  document.getElementById("sess-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var id = document.getElementById("sess-id").value;
    var body = {
      title: document.getElementById("sess-title").value,
      starts_at: document.getElementById("sess-when").value,
      join_url: document.getElementById("sess-url").value,
      notes: document.getElementById("sess-notes").value,
      published: 1
    };
    var req = id
      ? nethubAuth.api("/admin/sessions/" + id, { method: "PUT", body: body })
      : nethubAuth.api("/admin/sessions", { method: "POST", body: body });
    req
      .then(function () {
        fillSess(null);
        return load();
      })
      .catch(showErr);
  });

  document.getElementById("sess-clear").addEventListener("click", function () {
    fillSess(null);
  });

  document.getElementById("admin-sessions").addEventListener("click", function (e) {
    var edit = e.target.getAttribute("data-edit-sess");
    var del = e.target.getAttribute("data-del-sess");
    if (edit) {
      fillSess(
        state.sessions.find(function (x) {
          return String(x.id) === String(edit);
        })
      );
    }
    if (del && confirm("Delete this session?")) {
      nethubAuth.api("/admin/sessions/" + del, { method: "DELETE" }).then(load).catch(showErr);
    }
  });

  function renderMessages() {
    var box = document.getElementById("admin-messages");
    box.innerHTML = state.messages
      .map(function (m) {
        return (
          '<article class="nh-card"><p>' +
          esc(m.body) +
          "</p><p class=\"intro\">" +
          esc(m.from_name || "") +
          " · " +
          esc(m.created_at || "") +
          '</p><button type="button" class="nh-btn nh-btn-ghost" data-del-msg="' +
          m.id +
          '">Delete</button></article>'
        );
      })
      .join("") || "<p>No notes yet.</p>";
  }

  document.getElementById("msg-form").addEventListener("submit", function (e) {
    e.preventDefault();
    nethubAuth
      .api("/admin/messages", { method: "POST", body: { body: document.getElementById("msg-body").value } })
      .then(function () {
        document.getElementById("msg-body").value = "";
        return load();
      })
      .catch(showErr);
  });

  document.getElementById("admin-messages").addEventListener("click", function (e) {
    var del = e.target.getAttribute("data-del-msg");
    if (del && confirm("Delete this note?")) {
      nethubAuth.api("/admin/messages/" + del, { method: "DELETE" }).then(load).catch(showErr);
    }
  });

  function renderStaff() {
    var owner = state.me && state.me.is_owner;
    document.getElementById("staff-form").hidden = !owner;
    document.getElementById("staff-note").textContent = owner
      ? ""
      : "Staff desks cannot create another admin or delete the owner.";
    var box = document.getElementById("admin-staff");
    box.innerHTML = state.users
      .filter(function (u) {
        return u.role === "admin";
      })
      .map(function (u) {
        return (
          '<article class="nh-card"><div class="nh-tag">' +
          (u.is_owner ? "owner" : "staff") +
          "</div><h3>" +
          esc(u.name) +
          "</h3><p>" +
          esc(u.email) +
          " · " +
          esc(u.username || "") +
          "</p></article>"
        );
      })
      .join("");
  }

  document.getElementById("staff-form").addEventListener("submit", function (e) {
    e.preventDefault();
    nethubAuth
      .api("/admin/staff", {
        method: "POST",
        body: {
          name: document.getElementById("staff-name").value,
          email: document.getElementById("staff-email").value,
          username: document.getElementById("staff-username").value,
          password: document.getElementById("staff-pass").value
        }
      })
      .then(function () {
        e.target.reset();
        return load();
      })
      .catch(showErr);
  });

  document.querySelectorAll("[data-tab]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var tab = btn.getAttribute("data-tab");
      document.querySelectorAll("[data-tab]").forEach(function (b) {
        b.classList.toggle("is-on", b === btn);
      });
      document.querySelectorAll("[data-panel]").forEach(function (p) {
        p.hidden = p.getAttribute("data-panel") !== tab;
      });
    });
  });

  load().catch(showErr);
  loadInbox();
})();
